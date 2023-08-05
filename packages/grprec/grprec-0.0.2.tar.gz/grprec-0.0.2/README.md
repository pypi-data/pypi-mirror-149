# GrpRec

GrpRec is a pyhon library designed for group recommendation systems.The diffrent task that you can do using this library are:

    - Generate different types of groups from your dataset using many methods in group recommendation litterature (Random groups, similar groups, divergent groups, etc.)
    - Split your ratings dataset with different methods (train/test, train/validation/test, k-fold etc.)
    - Generate prediction scores for your generated groups using individual recommendation systems algorithm.
    - Use different group score aggregation strategies on the predicted scores to generate the recommendations (Average, Least miery, Borda count, etc.)
    - Evaluate the recommendations using diffrent metrics used in litterature (Precision, Recall, First hit, NDCG)

## Installation

To install the GrpRec library execute the following command in your python console:

```python
pip install grprec
```
