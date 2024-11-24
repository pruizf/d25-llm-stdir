from copy import copy
import json
import os
import re

import pandas as pd

from data import category_info as catinfo
import config as cf


# DATA PREPARATION ------------------------------------------------------------
def get_and_format_data(fname, sep, label_type="number"):
  """
  Get and format the stage directions and labels from dataframe.

  Returns:
      pandas.DataFrame: The formatted data.
  """
  assert label_type in ["number", "string"], "label_type must be 'number' or 'string'"
  df = pd.read_csv(fname, sep=sep)
  df = df.dropna()
  df.columns = ["stgdir", "categ"]
  if label_type == "number":
    df['categNbr'] = df['categ']
  else:
    #df['categNbr'] = df['categ'].apply(lambda x: cf.categs_as13.index(x) + 1)
    df['categNbr'] = df['categ'].apply(lambda x: cf.categs_as13.index(x))
  return df

def sample_dataframe(df, category_col, frac=0.3):
    """
    Randomly sample 30% of rows for each category in the dataframe.

    Args:
        df (pd.DataFrame): The input dataframe.
        category_col (str): The name of the column with category labels.
        frac (float): The fraction of rows to sample for each category.

    Returns:
        pd.DataFrame: The sampled dataframe.
    """
    sampled_df = df.groupby(category_col).apply(lambda x: x.sample(frac=frac)).reset_index(drop=True)
    return sampled_df


# PROMPT DEVELOPMENT ----------------------------------------------------------

def number_categories(clist):
  """
  Output a list of category labels as a numbered list,
  based on the index for the category in the list
  """
  out = []
  for cat in clist:
    out.append(f"{clist.index(cat)}. {cat}")
  return "\n".join(out)


def get_category_info_two_shot(mode="fr"):
  """
  Get the category information to include in the prompt.
  This function is only used with the two-shot classification mode,
  the other modes get this part of the prompt with other means.
  """
  if mode == "fr":
    return catinfo.two_shot_fr
  else:
    return catinfo.two_shot_fr_en


def sample_examples_per_category(df_fn, n=20):
  """
  Sample n examples for each category in the dataframe.
  Args:
    df_fn (str): Path to the input dataframe.
    n (int): The number of examples to sample for each category.
  Returns:
    pd.DataFrame: The sampled dataframe.
  """
  sep = "\t" if "30" in df_fn else "|" if "woDuplicates" in df_fn else ","
  df = pd.read_csv(df_fn, sep=sep)
  df.columns = ["stgdir", "label"]
  df_sampled = df.groupby('label', group_keys=False).apply(lambda x: x.sample(min(len(x), n)))
  if not os.path.exists(cf.sampled_df_for_prompts):
    df_sampled.to_csv(cf.sampled_df_for_prompts, sep="\t", index=False)
  return df_sampled


def format_examples_for_few_shot_prompt(sampled_df_fn, lang):
  """
  Formats the examples for the few-shot prompt as follows:
  `    - text for the example // Category | Catégorie: label`
  Args:
    sampled_df_fn (str): The path to the sampled dataframe.
    lang (str): The language of the examples to choose the category indicator.
  Returns:
    dict: A dictionary with strings `example_n`, where `n` is the int category label
    as key and the formatted examples as value. The keys are then used to populate
    the prompt template in the client calling this function.
  """
  out_dict = {}
  sampled_df = pd.read_csv(sampled_df_fn, sep="\t")
  for idx, row in sampled_df.iterrows():
    label_key = f"examples_{row['label']}"
    out_dict.setdefault(label_key, [])
    cat_indicator = "Category" if lang == "en" else "Catégorie"
    out_dict[label_key].append(f"{row['stgdir']} // {cat_indicator}: {row['label']}")
  for ke, va in out_dict.items():
    out_dict[ke] = "    - " + "\n    - ".join(va)
  return out_dict


# EVALUATION ------------------------------------------------------------------

def extract_category_from_openai_output(resdir, mode="individual"):
  """
  Get OpenAI classification results into a list. Assumes that the response files
  contain a JSON field "category" with the category number.
  """
  assert mode in ["individual", "grouped"], "mode must be 'individual' or 'grouped'"
  all_res = []
  for fn in sorted(os.listdir(resdir)):
    if "response" not in fn:
      continue
    with open(os.path.join(resdir, fn), "r") as f:
      jo = json.load(f)
      if mode == "individual":
        all_res.append(int(jo["category"]))
      else:
        for result in jo["result_list"]:
          all_res.append(int(result["category"]))
  return all_res


def extract_category_from_llama_output(res_dir):
  """
  Extract the category number from the output of the Llama model.
  Args:
    res_dir (str): The directory with the response files.
  Returns:
    list: The list of category numbers.
  """
  categs = []
  for idx, fn in enumerate(sorted(os.listdir(res_dir))):
    if "response" in fn:
      with open(os.path.join(res_dir, fn), "r") as f:
        res = json.load(f)
        # sometimes the number is in quotation marks
        catnbr = re.search(r'category":\s[\'"]?(\d+)[\'"]?', res[0]["generated_text"][-1]["content"])
        assert catnbr, f"Category number not found in response for item {str.zfill(str(idx), 4)}"
        categs.append(int(catnbr.group(1)))
  return categs


def classification_results_to_df(resdir):
  """
  Get classification results into a dataframe.
  """
  all_lines = []
  for fn in sorted(os.listdir(resdir)):
    if "response" not in fn:
      continue
    with open(os.path.join(resdir, fn), "r") as f:
      jo = json.load(f)
      all_lines.append([jo["stgdir"], jo["category"]])
  return pd.DataFrame(all_lines, columns=["stgdir", "categNbr"])

# Manual analyses ---------------------
def add_category_names(df, categ_dict=cf.categ_col_map):
  """
  Given a dataframe where categories are expressed as numbers
  and a dictionary with the column names containing those categories,
  add a new column where the category names are expressed as strings,
  based on the category name list (in `config.py`).
  The numbers are indices for that list.
  """
  df_new = copy(df)
  for idx, (ke, va) in enumerate(categ_dict.items()):
    if ke not in df.columns:
      continue
    ke_idx = df.columns.get_loc(ke)
    df_new.insert(ke_idx + 1 + idx, va, None)
    df_new[va] = df_new[ke].apply(lambda x: cf.categs_as13[x])
  return df_new

def add_category_numbers(df, categ_dict=cf.categ_col_map):
  """
  Given a dataframe where categories are expressed as strings
  and a dictionary with the column names containing those categories,
  add a new column where the category names are expressed as a numbers,
  based on the index for the category name in the list at `config.py`.
  """
  df_new = copy(df)
  for idx, (ke, va) in enumerate(categ_dict.items()):
    breakpoint()
    if ke not in df.columns:
      continue
    ke_idx = df.columns.get_loc(ke)
    df_new.insert(ke_idx, va, None)
    df_new[va] = df_new[ke].apply(lambda x: cf.categs_as13.index(x))
  return df_new