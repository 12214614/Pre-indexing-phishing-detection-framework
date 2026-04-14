from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from crawler.models import CrawledURL
from analysis.models import URLAnalysis

# ML + NCD Imports
from .feature_extractor import extract_all_features
from .ml_loader import predict_url
from .ncd_stage3 import run_ncd_stage3


# -----------------------------------------------------
# Submit URL + ML Prediction API
# -----------------------------------------------------
class SubmitURLAPIView(APIView):

    def post(self, request):

        website_url = request.data.get("website_url")

        if not website_url:
            return Response(
                {"error": "website_url is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------
        # 1️⃣ Check Duplicate URL
        # -----------------------------------------
        existing = CrawledURL.objects.filter(
            website_url=website_url
        ).first()

        if existing:
            # Extract features to get domain age even for cached URLs
            try:
                features = extract_all_features(website_url)
                domain_age = features.get("domain_age_days", -1)
            except:
                domain_age = -1
            
            try:
                analysis = URLAnalysis.objects.get(crawled_url=existing)
                return Response({
                    "message": "URL already analyzed",
                    "website_url": existing.website_url,
                    "prediction": analysis.prediction,
                    "confidence": analysis.confidence_score,
                    "status": existing.status,
                    "domain_age_days": domain_age,
                    "reason": analysis.reason
                }, status=status.HTTP_200_OK)

            except URLAnalysis.DoesNotExist:
                return Response({
                    "message": "URL already submitted but not analyzed yet",
                    "status": existing.status,
                    "domain_age_days": domain_age
                }, status=status.HTTP_200_OK)

        # -----------------------------------------
        # 2️⃣ Save New URL
        # -----------------------------------------
        crawled = CrawledURL.objects.create(
            website_url=website_url,
            status="pending"
        )

        # -----------------------------------------
        # 3️⃣ Feature Extraction
        # -----------------------------------------
        try:
            features = extract_all_features(website_url)
        except Exception as e:
            return Response(
                {"error": f"Feature extraction failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # -----------------------------------------
        # 4️⃣ ML Prediction (Stage 1)
        # -----------------------------------------
        try:
            result = predict_url(features)

            prediction_value = result["prediction"]
            probability = result["probability"]
            ml_model_name = result.get("model_name", "rf")
            ml_threshold = result.get("threshold")
            ml_source = result.get("model_source_dir", "")

            # Convert numeric prediction to label
            ml_label = "phishing" if prediction_value == 1 else "legitimate"

        except Exception as e:
            return Response(
                {"error": f"ML prediction failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # -----------------------------------------
        # 5️⃣ NCD Stage 3 (DOM + JS similarity)
        # -----------------------------------------
        ncd_result = run_ncd_stage3(website_url)
        ncd_label  = ncd_result.get("ncd_prediction")

        # -----------------------------------------
        # 6️⃣ Consensus Fusion (same as final_predict.py)
        #    Both phishing  → PHISHING
        #    Both legitimate→ LEGITIMATE
        #    Mixed          → SUSPICIOUS (treated as phishing for safety)
        # -----------------------------------------
        ncd_confident = ncd_result.get("ncd_confident", False)

        if ncd_result["ncd_available"] and ncd_confident and ncd_label is not None:
            if ml_label == "phishing" and ncd_label == "phishing":
                final_label = "phishing"
                consensus   = "agreement"
            elif ml_label == "legitimate" and ncd_label == "legitimate":
                final_label = "legitimate"
                consensus   = "agreement"
            else:
                # Stages disagree — mark suspicious, treat as phishing for safety
                final_label = "suspicious"
                consensus   = "disagreement"
        else:
            # NCD inconclusive or unavailable — fall back to ML alone
            final_label = ml_label
            consensus   = "ml_only" if not ncd_result["ncd_available"] else "ncd_inconclusive"

        # -----------------------------------------
        # 7️⃣ Save Analysis
        # -----------------------------------------
        URLAnalysis.objects.create(
            crawled_url=crawled,
            prediction=final_label,
            confidence_score=probability if probability is not None else 0.5,
            reason=(
                f"ML:{ml_label} ({ml_model_name}, thr={ml_threshold}) | "
                f"NCD:{ncd_label or 'N/A'} | consensus:{consensus}"
            )
        )

        # -----------------------------------------
        # 8️⃣ Decision Logic
        # -----------------------------------------
        if final_label in ("phishing", "suspicious"):
            crawled.status = "blocked"
        else:
            crawled.status = "legitimate"

        crawled.save()

        return Response({
            "website_url": website_url,
            "prediction":  final_label,
            "confidence":  probability,
            "status":      crawled.status,
            "domain_age_days": features.get("domain_age_days", -1),
            "stage1_ml":   ml_label,
            "stage1_model": ml_model_name,
            "stage1_threshold": ml_threshold,
            "stage1_model_source": ml_source,
            "stage3_ncd":  ncd_label or "unavailable",
            "consensus":   consensus,
            "ncd_phish_score": ncd_result.get("ncd_phish_score"),
            "ncd_legit_score": ncd_result.get("ncd_legit_score"),
            "ncd_score_gap": ncd_result.get("ncd_score_gap"),
        }, status=status.HTTP_200_OK)


# -----------------------------------------------------
# Get All URLs API
# -----------------------------------------------------
class URLListAPIView(APIView):

    def get(self, request):
        urls = CrawledURL.objects.all()
        result = []
        for url in urls:
            try:
                analysis = URLAnalysis.objects.get(crawled_url=url)
                confidence = float(analysis.confidence_score)
            except URLAnalysis.DoesNotExist:
                confidence = 0.5
            website = url.website_url
            url_len = len(website)
            result.append({
                "id": url.id,
                "website_url": website,
                "status": url.status,
                "confidence": confidence,
                "ssl": website.startswith("https://"),
                "complexity": "High" if url_len >= 60 else "Medium" if url_len >= 30 else "Low",
            })
        return Response(result, status=status.HTTP_200_OK)


# -----------------------------------------------------
# Dashboard Statistics API
# -----------------------------------------------------
class DashboardAPIView(APIView):

    def get(self, request):

        total = CrawledURL.objects.count()
        phishing = CrawledURL.objects.filter(status="blocked").count()
        legitimate = CrawledURL.objects.filter(status="legitimate").count()

        return Response({
            "total_urls": total,
            "phishing_detected": phishing,
            "legitimate": legitimate
        }, status=status.HTTP_200_OK)