from copy import copy
import json
import os
import re

import pandas as pd

import config as cf
import prompts as pr

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
    #df['categNbr'] = df['categ'].apply(lambda x: pr.categs_as13.index(x) + 1)
    df['categNbr'] = df['categ'].apply(lambda x: pr.categs_as13.index(x))
  return df


def get_judgement_info_for_dir(resdir):
  all_res = []
  for fn in sorted(os.listdir(resdir)):
    if not "response" in fn:
      continue
    with open(os.path.join(resdir, fn), "r") as f:
      jo = json.load(f)
      all_res.append(int(jo["category"]))
  return all_res


def judgement_info_to_df(resdir):
  all_lines = []
  for fn in sorted(os.listdir(resdir)):
    if not "response" in fn:
      continue
    with open(os.path.join(resdir, fn), "r") as f:
      jo = json.load(f)
      all_lines.append([jo["stgdir"], jo["category"]])
  return pd.DataFrame(all_lines, columns=["stgdir", "categNbr"])

def add_category_names(df, categ_dict):
  """
  Given a dataframe where categories are expressed as numbers
  and a dictionary with the column names containing those categories,
  add a new column where the category names are expressed as strings,
  based on the category name list (in `prompts.py`).
  The numbers are indices for that list.
  """
  df_new = copy(df)
  for idx, (ke, va) in enumerate(categ_dict.items()):
    if not ke in df.columns:
      continue
    ke_idx = df.columns.get_loc(ke)
    df_new.insert(ke_idx + 1 + idx, va, None)
    df_new[va] = df_new[ke].apply(lambda x: pr.categs_as13[x])
  #df_new.columns = cf.categ_col_order
  return df_new

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


def extract_category_from_llama_output(res_dir):
  """
  Extract the category number from the output of the Llama model.
  """
  categs = []
  for idx, fn in enumerate(sorted(os.listdir(res_dir))):
    if "response" in fn:
      with open(os.path.join(res_dir, fn), "r") as f:
        res = json.load(f)
        #catnbr = re.search(r'category":\s(\d+)', res[0][-2]["generated_text"][-1]["content"])
        # sometimes the number is in quotation marks
        catnbr = re.search(r'category":\s[\'"]?(\d+)[\'"]?', res[0]["generated_text"][-1]["content"])
        assert catnbr, f"Category number not found in response for item {str.zfill(str(idx), 4)}"
        categs.append(int(catnbr.group(1)))
  return categs
  # return llama_output[0]["generated_text"][-1]["category"]