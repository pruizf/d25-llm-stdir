"""
Get tokens and response times for the batches based on the completion object info.
"""

import argparse
from datetime import datetime
from importlib import reload
import json
import os
import re
import time

import pandas as pd

import config as cf


if __name__ == "__main__":
  # make sure to import updated modules
  for module in [cf]:
    reload(module)

  parser = argparse.ArgumentParser(description="Obtain some stats about results")
  parser.add_argument("out_sfx",
                      choices=cf.stat_suffixes,
                      help="Suffix for the output file")
  args = parser.parse_args()

  # Get ids for batches to
  batch_ids_to_types = {}
  with open(cf.batches_for_stats, "r") as in_bs:
    for line in in_bs:
      if line.startswith("#") or not len(line.strip()):
        continue
      batch_id, batch_type, lg = line.strip().split("|")
      batch_ids_to_types[batch_id] = {"b_type": batch_type, "lang": lg}

  data = {"batch_id": [],
          "batch_type": [],
          "language": [],
          "model_name": [],
          "prompt_tokens": [],
          "completion_tokens": [],
          "total_tokens": [],
          "mean_tokens_per_completion": [],
          "response_time": [],
          "mean_response_time_per_completion": []}

  for b_id, b_infos in sorted(batch_ids_to_types.items()):
    print(f"# Start batch: {b_id} {datetime.now().strftime('%H:%M:%S')}")
    completions_dir = cf.completions_dir.format(batch_id=b_id)
    postpro_response_dir = cf.postpro_response_dir.format(batch_id=b_id)
    # store per batch data here, to aggregate later before writing to dataframe
    prompt_tokens_for_batch = []
    completion_tokens_for_batch = []
    total_tokens_for_batch = []
    response_times_for_batch = []
    # go through completions and postpro responses
    for idx, fn in enumerate(sorted(os.listdir(completions_dir))):
      with open(os.path.join(completions_dir, fn), "r") as infi:
        #TODO why double?
        jso = json.loads(json.load(infi))
      if idx == 0:
        if "gpt" in jso["model"]:
          model_name = re.sub(r"-\d{2}.*", "", jso["model"])
          print(f"  - Renaming model from {jso['model']} to {model_name}")
        else:
          model_name = jso["model"]
        print(f"  - Model: {model_name}")
      prompt_tokens = jso["usage"]["prompt_tokens"]
      completion_tokens = jso["usage"]["completion_tokens"]
      total_tokens = jso["usage"]["total_tokens"]
      prompt_tokens_for_batch.append(prompt_tokens)
      completion_tokens_for_batch.append(completion_tokens)
      total_tokens_for_batch.append(total_tokens)
      # go over the postpro files to get response times
      postpro_file = sorted(os.listdir(postpro_response_dir))[idx]
      if model_name in cf.model_name_mappings:
        model_name_orig = model_name
        model_name = cf.model_name_mappings[model_name]
        print(f"  - Renaming model from {model_name_orig} to {model_name}")
      fcount_from_fn = re.match(fr".+_(\d+)_{model_name}.json", postpro_file)
      try:
        assert fcount_from_fn, f"File name format mismatch: {postpro_file}"
      except AssertionError as e:
        print("  - Error: ", e, "Model name: ", model_name)
        print(f"  - Trying to match file name with model name [{model_name_orig}] ")
        fcount_from_fn = re.match(fr".+_(\d+)_{model_name_orig}.json", postpro_file)
      assert idx == int(fcount_from_fn.group(1)), f"File count mismatch: idx {idx} vs fcount {fcount_from_fn.group(1)}"
      with open(os.path.join(postpro_response_dir, postpro_file), "r") as postfi:
        jso = json.load(postfi)
        resp_time = jso["response_time"]
        response_times_for_batch.append(resp_time)
    # create batch data, including aggregated values
    data["batch_id"].append(b_id)
    data["batch_type"].append(b_infos["b_type"])
    data["language"].append(b_infos["lang"])
    data["model_name"].append(model_name)
    data["prompt_tokens"].append(sum(prompt_tokens_for_batch))
    data["completion_tokens"].append(sum(completion_tokens_for_batch))
    data["total_tokens"].append(sum(total_tokens_for_batch))
    data["mean_tokens_per_completion"].append(sum(completion_tokens_for_batch) / len(completion_tokens_for_batch))
    data["response_time"].append(sum(response_times_for_batch))
    data["mean_response_time_per_completion"].append(sum(response_times_for_batch) / len(response_times_for_batch))
    print(f"  Done batch")#: {b_id} {datetime.now().strftime('%H:%M:%S')}")
  # create dataframe and write to file
  print(f"# Start dataframe {datetime.now().strftime('%H:%M:%S')}")
  df = pd.DataFrame(data)
  df.to_csv(os.path.join(cf.log_dir, cf.batch_stats_fn_prefix + f"__{args.out_sfx}.tsv"), sep="\t", index=False)
