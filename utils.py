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