"""
Evaluation harness — runs the pipeline over a test set and reports
reliability metrics (success rate, flagged-claim rate, etc.)
"""

from main import get_structured_data
from eval_data import CLINICAL_NOTES, INSURANCE_CLAIMS


def run_evaluation():
    results = {
        "clinical_notes": {"total": 0, "success": 0, "failed": 0},
        "insurance_claims": {"total": 0, "success": 0, "failed": 0, "flagged": 0},
    }

    print("Evaluating clinical notes...")
    for note in CLINICAL_NOTES:
        data = get_structured_data(note, doc_type="clinical_note")
        results["clinical_notes"]["total"] += 1
        if "error" in data:
            results["clinical_notes"]["failed"] += 1
        else:
            results["clinical_notes"]["success"] += 1

    print("Evaluating insurance claims...")
    for claim in INSURANCE_CLAIMS:
        data = get_structured_data(claim, doc_type="insurance_claim")
        results["insurance_claims"]["total"] += 1
        if "error" in data:
            results["insurance_claims"]["failed"] += 1
        else:
            results["insurance_claims"]["success"] += 1
            if data.get("flagged_for_review"):
                results["insurance_claims"]["flagged"] += 1

    return results


def print_report(results):
    print("\n===== EVALUATION REPORT =====\n")

    cn = results["clinical_notes"]
    success_rate = (cn["success"] / cn["total"]) * 100 if cn["total"] else 0
    print(f"Clinical Notes: {cn['success']}/{cn['total']} extracted successfully ({success_rate:.1f}%)")

    ic = results["insurance_claims"]
    success_rate_ic = (ic["success"] / ic["total"]) * 100 if ic["total"] else 0
    print(f"Insurance Claims: {ic['success']}/{ic['total']} extracted successfully ({success_rate_ic:.1f}%)")
    print(f"  -> {ic['flagged']} claims flagged for manual review")

    overall_total = cn["total"] + ic["total"]
    overall_success = cn["success"] + ic["success"]
    overall_rate = (overall_success / overall_total) * 100 if overall_total else 0
    print(f"\nOverall extraction reliability: {overall_rate:.1f}%")


if __name__ == "__main__":
    results = run_evaluation()
    print_report(results)