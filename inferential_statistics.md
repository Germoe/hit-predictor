# Inferential Statistics

The section on inferential statistics is looking at statistical significance on observations and thoughts during the EDA. This is an essential step to understanding whether or not the differences between hits and non-hits are factual or just happened by chance.

The focus for us lies on three categories:
- Distribution between Hits and Non-Hits
- Correlation with the Target Variable (i.e. hit or non-hit)
- Collinearity between features

# Challenges

### Normality 

One of the biggest challenges for this project was the lack of available normally distributed data. Normally distributed data is often a requirement for classical statistic tests. Luckily, the Central Limit Theorem is helping us to use the Z-Test to compare distribution differences anyways.

### Statistical and Practical Significance

Due to the large sample sizes even the slightest differences can be considered statistically significant but might not actually allow us to use a feature for our model as their predictive qualities are limited. As in many other cases we need to rely on a combination of staistical test and also sound reasoning for model building.

### Preprocessed Features

As we're relying on features that are preprocessed and aggregated by Spotify we're looking at features that are obtuse and abstract features. While this allows for intuitive interpretations, we're losing some of the interpretability as Spotify doesn't allow us to fully understand how these features come together.


