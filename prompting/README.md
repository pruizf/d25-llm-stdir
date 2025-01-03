# Prompting experiments

- Clients to run the LLM are:
  - `openai_client.py`
  - `openai_client_grouped.py`
  - `llama_client.py`
  - `mistral_client.py`
  - `mistral_client_grouped.py`
- For each batch, they create an output directory under `outputs`.
- The clients with `_grouped` in the name are for grouped stage directions (i.e. having several stage directions to classify in the same prompt, we tested with 75 stage directions).
- Evaluation scripts are:
  - `evaluation.py` for GPT-4 and Mistral results
  - `evaluation_llama.py` for Llama results
- Configuration options are in `config.py`
- Examples to classify are in `data`

A table summarizing results for experiments with only one stage direction to classify per prompt is at ["Result summary (individual stage direction prompts)"](#indiv-stgdir). A table summarizing results for experiments with up to 75 stage directions per prompt is at ["Grouped prompts"](#grouped-stgdir).

# Usage

CLI options can be seen in the `argparse` options in the clients.

## Example
- The command `python openai_client.py batch_014 data/stgdir_labelGeneric_trainvalid_100-test.csv gpt-4o-mini def-few-shot en` does the following (CLI options listed in order):
  - Output is saved to `outputs/batch_014`
  - Examples to classify are in `data/stgdir_labelGeneric_trainvalid_100-test.csv`
  - The model is `gpt-4o-mini`
  - Prompting mode is `def-few-shot`, which uses a detailed definition for each category and 20 examples for each category. Allowed prompt modes are in `config.py`.
  - The language for the category definitions is `en` (possible values in `config.py`).

# Data

- The data, available at https://nakala.fr/10.34847/nkl.fde37ug3 are from [Schneider (2024)](https://nakala.fr/10.34847/nkl.3ecb73zp) and [Schneider & Ruiz Fabo (2024)](https://aclanthology.org/2024.latechclfl-1.28/)
- The complete test-set (2923 examples) is used run in zero-shot batches, and a 30% fraction, stratified by category, is run in few-shot batches.

# Prompts
- The prompts, in both English and French, are in `prompts.py` and `prompts_grouped.py`. The prompts are templates with several fields, filled dynamically by the client with category definitions in all settings and, additionally, some examples in the few-shot setting.
- Category definitions are in `data/category_info.py`.
- In the case of few-shot batches, the examples in `data/sampled_df_for_prompts_0001.tsv` are added to the prompt.
- `prompts_grouped.py` contains prompts for grouped stage directions, where the model is asked to classify a list of stage directions. The order of stage directions on the list does not follow a pattern (is shuffled). 


# Evaluation

- Scripts `evaluate.py` and `evaluate_llama.py` produce a classification report and confustion matrix for a batch, for GPT or Mistral and Llama 3.1 results respectively. Results are written to the `plots` directory in each batch's output directory.


# Result summary

A description of column values follows the results tables.

<a name="indiv-stgdir"></a>

## Individual stage direction prompts

Batch IDs starting with 0 are for GPT-4 models, starting with 1 are for Llama models, and starting with 2 are for Mistral models.

| id  | definition type  | prompt language |         example use         |     data split     |       model        | macro F1 | weighted F1 | acc  |
|-----|:----------------:|:---------------:|:---------------------------:|:------------------:|:------------------:|:--------:|:-----------:|:----:|
| 001 |      simple      |       en        |          two-shot           |         1          |    gpt-4o-mini     |   0.48   |    0.53     | 0.52 |
| 002 |      simple      |       en        |          zero-shot          |   0.3 stratified   |    gpt-4o-mini     |   0.51   |    0.57     | 0.57 |
| 003 |     detailed     |       en        |          zero-shot          |   0.3 stratified   |    gpt-4o-mini     |   0.53   |    0.59     | 0.57 |
| 004 |     detailed     |       en        |          zero-shot          |   0.3 stratified   |       gpt-4o       |   0.7    |    0.73     | 0.72 |
| 005 |     detailed     |       en        |          zero-shot          |         1          |       gpt-4o       |   0.71   |    0.74     | 0.73 |
| 006 |     detailed     |       en        |          zero-shot          |         1          |    gpt-4o-mini     |   0.58   |    0.64     | 0.61 |
| 007 |      simple      |       en        |   few-shot (20 per class)   |   0.3 stratified   |    gpt-4o-mini     |   0.57   |    0.64     | 0.63 |
| 008 |     detailed     |       en        |   few-shot (20 per class)   |   0.3 stratified   |    gpt-4o-mini     |   0.58   |    0.65     | 0.67 |
| 009 |     detailed     |       en        |   few-shot (20 per class)   |   0.3 stratified   |       gpt-4o       |   0.73   |    0.79     | 0.78 |
| 010 |     detailed     |       fr        |   few-shot (20 per class)   |   0.3 stratified   |    gpt-4o-mini     |   0.62   |     0.7     | 0.69 |
| 011 |     detailed     |       fr        |          zero-shot          |         1          |       gpt-4o       |   0.69   |    0.72     | 0.71 |
| 012 |     detailed     |       fr        |          zero-shot          |         1          |    gpt-4o-mini     |   0.54   |    0.59     | 0.57 |
| 013 |     detailed     |       fr        |   few-shot (20 per class)   |         1          |    gpt-4o-mini     |   0.61   |    0.68     | 0.67 |
| 014 |     detailed     |       en        |   few-shot (20 per class)   |         1          |    gpt-4o-mini     |   0.6    |    0.67     | 0.67 |
| 015 |     detailed     |       fr        |   few-shot (20 per class)   | 0.3<br/>stratified |       gpt-4o       |   0.7    |    0.75     | 0.75 |
| 102 |     detailed     |       en        |          zero-shot          |         1          |      llama-3       |   0.43   |    0.52     | 0.49 |
| 103 |     detailed     |       en        |          zero-shot          |         1          |     llama-3.1      |   0.56   |    0.63     | 0.61 |
| 104 |     detailed     |       fr        |          zero-shot          |         1          |     llama-3.1      |   0.52   |     0.6     | 0.62 |
| 105 |     detailed     |       en        |   few-shot (20 per class)   |        0.3         |     llama-3.1      |   0.46   |     0.5     | 0.51 |
| 107 |     detailed     |       fr        |   few-shot (20 per class)   |        0.3         |     llama-3.1      |   0.48   |    0.56     | 0.55 |
| 201 |     detailed     |       en        |          zero-shot          |         1          | mistral-large-2407 |   0.70   |    0.74     | 0.73 |
| 202 |     detailed     |       fr        |          zero-shot          |         1          | mistral-large-2407 |   0.72   |    0.76     | 0.75 |
| 204 |     detailed     |       fr        |          zero-shot          |         1          | mistral-small-2409 |   0.6    |    0.63     | 0.62 |
| 205 |     detailed     |       en        |          zero-shot          |         1          | mistral-small-2409 |   0.57   |    0.61     | 0.62 |
| 206 |     detailed     |       fr        | few-shot<br/>(20 per class) |         0.3<br/>stratified          | mistral-large-2407 |   0.69   |    0.73     | 0.73 |
| 207 |     detailed     |       en        | few-shot<br/>(20 per class) |         0.3<br/>stratified          | mistral-large-2407 |   0.68   |    0.73     | 0.73 |
| 208 |     detailed     |       fr        | few-shot<br/>(20 per class) |         0.3<br/>stratified          | mistral-small-2409 |   0.60   |    0.64     | 0.62 |
| 209 |     detailed     |       en        | few-shot<br/>(20 per class) |         0.3<br/>stratified          | mistral-small-2409 |   0.51   |    0.55     | 0.56 |
| 210 |     detailed     |       en        | few-shot<br/>(20 per class) |         0.3<br/>stratified          | mistral-small-2409 |   0.51   |    0.56     | 0.56 |

<a name="grouped-stgdir"></a>
##  Grouped prompts

We also tested prompts where, instead of asking to classify a single stage direction, the model is asked to classify a list of stage directions with the same prompt. The table below summarizes such results.

| id     | definition type | prompt language | stdir per prompt | example use |          data split           |        model         | macro F1 | weighted F1 |  acc  |  secs   | 
|--------|:--------:|:---------------:|:----------------:|:-----------:|:-----------------------------:|:--------------------:|:--------:|:-----------:|:-----:|:-------:|
| 303    | detailed |       en        |        10        |  zero-shot  |               1               |     gpt-4o-mini      |   0.60   |    0.66     | 0.64  |         |
| 304    | detailed |       en        |        10        |  zero-shot  |               1               |        gpt-4o        |   0.70   |    0.739    | 0.733 |         |
| 304    | detailed |       en        |        10        |  zero-shot  |               1               |        gpt-4o        |   0.70   |    0.739    | 0.733 |         |
| 305    | detailed |       en        |        10        |  zero-shot  |        0.3 stratified         |    mistral-large     |  0.648   |    0.703    | 0.706 |         |
| 306    | detailed |       en        |        10        |  zero-shot  |               1               |    mistral-large     |   0.69   |    0.726    | 0.726 | 5812.24 |
| 307    | detailed |       en        |        75        |  zero-shot  |               1               |        gpt-4o        |  0.696   |    0.745    | 0.735 | 2510.22 |
| 308    | detailed |       fr        |        75        |  zero-shot  |               1               |    mistral-large     |  0.708   |    0.74     | 0.736 | 5244.82 |
| 309    | detailed |       fr        |       100        |  zero-shot  |               1               |    mistral-large     |          |             |       |         |
| 310    | detailed |       fr        |       100        |  zero-shot  |               1               |    mistral-small     |          |             |       |         |
| 311    | detailed |       fr        |        75        |  few-shot   |       0.3<br>stratified       |    mistral-large     |  0.734   |    0.797    | 0.796 |         |
| 312    | detailed |       en        |        75        |  few-shot   |       0.3<br>stratified       |    mistral-large     |  0.717   |    0.761    | 0.759 |         |
| 313    | detailed |       en        |        75        |  few-shot   |       0.3<br>stratified       |        gpt-4o        |  0.765   |    0.826    | 0.818 | 973.99  |
| 314    | detailed |       fr        |        75        |  few-shot   |       0.3<br>stratified       |        gpt-4o        |  0.744   |    0.802    | 0.791 | 747.69  |
| 315    | detailed |       en        |        75        |  few-shot   |       0.3<br>stratified       | mistral-small-latest |  0.473   |    0.569    | 0.551 |  705.2  |
| 316    | detailed |       fr        |        75        |  few-shot   |       0.3<br>stratified       | mistral-small-latest |  0.525   |    0.608    | 0.597 |         |
| 317    | detailed |       en        |        75        |  zero-shot  |               1               |     gpt-4o-mini      |  0.623   |    0.676    | 0.676 |         |
| 318    | detailed |       en        |        75        |  few-shot   |       0.3<br>stratified       | mistral-small-latest |  0.472   |    0.548    | 0.555 |         |
| 319    | detailed |       fr        |        75        |  zero-shot  |               1               |     gpt-4o-mini      |  0.623   |    0.675    | 0.665 | 965.42  |
| 320    | detailed |       en        |        75        |  zero-shot  |               1               |    mistral-large     |  0.683   |    0.714    | 0.713 | 1278.86 |
| 321    | detailed |       fr        |        75        |  zero-shot  |               1               |        gpt-4o        |  0.691   |    0.742    | 0.732 | 1522.73 |
| 322    | detailed |       fr        |        75        |  zero-shot  |               1               |    mistral-small     |  0.616   |    0.692    | 0.686 | 1221.21 |
| 323    | detailed |       en        |        75        |  few-shot   |       0.3<br>stratified       |     gpt-4o-mini      |  0.705   |    0.764    | 0.753 |         |
| 324    | detailed |       fr        |        75        |  few-shot   |       0.3<br>stratified       |     gpt-4o-mini      |  0.724   |    0.76     | 0.753 | 380.65  |
| 325    | detailed |       fr        |        75        |  zero-shot  |               1               |    mistral-small     |   0.61   |    0.674    | 0.675 |         |
| 326    | detailed |       fr        |        75        |  few-shot   | 0.3<br>stratified<br>shuffled |     gpt-4o-mini      |  0.621   |    0.666    | 0.657 | 374.07  |
| 327    | detailed |       en        |        75        |  few-shot   | 0.3<br>stratified<br>shuffled |     gpt-4o-mini      |   0.65   |    0.707    | 0.700 | 312.11  |
| 328    | detailed |       en        |        75        |  few-shot   | 0.3<br>stratified<br>shuffled |        gpt-4o        |  0.729   |    0.788    | 0.78  | 312.11  |
| 329    | detailed |       fr        |        75        |  few-shot   | 0.3<br>stratified<br>shuffled |        gpt-4o        |  0.726   |    0.788    | 0.781 |         |
| 330    | detailed |       en        |        75        |  few-shot   | 0.3<br>stratified<br>shuffled |    mistral-small     |  0.526   |    0.606    | 0.602 |         |
| 331    | detailed |       en        |        75        |  few-shot   | 0.3<br>stratified<br>shuffled | mistral-small-latest |  0.592   |    0.66     | 0.652 |         |
| 332    | detailed |       fr        |        75        |  few-shot   | 0.3<br>stratified<br>shuffled |    mistral-large     |  0.707   |    0.728    | 0.727 |         |
| 333    | detailed |       en        |        75        |  few-shot   | 0.3<br>stratified<br>shuffled |    mistral-large     |  0.707   |    0.744    | 0.741 |       |


## Legend for the result summaries

### *Definition type* column

- **simple** definition: The prompt contains a short definition for each category. It may additionally contain examples or not, this is reflected in the `example use` column. 
- **detailed**: Besides a definition (which may provide some more detail than the *simple* type), the prompt contains a list of expressions that may be related to the category. These expressions are not direct examples of stage directions, they may be verbs or other expressions related to the vocabulary of the category's stage directions. The prompt may additionally contain examples or not, this is reflected in the `example use` column.

Note that, in all batches from 005 onwards, all prompts in English mention explicitly that the text to classify is in French. The reason for adding this information is the following: We asked the models to generate a text to "explain" each classification. In early batches, it was seen that `gpt-4o-mini` was interpreting some potentially ambiguous examples as English text. E.g. a case like "Evelyn sort" might get interpreted as English text, as a type of "sort" (a method for arranging things in a order), rather than as French text (inflected form of verb "sortir", for "exiting").

### *Data splits* column

- **1**: 100% of the testset (2923 examples) from [Schneider & Ruiz Fabo (2024)](https://aclanthology.org/2024.latechclfl-1.28/), available at https://nakala.fr/10.34847/nkl.fde37ug3.
- **0.3 stratified**: 30% of the testset, stratified by category.
- **0.3 stratified shuffled** means that examples were shuffled before creating the "grouped" prompts, which have > 1 stage direction to classify. This is because, in the 30% testset, examples for each category were sequential, and without shuffling this could be used as a clue by the model. This was not a problem when only having one stage direction in the prompt, as each API call is independent, but becomes a problem when you have more than one stage direction in the same prompt. In the 100% testset, examples for each category are not sequential, they had already been shuffled, so no extra shuffling is necessary. 