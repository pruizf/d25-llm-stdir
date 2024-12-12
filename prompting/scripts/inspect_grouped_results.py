"""
Verifications on results per group (given mismatch between reference and result number seen with Mistral)
"""

import argparse
from importlib import reload
import json
import os

import config as cf
import utils as ut

import pandas as pd


if __name__ == "__main__":
  for modu in [cf, ut]:
    reload(modu)

  parser = argparse.ArgumentParser(description="Inspecting results")
  parser.add_argument("batch_name", help="Batch name used as prefix on outputs")
  parser.add_argument("corpus", help="Corpus to run the model on")
  args = parser.parse_args()

  res_dir = cf.postpro_response_dir.format(batch_id=args.batch_name)
  corpus_sep = "\t" if "30" in args.corpus else ","
  stdirs = ut.get_and_format_data(args.corpus, corpus_sep)

  for fname in sorted(os.listdir(res_dir)):
    ffname = os.path.join(res_dir, fname)
    with open (ffname, "r") as f:
      res = json.load(f)
      if len(res["result_list"]) != 10:
        print(f"- {fname}: {len(res['result_list'])} results")
        missing_idx = ut.find_missing_numbers(
          [int(resit["stgdir_nbr"]) for resit in res["result_list"]])
        print("\n  - Missing idx: ".join([str(x) for x in missing_idx]))

