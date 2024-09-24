# Batches

## Summary of results
| id  | prompt                               |  data<br/>fraction  | model       |       prompt<br/>mode       | macro<br/>F1 | weighted<br/>F1 | acc  |
|-----|--------------------------------------|:-------------------:|-------------|:---------------------------:|:------------:|:---------------:|:----:|
| 001 | general                              |          1          | gpt-4o-mini |          two-shot           |     0.48     |      0.53       | 0.52 |
| 002 | definition                           | 0.3<br/>stratified  | gpt-4o-mini |          zero-shot          |     0.51     |      0.57       | 0.57 |
| 003 | definition + "verbs"                 | 0.3<br/>stratified  | gpt-4o-mini |          zero-shot          |     0.53     |      0.59       | 0.57 |
| 004 | definition + "verbs"                 | 0.3<br/>stratified  | gpt-4o      |          zero-shot          |     0.7      |      0.73       | 0.72 |
| 005 | definition + "verbs" + fr            |          1          | gpt-4o      |          zero-shot          |     0.71     |      0.74       | 0.73 |
| 006 | definition + "verbs" + fr            |          1          | gpt-4o-mini |          zero-shot          |     0.58     |      0.64       | 0.61 |
| 007 | general + fr                         | 0.3<br/>stratified  | gpt-4o-mini | few-shot<br/>(20 per class) |     0.57     |      0.64       | 0.63 |
| 008 | general + "verbs" + fr               | 0.3<br/>stratified  | gpt-4o-mini | few-shot<br/>(20 per class) |     0.58     |      0.65       | 0.67 |
| 009 | general + "verbs" + fr               | 0.3<br/>stratified  | gpt-4o      | few-shot<br/>(20 per class) |     0.73     |      0.79       | 0.78 |
| 010 | general + "verbs" + frPrompt         | 0.3<br/>stratified  | gpt-4o-mini | few-shot<br/>(20 per class) |     0.62     |      0.70       | 0.69 |
| 011 | definition + "verbs" + frPrompt      | 1 | gpt-4o      |          zero-shot          |     0.69     |      0.72       | 0.71 |
| 012 | definition + "verbs" + frPrompt      | 1 | gpt-4o-mini |          zero-shot          |     0.54     |      0.59       | 0.57 |
| 013 | general + "verbs" + frPrompt      | 1 | gpt-4o-mini | few-shot<br/>(20 per class) |     0.61     |      0.68       | 0.67 |
| 014 | general + "verbs" + fr      | 1 | gpt-4o-mini | few-shot<br/>(20 per class) |     0.6      |      0.67       | 0.67 |
| 102 | definition + "verbs" + fr            |          1          | llama-3     |          zero-shot          |     0.43     |      0.52       | 0.49 |
| 103 | definition + "verbs" + fr            |          1          | llama-3.1   |          zero-shot          |     0.56     |      0.63       | 0.61 |
| 104 | definition + "verbs" + fr + frPrompt |          1          | llama-3.1   |          zero-shot          |     0.52     |       0.6       | 0.62 |


## Meaning of "prompt" column
- **general**: Classification prompt with a short definition and a varying number of examples for each category.
- **definition**: A short definition is given for each category, without examples.
- **"verbs"**: A list of expressions (but not stage directions, not direct examples) that may be related to the category is given.
- **fr**: The prompt explicitly mentions that the text to classify is in French. The reasoning is that we asked the models to generate a text to "explain" each classification, and in some ambiguous cases like "Evelyn sort",gpt-4o-mini was interpreting the text as English (as a way of "sorting" something) instead of French (as someone exiting).
- **frPrompt**: The prompt is written in French. This makes it superfluous to mention that the text to classify is in French.

## Data fractions

- **1**: 100% of the testset (2923 examples) from [Schneider & Ruiz Fabo (2024)](https://aclanthology.org/2024.latechclfl-1.28/), available at https://nakala.fr/10.34847/nkl.fde37ug3.
- **0.3 stratified**: 30% of the testset, stratified by category.

## Notes about some of the batches

- 001: General prompt, two to three-shot, 100% testset, gpt-4o-mini
- 002: Definition only prompt (zero shot), 0.3 frac (stratified), gpt-4o-mini.
- 003: Definition only prompt (zero shot) but gives a list of expressions (not stage directions) that may be related to the category, 0.3 frac (stratified), gpt-4o-mini
- 004: Definition only prompt (zero shot) but gives a list of expressions (not stage directions) that may be related to the category, 0.3 frac (stratified), gpt-4o
- 005: Definition only prompt (zero shot) but gives a list of expressions (not stage directions) that may be related to the category and explicitly mentions that they are in French, 100% of testset, gpt-4o
- 006: Definition only prompt (zero shot) but gives a list of expressions (not stage directions) that may be related to the category and explicitly mentions that they are in French, 100% of testset, gpt-4o-mini
- 007: General prompt with a short definition for each category and 20 examples for each. Explicitly mentions that text to classify is in French, 0.3 frac, stratified, gpt-4o-mini
- 102: Definition only prompt (zero shot) but gives a list of expressions (not stage directions) that may be related to the category and explicitly mentions that they are in French, 100% of testset, llama-3-8B-Instruct
- 103: Definition only prompt (zero shot) but gives a list of expressions (not stage directions) that may be related to the category and explicitly mentions that they are in French, 100% of testset, llama-3.1-8B-Instruct. Uses 2 Quadro RTX 5000 GPUs (ca. 32GB) from Unistra HPC.
- 104: Tesla V100 32G at Unistra HPC
