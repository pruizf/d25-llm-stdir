"""
Given a result batch and a category, sort results into errors and matches, for qualitative analysis.
"""

import argparse
import json
import os
from typing import List, Dict, Tuple

import pandas as pd

import config as cf


def ana_batch_results(ref: pd.DataFrame, batch_id: int, category_pair: tuple) -> Tuple[List[Dict], List[Dict]]:
  """
  Analyze the results of a batch.

  Args:
      ref (pd.DataFrame): reference data
      batch_id (int): batch ID
      category_pair (tuple): reference and predicted category labels

  Returns:
      tuple: list of dicts with data for matching results, list of dicts with data for errors
  """
  batch_data_match = []
  batch_data_error = []
  if category_pair[1] is None:
    cat_pair_as_int = (cf.categs_as13.index(category_pair[0]), None)
  else:
    cat_pair_as_int = tuple(cf.categs_as13.index(cat) for cat in category_pair)
  # filter reference data to include only the selected category
  selrows = ref[ref["label"] == cat_pair_as_int[0]]
  for idx, row in selrows.iterrows():
    # get reference data
    st_txt = row["text"]
    label_num = row["label"]
    label_str = cf.categs_as13[label_num]
    # get predicted data
    res_dir = cf.postpro_response_dir.format(batch_id=f"batch_{batch_id}")
    res_fn = [fname for fname in os.listdir(res_dir) if f"_{str.zfill(str(idx), 4)}_" in fname]
    assert len(res_fn) == 1, f"Expected 1 result file for stage direction {idx}, found {len(res_fn)}"
    with open(os.path.join(res_dir, res_fn[0]), "r") as res_f:
      res_data = json.load(res_f)
    pred_label_num = int(res_data["category"])
    pred_label_str = cf.categs_as13[pred_label_num]
    if category_pair[1] is not None:
      if pred_label_num != cat_pair_as_int[1]:
        continue
    text_in_res = res_data["stgdir"]
    assert st_txt.strip().lower() == text_in_res.strip().lower(), f"Text mismatch for stage direction {idx}"
    res_type = "match" if label_num == pred_label_num else "error"
    res_data = {
      "id": idx,
      "text": st_txt,
      "ref_num": label_num,
      "ref": label_str,
      "pred_num": pred_label_num,
      "pred": pred_label_str,
      "type": res_type,
      "explanation": res_data["explanation"]
    }
    if res_type == "match":
      batch_data_match.append(res_data)
    else:
      batch_data_error.append(res_data)
  return batch_data_match, batch_data_error


def write_out_results(data: List[Dict], batch_id: int, out_file: str, mode="w"):
  """
  Write out the analysis results.

  Args:
      data (List[Dict]): list of dicts with data
      batch_id (int): batch ID
      out_file (str): output file name
      mode (str): write mode (default: "w"), can be "a" for append
  """
  # add the sorting (by cat and then by row id
  open_mode = "a" if mode == "a" else "w"
  with open(out_file, open_mode) as out_f:
    out_f.write(f"# Batch {batch_id}\n\n")
    for res in sorted(data, key=lambda x: (x["ref_num"], x["pred_num"], x["id"])):
      out_f.write(f"## {str.zfill(str(res['id']), 4)} [{res['type']}]\n")
      out_f.write(f"  - REF;PRD: {res['ref']} ; {res['pred']}\n")
      out_f.write(f"  - TXT: {res['text']}\n")
      out_f.write(f"  - XPL: {res['explanation']}\n")
      out_f.write("\n")


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Qualitative result analysis")
  parser.add_argument("batch_id", help="Batch ID")
  parser.add_argument("reference_category", help="Category in reference set")
  parser.add_argument("--predicted_category", help="Category in system results")
  args = parser.parse_args()

  # IO and config
  ref_df = pd.read_csv(cf.testset_file)
  categ_to_ana = args.reference_category
  categ_pred_to_ana = args.predicted_category if args.predicted_category else None

  # ana results
  batch_ok, batch_err = ana_batch_results(ref_df, args.batch_id, (categ_to_ana, categ_pred_to_ana))

  # write out results
  out_fname = os.path.join(cf.ana_dir, f"ana_batch_{args.batch_id}.md")
  write_out_results(batch_err, args.batch_id, out_fname)
  write_out_results(batch_ok, args.batch_id, out_fname, mode="a")
