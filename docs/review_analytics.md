# Review Analytics

The descriptive analysis treats review text and corpus metadata as analytical data before applying classification or retrieval engineering.

## Sentiment composition

The three-class labeled set contains 2,217 positive reviews (42.95%), 2,074 negative reviews (40.18%) and 871 neutral reviews (16.87%). The distribution is sufficiently imbalanced to justify Macro-F1 alongside accuracy.

The aggregate source is `results/module3/overall_sentiment_distribution.csv`, with the corresponding chart in `figures/module3/sentiment_3class_distribution.png`.

## Text length

The project summary reports an average sentiment-review length of approximately 13.13 tokens/units under the pipeline's length definition and an average retrieval-corpus length of approximately 26.79. The length chart is descriptive: it helps explain why short, ambiguous reviews can be difficult for a text classifier, but it is not a causal claim.

## Retrieval-corpus composition

The 82,677-document corpus is concentrated in Fashion (24,989), Electronic (19,645), HealthBeauty (13,739), BabiesToys (10,827) and HomeLifestyle (9,798), with smaller App, Cosmetic and Mobile groups. This composition matters when interpreting retrieval coverage: a query from a well-represented category has more candidate evidence than a query from a sparse category.

## Interpretation safeguards

The rating-versus-sentiment cross-tab is not presented as an independent analytical finding because the three-class label is constructed directly from the rating. The analysis therefore emphasizes class balance, text length, corpus composition and model error patterns rather than claiming that ratings independently validate the labels.
