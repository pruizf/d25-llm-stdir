## Fine-tuning experiments

Experiments were carried out on Google Colab. The GPU was an L4 for FlauBERT and XLM-R, and a V100 for the earlier experiments with CamemBERT and M-BERT.

The filename tells which experiment each notebook corresponds to, e.g.:

```
stgcls__estp__flaubert_base_cased__100__1.ipyb
```

If we split on the double underscores, `__`, the filename has four fields, parsed as follows:

1. Prefix shared by all notebooks for this task (`stgcls__estp__`)
2. Model name (`flaubert_base_cased` in the example name above)
3. Proportion of the examples used for fine-tuning (here `100` for 100%). Can be 100, 050, 025, 010 or 005, where the numbers mean a percentage
4. Run number (`1` in the example). Macro-F1 was averaged over 5 runs, the value here can be 1, 2, 3, 4, or 5.


