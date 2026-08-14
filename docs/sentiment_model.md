# Sentiment Classification

## Task and labels

The task is three-class prediction from Vietnamese review text. Labels are rating-derived: ratings 1–2 map to negative, 3 to neutral and 4–5 to positive. They are not independent human annotations.

## Representation and selection

The candidate pipelines use TF-IDF with unigram and bigram features. A majority baseline, Logistic Regression and Linear SVM are compared. The model configuration is selected using validation Macro-F1; the test partition is evaluated only after selection.

## Verified test results

| Model | Macro-F1 | Accuracy |
| --- | ---: | ---: |
| Majority baseline | 0.200361 | 0.429677 |
| Logistic Regression | 0.894028 | 0.917419 |
| Linear SVM | **0.909809** | **0.932903** |

The Linear SVM is selected by validation Macro-F1. Its test F1 scores are approximately 0.943 for negative, 0.823 for neutral and 0.964 for positive. Neutral is the most difficult class in the recorded classification report.

## Error analysis

The tracked error-analysis tables contain short or ambiguous reviews such as brief quality statements and mixed/underspecified wording. These examples motivate per-class metrics and caution against treating the aggregate score as a human-annotation agreement measure. The benchmark files under `results/module2/` are unchanged.
