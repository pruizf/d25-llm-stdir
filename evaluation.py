"""Evaluating LLM-based classification (GPT and Mistral)"""

import argparse
from importlib import reload
import os
import random

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, confusion_matrix

import config as cf
import prompts as pr
import utils as ut

# constants
clrmap_dict = {"gpt-4o-mini": "Blues", "gpt-4o": "Greens",
               "mistral-large-latest": "BuGn", "mistral-small-latest": "PuBu"}
for ke in clrmap_dict:
  assert ke in cf.llm_list, f"Model {ke} not in {cf.llm_list}"

def plot_confusion_matrix(y_preds, y_true, labels, color_key, batch_sfx=None, normalize=None):
  cm = confusion_matrix(y_true, y_preds, normalize=normalize)
  fig, ax = plt.subplots(figsize=(6, 6))
  plt.grid(False)
  if False:
    font = {'family' : 'Arial',
      'weight' : 'bold',
      'size'   : 16}
    plt.rc('font', **font)
  #labels_for_fig = [l[0:4]+'.' for l in labels]
  labels_for_fig = labels
  disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                display_labels=labels_for_fig)
  #disp.plot(cmap="Purples", values_format=".2f", ax=ax, colorbar=False)
  if normalize:
    disp.plot(cmap=clrmap_dict[color_key], values_format=".2f", ax=ax, colorbar=False)
    norm_prefix = "Normalized "
    title_text = f"confusion matrix ({color_key})"
  else:
    disp.plot(cmap=clrmap_dict[color_key], ax=ax, colorbar=False)
    norm_prefix = ""
    title_text = f"Confusion matrix ({color_key})"
  #disp.plot(cmap=clrmap_dict[color_key], values_format=".2f", ax=ax, colorbar=False)
  ax.tick_params(axis='x', rotation=45)
  plt.xticks(ha='right')
  plt.title(f"{norm_prefix}{title_text}")
  #plt.show()
  out_fname = f"cm_{color_key}_{batch_sfx}.pdf" if batch_sfx is not None else f"cm_{color_key}.pdf"
  plt.savefig(os.path.join(cf.plot_dir.format(batch_id=args.batch_name), out_fname), format='pdf',
              bbox_inches='tight')


def eval_res(res_dir, golden_df, color_mode, prompt_type, batch_sfx=None):
  assert color_mode in clrmap_dict
  sys_jmt = ut.extract_category_from_model_output(res_dir, mode=prompt_type)
  #gold_df = pd.read_csv(golden_fn, sep=cf.sep_test)
  ref_jmt = golden_df['categNbr'].tolist()
  labels = cf.categs_as13
  classif_report = classification_report(ref_jmt, sys_jmt, target_names=labels, digits=3)
  plot_confusion_matrix(sys_jmt, ref_jmt, labels, color_mode, batch_sfx=batch_sfx, normalize="true")
  plain_cm = confusion_matrix(ref_jmt, sys_jmt, normalize="true")
  return {"sys_res": sys_jmt, "ref_res": ref_jmt, "cm": plain_cm, "cr": classif_report}


