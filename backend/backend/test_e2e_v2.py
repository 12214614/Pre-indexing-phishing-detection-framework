#!/usr/bin/env python
"""
End-to-end diagnostic test for PIPPF system:
- Check if crawler is working
- Check if ML model is loaded
- Check if feature extraction works
- Check if API endpoint returns correct data
- Verify domain age extraction
"""

import os
import sys
import json
import django
import requests
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core_api.feature_extractor import extract_all_features, extract_whois_features
from core_api.ml_loader import predict_url, model, threshold, model_name, model_source_dir
from core_api.ncd_stage3 import run_ncd_stage3
from crawler.models import CrawledURL
from analysis.models import URLAnalysis

print("=" * 80)
print("PIPPF END-TO-END DIAGNOSTIC TEST")
print("=" * 80)
print()

# ============================================================================
# TEST 1: Check ML Model Loading
# ============================================================================
print("TEST 1: ML Model Loading")
print("-" * 80)
try:
    print("[OK] ML Model loaded successfully!")
    print(f"   Model type: {type(model)}")
    print(f"   Model name: {model_name}")
    print(f"   Threshold: {threshold}")
    print(f"   Source dir: {model_source_dir}")
except Exception as e:
    print(f"[FAIL] ML Model loading FAILED: {str(e)}")

print()

# ============================================================================
# TEST 2: Feature Extraction (Domain Age Check)
# ============================================================================
print("TEST 2: Feature Extraction (especially Domain Age)")
print("-" * 80)
test_url_1 = "https://google.com"
test_url_2 = "https://example.com"

for test_url in [test_url_1, test_url_2]:
    print(f"\nExtracting features for: {test_url}")
    try:
        features = extract_all_features(test_url)
        print(f"[OK] Features extracted successfully!")
        print(f"   Total features: {len(features)}")
        
        # Check if domain_age_days is present
        if 'domain_age_days' in features:
            print(f"   [OK] Domain Age: {features['domain_age_days']} days")
        else:
            print(f"   [FAIL] Domain Age NOT found in features!")
        
        # Show first 10 features
        print(f"   Sample features: {dict(list(features.items())[:5])}")
        
    except Exception as e:
        print(f"   [FAIL] Feature extraction FAILED: {str(e)}")

print()

# ============================================================================
# TEST 3: ML Prediction
# ============================================================================
print("TEST 3: ML Prediction")
print("-" * 80)
try:
    features = extract_all_features(test_url_1)
    result = predict_url(features)
    print(f"[OK] ML Prediction successful!")
    print(f"   URL: {test_url_1}")
    print(f"   Prediction: {result['prediction']} (0=legitimate, 1=phishing)")
    print(f"   Confidence: {result['probability']:.4f}")
    print(f"   Model: {result.get('model_name', 'unknown')}")
    print(f"   Threshold: {result.get('threshold', 'unknown')}")
except Exception as e:
    print(f"[FAIL] ML Prediction FAILED: {str(e)}")

print()

# ============================================================================
# TEST 4: NCD Stage 3 (DOM + JS similarity)
# ============================================================================
print("TEST 4: NCD Stage 3 (DOM/JS Similarity)")
print("-" * 80)
try:
    ncd_result = run_ncd_stage3(test_url_1)
    print(f"[OK] NCD Stage 3 executed!")
    print(f"   URL: {test_url_1}")
    print(f"   NCD Available: {ncd_result.get('ncd_available', False)}")
    print(f"   NCD Prediction: {ncd_result.get('ncd_prediction', 'N/A')}")
    print(f"   NCD Phishing Score: {ncd_result.get('ncd_phish_score', 'N/A')}")
    print(f"   NCD Legit Score: {ncd_result.get('ncd_legit_score', 'N/A')}")
    print(f"   NCD Score Gap: {ncd_result.get('ncd_score_gap', 'N/A')}")
except Exception as e:
    print(f"[FAIL] NCD Stage 3 FAILED: {str(e)}")

print()

