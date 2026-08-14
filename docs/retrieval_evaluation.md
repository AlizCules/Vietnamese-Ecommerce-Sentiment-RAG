# Retrieval Evaluation

Manual retrieval relevance was assessed on 15 representative Vietnamese queries. The aggregate results are:

| Metric | Precision |
| --- | ---: |
| Precision@3 | 0.422 |
| Precision@5 | **0.507** |
| Precision@10 | 0.487 |

The evaluation is a small diagnostic sample, not a comprehensive production benchmark. It is useful for comparing retrieval behavior and inspecting evidence quality, but the result should not be described as highly accurate or general-purpose. The source table is `results/module5/manual_precision_overall.csv` and the chart is `figures/module5/manual_precision_at_k.png`.

## Interpretation

Precision@5 is the selected compact summary because it reflects the quality of a short evidence list. Query wording, category coverage, embedding behavior and metadata quality all affect the result. Expanding the evaluation with independently labeled query–document relevance would be the next rigorous step.
