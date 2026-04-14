from sklearn.metrics import classification_report, roc_auc_score


def evaluate(y_true, scores):
    print(classification_report(y_true, scores))
    print("ROC-AUC:", roc_auc_score(y_true, scores))