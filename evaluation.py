"""Evaluating LLM-based classification"""

from importlib import reload
import os

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, confusion_matrix

import config as cf
import prompts as pr
import utils as ut

# constants
clrmap_dict = {"gpt-4o-mini": "Greens", "gpt-4o": "Blues"}

def plot_confusion_matrix(y_preds, y_true, labels, color_key,
                          batch_sfx=None, normalize=None):
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
    title_text = f"confusion matrix ({cf.oai_models[0]})"
  else:
    disp.plot(cmap=clrmap_dict[color_key], ax=ax, colorbar=False)
    norm_prefix = ""
    title_text = f"Confusion matrix ({cf.oai_models[0]})"
  #disp.plot(cmap=clrmap_dict[color_key], values_format=".2f", ax=ax, colorbar=False)
  ax.tick_params(axis='x', rotation=45)
  plt.xticks(ha='right')
  plt.title(f"{norm_prefix}{title_text}")
  #plt.show()
  out_fname = f"cm_{color_key}_{batch_sfx}.pdf" if batch_sfx is not None else f"cm_{color_key}.pdf"
  plt.savefig(os.path.join(cf.plot_dir, out_fname), format='pdf',
              bbox_inches='tight')


def eval_res(res_dir, golden_df, color_mode, batch_sfx=None):
  assert color_mode in clrmap_dict
  sys_jmt = ut.get_judgement_info_for_dir(res_dir)
  #gold_df = pd.read_csv(golden_fn, sep=cf.sep_test)
  ref_jmt = golden_df['categNbr'].tolist()
  labels = pr.categs_as13
  classif_report = classification_report(ref_jmt, sys_jmt, target_names=labels)
  plot_confusion_matrix(sys_jmt, ref_jmt, labels, color_mode, batch_sfx=batch_sfx, normalize="true")
  plain_cm = confusion_matrix(ref_jmt, sys_jmt, normalize="true")
  return {"sys_res": sys_jmt, "ref_res": ref_jmt, "cm": plain_cm, "cr": classif_report}


if __name__ == "__main__":
  # make sure to import updated modules
  for module in [cf, pr, ut, pr.catinfo]:
    reload(module)

  #IO
  if not os.path.exists(cf.plot_dir):
    os.makedirs(cf.plot_dir)

  results_dir = cf.postpro_response_dir.format(batch_id=cf.batch_id)
  golden = ut.get_and_format_data("testset")

  eval_data = eval_res(results_dir, golden, cf.oai_models[0], batch_sfx=cf.batch_id.replace("batch_", ""))
  print(eval_data["cr"])
  print()
  with open(os.path.join(cf.plot_dir, f"cr_{cf.oai_models[0]}_{cf.batch_id.replace('batch_', '')}.txt"), "w") as out_cr:
    out_cr.write(eval_data["cr"])
  #print(eval_data["cm"])
