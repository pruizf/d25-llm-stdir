# Stage direction classification in French theater with LLM
Pablo Ruiz Fabo & Alexia Schneider, Université de Strasbourg
# Repository structure

- Clients to run the LLM are:
  - `openai_client.py`
  - `llama_client.py`
- For each batch, they create an output directory in the `results` directory.
- Evaluation scripts are:
- `evaluate.py` for GPT-4 results
- `evaluate_llama.py` for Llama results
- Configuration options are in `config.py`
- Examples to classify are in `data`

# Usage

CLI options can be seen in the `argparse` options in the clients.

## Example
- The command `python openai_client.py batch_014 data/stgdir_labelGeneric_trainvalid_100-test.csv gpt-4o-mini def-few-shot en` does the following (CLI option listed in order):
  - Output is saved to `outputs/batch_014`
  - Examples to classify are in `data/stgdir_labelGeneric_trainvalid_100-test.csv`
  - The model is `gpt-4o-mini`
  - Prompting mode is `def-few-shot`, which uses a detailed definition for each category and 20 examples for each category. Allowed prompt modes are in ̀config.py`
  - The language for the category definitions is  ̀en` (possible values in `config.py`).

# Data

- The data, available at https://nakala.fr/10.34847/nkl.fde37ug3 are from [Schneider (2024)](https://nakala.fr/10.34847/nkl.3ecb73zp) and [Schneider & Ruiz Fabo (2024)](https://aclanthology.org/2024.latechclfl-1.28/)
- The complete test-set (2923 examples) is used run in zero-shot batches, and a 30% fraction, stratified by category, is run in few-shot batches.

# Prompts
- The prompts, in both English and French, are in `prompts.py`. The prompts are templates with several fields, filled dynamically by the client with category definitions in all settings and, additionally, some examples in the few-shot setting.
- Category definitions are in `data/category_info.py`.
- In the case of few-shot batches, the examples in `data/sampled_df_for_prompts_0001.tsv` are added to the prompt.

# Evaluation

- Script `evaluate.py` and `evaluate_llama.py` produce a classification report and confustion matrix for a batch, for GPT-4 and Llama 3.1 results respectively. Results are written to the `plots` directory in each batch's output directory.

# Result summary
| id  | prompt                               |   data<br/>split   | model  |       prompt<br/>mode       | macro<br/>F1 | weighted<br/>F1 | acc  |
|-----|--------------------------------------|:------------------:|--------|:---------------------------:|:------------:|:---------------:|:----:|
| 001 | general                              |         1          | gpt-4o-mini |          two-shot           |     0.48     |      0.53       | 0.52 |
| 002 | definition                           | 0.3<br/>stratified | gpt-4o-mini |          zero-shot          |     0.51     |      0.57       | 0.57 |
| 003 | definition + "verbs"                 | 0.3<br/>stratified | gpt-4o-mini |          zero-shot          |     0.53     |      0.59       | 0.57 |
| 004 | definition + "verbs"                 | 0.3<br/>stratified | gpt-4o |          zero-shot          |     0.7      |      0.73       | 0.72 |
| 005 | definition + "verbs" + fr            |         1          | gpt-4o |          zero-shot          |     0.71     |      0.74       | 0.73 |
| 006 | definition + "verbs" + fr            |         1          | gpt-4o-mini |          zero-shot          |     0.58     |      0.64       | 0.61 |
| 007 | general + fr                         | 0.3<br/>stratified | gpt-4o-mini | few-shot<br/>(20 per class) |     0.57     |      0.64       | 0.63 |
| 008 | general + "verbs" + fr               | 0.3<br/>stratified | gpt-4o-mini | few-shot<br/>(20 per class) |     0.58     |      0.65       | 0.67 |
| 009 | general + "verbs" + fr               | 0.3<br/>stratified | gpt-4o | few-shot<br/>(20 per class) |     0.73     |      0.79       | 0.78 |
| 010 | general + "verbs" + frPrompt         | 0.3<br/>stratified | gpt-4o-mini | few-shot<br/>(20 per class) |     0.62     |      0.70       | 0.69 |
| 011 | definition + "verbs" + frPrompt      |         1          | gpt-4o |          zero-shot          |     0.69     |      0.72       | 0.71 |
| 012 | definition + "verbs" + frPrompt      |         1          | gpt-4o-mini |          zero-shot          |     0.54     |      0.59       | 0.57 |
| 013 | general + "verbs" + frPrompt         |         1          | gpt-4o-mini | few-shot<br/>(20 per class) |     0.61     |      0.68       | 0.67 |
| 014 | general + "verbs" + fr               |         1          | gpt-4o-mini | few-shot<br/>(20 per class) |     0.6      |      0.67       | 0.67 |
| 015 | general + "verbs" + frPrompt         |         1          | gpt-4o | few-shot<br/>(20 per class) |     0.7      |      0.75       | 0.75 |
| 102 | definition + "verbs" + fr            |         1          | llama-3 |          zero-shot          |     0.43     |      0.52       | 0.49 |
| 103 | definition + "verbs" + fr            |         1          | llama-3.1 |          zero-shot          |     0.56     |      0.63       | 0.61 |
| 104 | definition + "verbs" + fr + frPrompt |         1          | llama-3.1 |          zero-shot          |     0.52     |       0.6       | 0.62 |
| 105 | general + "verbs" + fr               |        0.3         | llama-3.1 | few-shot<br/>(20 per class) |     0.46     |       0.5       | 0.51 |


## Meaning of "prompt" column
- **general**: Classification prompt with a short definition and a varying number of examples for each category.
- **definition**: A short definition is given for each category, without examples.
- **"verbs"**: A list of expressions (but not stage directions, not direct examples) that may be related to the category is given.
- **fr**: The prompt explicitly mentions that the text to classify is in French. The reasoning is that we asked the models to generate a text to "explain" each classification, and in some ambiguous cases like "Evelyn sort",gpt-4o-mini was interpreting the text as English (as a way of "sorting" something) instead of French (as someone exiting).
- **frPrompt**: The prompt is written in French. It is thus no longer mentioned that the examples to classify are in French.

## Data splits

- **1**: 100% of the testset (2923 examples) from [Schneider & Ruiz Fabo (2024)](https://aclanthology.org/2024.latechclfl-1.28/), available at https://nakala.fr/10.34847/nkl.fde37ug3.
- **0.3 stratified**: 30% of the testset, stratified by category.
