import requests
import warnings

from url_checker import stage1_decision
from test import stage3_decision   # rename your stage-3 file accordingly

warnings.filterwarnings("ignore")


def final_decision(url: str) -> dict:
    """
    Hybrid decision logic:

    1 + 1 → PHISHING
    0 + 0 → LEGITIMATE
    mixed → SUSPICIOUS
    """

    # Run both stages
    result_stage1 = stage1_decision(url)
    result_stage3 = stage3_decision(url)

    # Check errors
    if "error" in result_stage1 or "error" in result_stage3:
        return {
            "url": url,
            "error": "One or more stages failed",
            "stage1": result_stage1,
            "stage2": result_stage3
        }

    s1 = result_stage1["decision"]
    s3 = result_stage3["decision"]

    # Fusion logic
    if s1 == 1 and s3 == 1:
        final_label = "PHISHING"
    elif s1 == 0 and s3 == 0:
        final_label = "LEGITIMATE"
    else:
        final_label = "SUSPICIOUS"

    return {
        "url": url,
        "final_label": final_label,
        "stage1": result_stage1,
        "stage3": result_stage3
    }


# -----------------------------
# Interactive Mode
# -----------------------------
if __name__ == "__main__":

    print("\nHybrid Phishing Detection System")
    print("Type 'exit' to quit\n")

    while True:
        url = input("Enter URL: ").strip()

        if url.lower() == "exit":
            break

        result = final_decision(url)

        print("\n================ FINAL RESULT ================")

        if "error" in result:
            print("Error:", result["error"])
        else:
            print("Final Label:", result["final_label"])

            print("\n--- Stage 1 ---")
            print(result["stage1"])

            print("\n--- Stage 3 ---")
            print(result["stage3"])

        print("==============================================\n")