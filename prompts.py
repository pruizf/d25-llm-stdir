"""Prompts for project"""

from importlib import reload

from data import category_info as catinfo
reload(catinfo)
import config as cf

categs_as13 = ["action", "aggression", "aparte", "delivery", "entrance",
               "exit", "interaction", "movement", "music",
               "narration", "object", "setting", "toward",]

def number_categories(clist):
  out = []
  for cat in clist:
    out.append(f"{clist.index(cat)}. {cat}")
  return "\n".join(out)


def get_category_info(cf, mode="fr"):
  if mode == "fr":
    return catinfo.cat_info_fr_only
  else:
    return catinfo.cat_info_fr_en

gen_promt = """
Classify the stage direction into one of the categories provided below it:

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
Classify the stage direction into one of the categories provided below it:

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

"""