# ============================================================================
# TEST 5: Crawler Functionality
# ============================================================================
print("TEST 5: Crawler Functionality")
print("-" * 80)
try:
    initial_count = CrawledURL.objects.count()
    print(f"[OK] Crawler database connection successful!")
    print(f"   Current URLs in database: {initial_count}")
    
    # List last 3 URLs
    recent_urls = CrawledURL.objects.all().order_by('-id')[:3]
    if recent_urls:
        print(f"   Last 3 URLs:")
        for url in recent_urls:
            print(f"      - {url.website_url} (Status: {url.status})")
    else:
        print(f"   No URLs in database yet")
except Exception as e:
    print(f"[FAIL] Crawler database access FAILED: {str(e)}")

print()

# ============================================================================
# TEST 6: Complete API Endpoint Flow
# ============================================================================
print("TEST 6: Complete API Flow (Simulating Frontend Request)")
print("-" * 80)
try:
    api_url = "http://127.0.0.1:8001/api/core/submit-url/"
    test_urls = [
        "https://google.com",
        "https://github.com",
        "https://example-suspicious-domain-12345.com"
    ]
    
    for test_url in test_urls:
        print(f"\nTesting URL: {test_url}")
        response = requests.post(
            api_url,
            json={"website_url": test_url},
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            print(f"[OK] API Response successful (HTTP {response.status_code})")
            print(f"   Prediction: {data.get('prediction', 'N/A')}")
            print(f"   Confidence: {data.get('confidence', 'N/A'):.4f}")
            print(f"   Status: {data.get('status', 'N/A')}")
            print(f"   Stage1 ML: {data.get('stage1_ml', 'N/A')}")
            print(f"   Stage3 NCD: {data.get('stage3_ncd', 'N/A')}")
            print(f"   Consensus: {data.get('consensus', 'N/A')}")
            
            # Check if domain_age is in response
            if 'domain_age_days' in data:
                domain_age = data['domain_age_days']
                if domain_age >= 0:
                    print(f"   [OK] Domain Age in response: {domain_age} days")
                else:
                    print(f"   [WARN] Domain Age in response but WHOIS failed: {domain_age}")
            else:
                print(f"   [FAIL] Domain Age NOT in API response")
                
        else:
            print(f"[FAIL] API Request FAILED (HTTP {response.status_code})")
            print(f"   Response: {response.text[:200]}")
            
except requests.exceptions.ConnectionError:
    print(f"[FAIL] Cannot connect to API (http://127.0.0.1:8001)")
    print(f"   Make sure backend is running with: python manage.py runserver 127.0.0.1:8001")
except Exception as e:
    print(f"[FAIL] API test FAILED: {str(e)}")

print()

# ============================================================================
# TEST 7: Database Analysis Models
# ============================================================================
print("TEST 7: Database Analysis Models")
print("-" * 80)
try:
    total_analyses = URLAnalysis.objects.count()
    phishing_count = URLAnalysis.objects.filter(prediction="phishing").count()
    legit_count = URLAnalysis.objects.filter(prediction="legitimate").count()
    suspicious_count = URLAnalysis.objects.filter(prediction="suspicious").count()
    
    print(f"[OK] Analysis database accessible!")
    print(f"   Total analyses: {total_analyses}")
    print(f"   Phishing predictions: {phishing_count}")
    print(f"   Legitimate predictions: {legit_count}")
    print(f"   Suspicious predictions: {suspicious_count}")
    
    if total_analyses > 0:
        recent_analysis = URLAnalysis.objects.latest('id')
        print(f"\n   Most recent analysis:")
        print(f"      URL: {recent_analysis.crawled_url.website_url}")
        print(f"      Prediction: {recent_analysis.prediction}")
        print(f"      Confidence: {recent_analysis.confidence_score}")
        print(f"      Reason: {recent_analysis.reason[:100]}...")
        
except Exception as e:
    print(f"[FAIL] Database access FAILED: {str(e)}")

print()
print("=" * 80)
print("DIAGNOSTIC TEST COMPLETE")
print("=" * 80)
