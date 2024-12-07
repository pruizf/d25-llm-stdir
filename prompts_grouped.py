"""
Prompts for project, grouping several stage directions in the same prompt.
"""


gen_prompt = """
You will find below a numbered list of stage directions in French, within the <<<>>> signs. For each stage direction, classify it into one of the categories provided in the category list below the stage direction list:

<<<
Stage direction list:
{stdir}
>>>

###
Category list:
{numbered_categories}

To help classification, here is a definition for each category, along with some examples:
{category_details}
###

Provide a JSON response. Your response will contain a `result_list` element
with an entry for each stage direction in the list. Each entry will contain
the stage direction number, the number for the category that best fits
the stage direction type, and an explanation for your choice.
Response format will be as follows:

{{"result_list": [
  {{
    "stgdir_nbr": "stage direction number",
    "category": "category number",
    "explanation": "explanation for choice"
  }} ...
  ]
}}

Note that all stage directions are in French.

"""

prompt_def_only = """
You will find below a numbered list of stage directions in French, within the <<<>>> signs. For each stage direction, classify it into one of the categories provided in the category list below the stage direction list:

<<<
Stage direction list:
{stdir}
>>>

###
Category list:
{numbered_categories}

To help classification, here is a definition for each category:
{category_details}
###

Provide a JSON response. Your response will contain a `result_list` element
with an entry for each stage direction in the list. Each entry will contain
the stage direction number, the number for the category that best fits
the stage direction type, and an explanation for your choice.
Response format will be as follows:

{{"result_list": [
  {{
    "stgdir_nbr": "stage direction number",
    "category": "category number",
    "explanation": "explanation for choice"
  }} ...
  ]
}}

Note that all stage directions are in French.

"""

gen_prompt_fr = """
Vous trouverez ci-dessous une liste numérotée de didascalies en français, à l'intérieur des signes <<<>>>. Pour chaque didascalie, classez-la dans l'une des catégories fournies dans la liste de catégories située sous la liste de didascalies :

<<<
Liste de didascalies :
{stdir}
>>>

###
Liste des catégories :
{numbered_categories}

Pour vous aider à la classification, voici une définition de chaque catégorie avec quelques exemples :
{category_details}
###

Fournissez une réponse au format JSON. Votre réponse contiendra un élément nommé `result_list`. À l'intérieur de cet élément, il y aura une entrée pour chaque didascalie. Chaque entrée contiendra le numéro de la didascalie, le numéro de la catégorie qui correspond le mieux au type de la didascalie, ainsi qu'une explication de votre choix. Utilisez le format suivant :

{{"result_list": [
  {{
    "stgdir_nbr": "numéro de la didascalie",
    "category": "numéro de la catégorie",
    "explanation": "explication du choix"
  }} ...
  ]
}}

"""

prompt_def_only_fr = """
Vous trouverez ci-dessous une liste numérotée de didascalies en français, à l'intérieur des signes <<<>>>. Pour chaque didascalie, classez-la dans l'une des catégories fournies dans la liste de catégories située sous la liste de didascalies :

<<<
Liste de didascalies :
{stdir}
>>>

###
Liste des catégories :
{numbered_categories}

Pour vous aider à la classification, voici une définition de chaque catégorie:
{category_details}
###

Fournissez une réponse au format JSON. Votre réponse contiendra un élément nommé `result_list`. À l'intérieur de cet élément, il y aura une entrée pour chaque didascalie. Chaque entrée contiendra le numéro de la didascalie, le numéro de la catégorie qui correspond le mieux au type de la didascalie, ainsi qu'une explication de votre choix. Utilisez le format suivant :

{{"result_list": [
  {{
    "stgdir_nbr": "numéro de la didascalie",
    "category": "numéro de la catégorie",
    "explanation": "explication du choix"
  }} ...
  ]
}}

"""