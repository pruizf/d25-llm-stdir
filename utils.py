import pandas as pd

import config as cf
import prompts as pr

def get_and_format_data():
  """
  Get and format the data for the project.

  Returns:
      pandas.DataFrame: The formatted data.
  """
  df = pd.read_csv(cf.corpus_file, sep=cf.sep)
  df = df.dropna()
  df.columns = ["stgdir", "categ"]
  df['categNbr'] = df['categ'].apply(lambda x: pr.categs_as13.index(x) + 1)
  return df