from copy import copy
import json
import os

import pandas as pd

import config as cf
import prompts as pr

def get_and_format_data(mode="testset"):
  """
  Get and format the data for the project.

  Returns:
      pandas.DataFrame: The formatted data.
  """
  fname = cf.testset_file if mode == "testset" else cf.corpus_file
  sep = cf.sep_test if mode == "testset" else cf.sep
  df = pd.read_csv(fname, sep=sep)
  df = df.dropna()
  df.columns = ["stgdir", "categ"]
  if mode == "testset":
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
