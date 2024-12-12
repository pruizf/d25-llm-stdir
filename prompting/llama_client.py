"""Llama 3 client"""

import argparse
from importlib import reload
import json
import os
import re
import sys
import time

import torch
import transformers

from data import category_info as catinfo
import config as cf
import prompts as pr
import utils as ut


if __name__ == "__main__":
  # cli args
  parser = argparse.ArgumentParser(description="Open AI client")
  parser.add_argument("batch_name", help="Batch name used as prefix on outputs")
  parser.add_argument("corpus", help="Corpus to run the model on")
  parser.add_argument("model", help="Model to use for generating the response")
  parser.add_argument("prompt_mode", help="Prompting strategy to use")
  parser.add_argument("prompt_lang", help="Language for prompts")
  parser.add_argument("--ignore-existing", "-i", action="store_true",
                      help="Run even if results for same batch_name already exist (Used to continue an interrupted batch")
  args = parser.parse_args()
  assert args.model in cf.llm_list, f"Model {args.model} not in {cf.llm_list}"
  if not args.ignore_existing:
    assert args.batch_name not in os.listdir(cf.response_base_dir), f"Batch {args.batch_name} already exists"
  assert args.batch_name.startswith("batch_"), "Batch name must start with 'batch_'"
  assert args.prompt_mode in cf.prompting_modes, f"Prompting strategy {args.prompting} not in {cf.prompting_modes}"
  assert args.prompt_lang in cf.prompting_langs, f"Prompting language {args.prompt_lang} not in {cf.prompting_langs}"

  # log gpu info
  batch_dir = os.path.join(cf.response_base_dir, args.batch_name)
  if not os.path.exists(batch_dir):
    os.makedirs(batch_dir)
  batch_log_fn = os.path.join(batch_dir, f"gpu_infos_{args.batch_name}.txt")
  if torch.cuda.is_available():
    with open(batch_log_fn, "w") as batch_log_fh:
      batch_log_fh.write(f"Cur GPU: {torch.cuda.current_device()}\n")
      batch_log_fh.write(f"GPU name: {torch.cuda.get_device_name(torch.cuda.current_device())}\n")
      batch_log_fh.write(f"GPU count: {torch.cuda.device_count()}\n")

  print(f"{args.batch_name}: Running [{args.model}] on [{args.corpus}]. Start {time.strftime('%H:%M:%S')}\n")

  # make sure to import updated modules
  for module in [cf, pr, ut, catinfo, ut.catinfo]:
    reload(module)

  # IO
  for mydir in [cf.response_dir, cf.completions_dir, cf.postpro_response_dir,
                cf.prompts_dir]:
    if not os.path.exists(mydir.format(batch_id=args.batch_name)):
      os.makedirs(mydir.format(batch_id=args.batch_name))
  if not os.path.exists(cf.log_dir):
    os.makedirs(cf.log_dir)

  # prepare client
  print(f"Start loading model {time.strftime('%H:%M:%S')}")
  model_id = "meta-llama/Meta-Llama-3-8B-Instruct" if args.model == "llama-3" else "meta-llama/Meta-Llama-3.1-8B-Instruct"
  pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
  )
  print()
  print(f"Done loading model {time.strftime('%H:%M:%S')}")

  terminators = [
    pipeline.tokenizer.eos_token_id,
    pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
  ]

  # run the client
  corpus_sep = "\t" if "30" in args.corpus else ","
  stdirs = ut.get_and_format_data(args.corpus, corpus_sep)
  for idx, row in stdirs.iterrows():
    print(f"# Processing stage direction: {idx}")
    if False and idx > 10:
      break
    # do not call model if the response is already available
    out_resp_fn = os.path.join(cf.postpro_response_dir.format(batch_id=args.batch_name),
                               f"postpro_response_{str.zfill(str(idx), 4)}_{args.model}.json")
    if os.path.exists(out_resp_fn):
      print(f"# Skipping stage direction: {idx}")
      continue
    # general prompt (brief definition and two or three examples)
    if args.prompt_mode == "two-shot":
      # Note: Prompt is English, the two examples are in French, and we did
      # not implement the choice to use a French prompt here
      prompt_template = pr.gen_prompt if args.prompt_lang == "en" else pr.gen_prompt_fr
      prompt = prompt_template.format(
        numbered_categories=ut.number_categories(cf.categs_as13),
        stdir=row["stgdir"],
        category_details=ut.get_category_info_two_shot())
    # prompt with a detailed definition only (no examples)
    elif args.prompt_mode == "definition":
      prompt_template = pr.prompt_def_only if args.prompt_lang == "en" else pr.prompt_def_only_fr
      catinfo_template = catinfo.defs_detailed_en if args.prompt_lang == "en" else catinfo.defs_detailed_fr
      prompt = prompt_template.format(
        numbered_categories=ut.number_categories(cf.categs_as13),
        stdir=row["stgdir"],
        category_details=catinfo_template)
    # few-shot, without detailed definition
    elif args.prompt_mode == "few-shot":
      prompt_template = pr.gen_prompt if args.prompt_lang == "en" else pr.gen_prompt_fr
      catinfo_template = catinfo.few_shot_defs_simple_en if args.prompt_lang == "en" else catinfo.few_shot_defs_simple_fr
      shots_per_cat = ut.format_examples_for_few_shot_prompt(cf.sampled_df_for_prompts, args.prompt_lang)
      prompt = prompt_template.format(
        numbered_categories=ut.number_categories(cf.categs_as13),
        stdir=row["stgdir"],
        category_details=catinfo_template.format(**shots_per_cat))
    # few-shot, with detailed definition (mode def-few-shot)
    else:
      prompt_template = pr.gen_prompt if args.prompt_lang == "en" else pr.gen_prompt_fr
      catinfo_template = catinfo.few_shot_defs_detailed_en if args.prompt_lang == "en" else catinfo.few_shot_defs_detailed_fr
      shots_per_cat = ut.format_examples_for_few_shot_prompt(cf.sampled_df_for_prompts, args.prompt_lang)
      prompt = prompt_template.format(
        numbered_categories=ut.number_categories(cf.categs_as13),
        stdir=row["stgdir"],
        category_details=catinfo_template.format(**shots_per_cat))

    messages = [
      {"role": "user", "content": prompt},
    ]

    t1 = time.time()
    resp = pipeline(
      messages,
      max_new_tokens=256,
      eos_token_id=terminators,
      do_sample=True,
      #temperature=1,
      #top_p=1,
    )
    td = 1000 * (time.time() - t1)
    resp.append(td)

    out_resp_fn = os.path.join(cf.postpro_response_dir.format(batch_id=args.batch_name),
                               f"postpro_response_{str.zfill(str(idx), 4)}_{args.model}.json")
    with open(out_resp_fn, "w") as out_resp_fh:
      #out_resp_fh.write(resp)
      json.dump(resp, out_resp_fh, indent=2)
