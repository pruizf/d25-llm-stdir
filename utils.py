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
