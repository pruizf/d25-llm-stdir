"""Prompts for project"""


gen_prompt = """
Classify the following stage direction in French into one of the categories provided below it:

Stage direction: {stdir} 

Category list:
{numbered_categories}

To help classification, here is a definition for each category along with some examples:
{category_details}

Provide a JSON response. In your response, provide the number for the category that
best fits the stage direction type, and an explanation for your choice,
using the following format:

{{
  "category": "number",
  "explanation": "explanation for choice"
}}

Express your confidence in your response in a 0 to 1 scale, where 1 is the most confident, output this
in the same JSON object as the category and explanation, using the key "confidence".

Note that all stage directions are in French.

"""

prompt_def_only = """
Classify the following stage direction in French into one of the categories provided below it:

Stage direction: {stdir} 

Category list:
{numbered_categories}

To help classification, here is a definition for each category:
{category_details}

Provide a JSON response. In your response, provide the number for the category that
best fits the stage direction type, and an explanation for your choice,
using the following format:

{{
  "category": "number",
  "explanation": "explanation for choice"
}}

Express your confidence in your response in a 0 to 1 scale, where 1 is the most confident, output this
in the same JSON object as the category and explanation, using the key "confidence".

Note that all stage directions are in French.

"""

gen_prompt_fr = """
Classifiez la didascalie suivante dans l'une des catégories fournies ci-dessous :

Didascalie : {stdir}

Liste des catégories :
{numbered_categories}

Pour vous aider à la classification, voici une définition de chaque catégorie avec quelques exemples :
{category_details}

Fournissez une réponse au format JSON. Dans votre réponse, indiquez le numéro de la catégorie qui correspond le mieux au type de didascalie, ainsi qu'une explication de votre choix, en utilisant le format suivant :

{{
  "category": "numéro de la catégorie",
  "explanation": "explication du choix"
}}

Exprimez votre confiance dans votre réponse sur une échelle de 0 à 1, où 1 est le niveau de confiance le plus élevé, et indiquez-le dans le même objet JSON avec la clé "confidence".

"""

prompt_def_only_fr = """
Classifiez la didascalie suivante dans l'une des catégories fournies ci-dessous :

Didascalie : {stdir}

Liste des catégories :
{numbered_categories}

Pour vous aider à la classification, voici une définition de chaque catégorie:
{category_details}

Fournissez une réponse au format JSON. Dans votre réponse, indiquez le numéro de la catégorie qui correspond le mieux au type de didascalie, ainsi qu'une explication de votre choix, en utilisant le format suivant :

{{
  "category": "numéro de la catégorie",
  "explanation": "explication du choix"
}}

Exprimez votre confiance dans votre réponse sur une échelle de 0 à 1, où 1 est le niveau de confiance le plus élevé, et indiquez-le dans le même objet JSON avec la clé "confidence".

"""