def eval_res_safe(res_dir, golden_df, color_mode, prompt_type,
                  group_size, data_size, batch_sfx=None, previous_categs=None):
  assert color_mode in clrmap_dict
  sys_jmt = ut.extract_category_from_model_output_safe(res_dir, group_size, data_size, mode=prompt_type)
  # also do dictionary here for ref_jmt, based on index as key, categNbr as labels
  ref_jmt = golden_df['categNbr'].to_dict()
  # now that both ref and sys results are indexed by stgdir number, compare to
  # figure out missing numbers. Fill inmissing numbers with a random category
  ref_stgdir_nbrs = set(ref_jmt.keys())
  sys_stgdir_nbrs = set(sys_jmt.keys())
  missing_stgdir_nbrs = ref_stgdir_nbrs - sys_stgdir_nbrs
  added_categs = {}
  for ms in missing_stgdir_nbrs:
    if ms in previous_categs:
      sys_jmt[ms] = previous_categs[ms]
      print(f"Missing stage direction {ms} filled with previous random category {previous_categs[ms]}")
      continue
    rand_choice = random.choice(cf.categs_as13)
    sys_jmt[ms] = cf.categs_as13.index(rand_choice)
    added_categs[ms] = cf.categs_as13.index(rand_choice)
    print(f"Missing stage direction {ms} filled with random category {rand_choice}")
  ref_jmt_as_list = [ref_jmt[stgdir] for stgdir in sorted(ref_jmt.keys())]
  sys_jmt_as_list = [sys_jmt[stgdir] for stgdir in sorted(sys_jmt.keys())]
  # actual evaluation
  labels = cf.categs_as13
  classif_report = classification_report(ref_jmt_as_list, sys_jmt_as_list, target_names=labels, digits=3)
  plot_confusion_matrix(sys_jmt_as_list, ref_jmt_as_list, labels, color_mode, batch_sfx=batch_sfx, normalize="true")
  plain_cm = confusion_matrix(ref_jmt_as_list, sys_jmt_as_list, normalize="true")
  return {"sys_res": sys_jmt_as_list, "ref_res": ref_jmt_as_list, "cm": plain_cm, "cr": classif_report,
          "added_categs": {}}


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Evaluation of LLM-based classification")
  parser.add_argument("batch_name", help="Batch name used as prefix on outputs")
  parser.add_argument("corpus", help="Corpus to run the model on")
  parser.add_argument("model", help="Model used for generating the response")
  parser.add_argument("run_mode", choices=["individual", "grouped"],
                      help="Whether prompt contained a single stage direction or several")
  parser.add_argument("--safe_eval", "-s", action="store_true",
                      help="Compares stage direction number in reference and results, "
                           "to account for cases where model skips some stage directions")
  args = parser.parse_args()
  assert args.model in cf.llm_list, f"Model {args.model} not in {cf.llm_list}"
  assert args.batch_name in os.listdir(cf.response_base_dir), f"Results for batch {args.batch_name} not available"
  assert args.batch_name.startswith("batch_"), "Batch name must start with 'batch_'"
  print(f"{args.batch_name}: Running [{args.model}] on [{args.corpus}]\n")

  # make sure to import updated modules
  for module in [cf, pr, ut, ut.catinfo]:
    reload(module)

  #IO
  if not os.path.exists(cf.plot_dir.format(batch_id=args.batch_name)):
    os.makedirs(cf.plot_dir.format(batch_id=args.batch_name))

  results_dir = cf.postpro_response_dir.format(batch_id=args.batch_name)
  corpus_sep = "\t" if "30" in args.corpus else ","
  golden = ut.get_and_format_data(args.corpus, corpus_sep)

  if args.safe_eval:
    # get last-added random categories for missing stage directions
    if os.path.exists(os.path.join("logs", f"added_categs_{args.batch_name}.txt")):
      with open(os.path.join("logs", f"added_categs_{args.batch_name}.txt"), "r") as in_ac:
        added_categs = in_ac.readlines()
        added_categs = {int(l.split("\t")[0].strip()): int(l.split("\t")[1].strip()) for l in added_categs}
    #TODO these arguments should be dynamic
    # read group size from results and data size from golden
    eval_data = eval_res_safe(results_dir, golden, args.model, args.run_mode,
                              10, 2923,
                              batch_sfx=args.batch_name.replace("batch_", ""))
    # log added categories to reuse later
    with open(os.path.join("logs", f"added_categs_{args.batch_name}.txt"), "w") as out_ac:
      for k, v in eval_data["added_categs"].items():
        out_ac.write(f"{k}\t{v}\n")
  else:
    eval_data = eval_res(results_dir, golden, args.model, args.run_mode, batch_sfx=args.batch_name.replace("batch_", ""))
  print(eval_data["cr"])
  print()
  with open(os.path.join(cf.plot_dir.format(batch_id=args.batch_name),
                         f"cr_{args.model}_{args.batch_name.replace('batch_', '')}.txt"), "w") as out_cr:
    out_cr.write(eval_data["cr"])
  #print(eval_data["cm"])
