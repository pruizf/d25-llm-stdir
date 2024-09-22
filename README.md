# Batches

| id  | prompt                        |      data fraction | model       | promptMode | macro-F1 | acc  |
|-----|-------------------------------|-------------------:|-------------|------------|:--------:|:----:|
| 001 | general                       |                  1 | gpt-4o-mini | two-shot   |   0.48   | 0.52 |
| 002 | definition                    | 0.3<br/>stratified | gpt-4o-mini | zero-shot  |   0.51   | 0.57 |
| 003 | definition + "verbs"          | 0.3<br/>stratified | gpt-4o-mini | zero-shot  |   0.53   | 0.57 |
| 004 | definition + "verbs"          | 0.3<br/>stratified | gpt-4o      | zero-shot  |   0.7    | 0.72 |
| 005 | definition + "verbs" + French |                  1 | gpt-4o      | zero-shot  |   0.71   | 0.73 |
| 006 | definition + "verbs" + French |                  1 | gpt-4o-mini | zero-shot  |   0.58   | 0.61 |
| 102 | definition + "verbs" + French |                  1 | llama-3     | zero-shot  |   0.43   | 0.49 |
| 103 | definition + "verbs" + French |                  1 | llama-3.1   | zero-shot  |   0.56   | 0.61 |


- 001: General prompt, two to three-shot, 100% testset, gpt-4o-mini
- 002: Definition only prompt (zero shot), 0.3 frac (stratified), gpt-4o-mini.
- 003: Definition only prompt (zero shot) but gives a list of expressions (not stage directions) that may be related to the category, 0.3 frac (stratified), gpt-4o-mini
- 004: Definition only prompt (zero shot) but gives a list of expressions (not stage directions) that may be related to the category, 0.3 frac (stratified), gpt-4o
- 005: Definition only prompt (zero shot) but gives a list of expressions (not stage directions) that may be related to the category and explicitly mentions that they are in French, 100% of testset, gpt-4o
- 006: Definition only prompt (zero shot) but gives a list of expressions (not stage directions) that may be related to the category and explicitly mentions that they are in French, 100% of testset, gpt-4o-mini
- 102: Definition only prompt (zero shot) but gives a list of expressions (not stage directions) that may be related to the category and explicitly mentions that they are in French, 100% of testset, llama-3-8B-Instruct
- 103: Definition only prompt (zero shot) but gives a list of expressions (not stage directions) that may be related to the category and explicitly mentions that they are in French, 100% of testset, llama-3.1-8B-Instruct. Uses 2 Quadro RTX 5000 GPUs, ca. 32GB.

