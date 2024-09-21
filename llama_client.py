"""Llama 3 client"""

import argparse
from importlib import reload
import json
import os
import re
import sys
import time

from openai import OpenAI
import torch
import transformers

from openai.types.chat import ChatCompletion
import pandas as pd

from data import category_info as catinfo
import config as cf
import prompts as pr
import utils as ut


def get_openai_response(oa_client, model, prompt, cf):
  """
  Returns Open AI response and response time.

  Args:
      oa_client (openai.OpenAI): The OpenAI client.
      model (str): The model to use for generating the response.
      prompt: The prompt to use for generating the response.
      cf (module): The configuration module.

  Returns:
      tuple: A tuple containing the humor response and the response time in seconds.
  """
  t1 = time.time()
  completion = oa_client.chat.completions.create(
    model=model,
    messages=[
      {"role": "user", "content": prompt},
    ],
    temperature=cf.oai_config["temperature"],
    top_p=cf.oai_config["top_p"],
    response_format={"type": "json_object"},
    seed=cf.oai_config["seed"]
  )
  td = 1000 * (time.time() - t1)
  #breakpoint()
  resps = [resp.message.content for resp in completion.choices]
  return completion, resps, td


if __name__ == "__main__":
  # cli args
  parser = argparse.ArgumentParser(description="Open AI client")
  parser.add_argument("batch_name", help="Batch name used as prefix on outputs")
  parser.add_argument("corpus", help="Corpus to run the model on")
  args = parser.parse_args()
  assert args.batch_name not in os.listdir(cf.response_base_dir), f"Batch {args.batch_name} already exists"
  assert args.batch_name.startswith("batch_"), "Batch name must start with 'batch_'"
  print(f"{args.batch_name}: Running [{args.model}] on [{args.corpus}]\n")

  # make sure to import updated modules
  for module in [cf, pr, ut, catinfo, pr.catinfo]:
    reload(module)

  # IO
  for mydir in [cf.response_dir, cf.completions_dir, cf.postpro_response_dir,
                cf.prompts_dir]:
    if not os.path.exists(mydir.format(batch_id=args.batch_name)):
      os.makedirs(mydir.format(batch_id=args.batch_name))
  if not os.path.exists(cf.log_dir):
    os.makedirs(cf.log_dir)

  # prepare client
  model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
  pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
  )

  terminators = [
    pipeline.tokenizer.eos_token_id,
    pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
  ]



  # run the client
  corpus_sep = "\t" if "30" in args.corpus else ","
  stdirs = ut.get_and_format_data(args.corpus, corpus_sep)
  for idx, row in stdirs.iterrows():
    if False and idx > 3:
      break
    # general prompt
    if False:
      prompt = pr.gen_promt.format(
        numbered_categories=pr.number_categories(pr.categs_as13),
        stdir=row["stgdir"],
        category_details=pr.get_category_info(cf))
    # prompt with definition only
    prompt = pr.prompt_def_only.format(
      numbered_categories=pr.number_categories(pr.categs_as13),
      stdir=row["stgdir"],
      category_details=catinfo.cat_info_defs_only_en)

    messages = [
      {"role": "user", "content": prompt},
    ]

    resp = pipeline(
      messages,
      max_new_tokens=256,
      eos_token_id=terminators,
      do_sample=True,
      temperature=1,
      top_p=1,
    )

    jresp = json.loads(resp[0])
    jresp["stgdir"] = row["stgdir"]
    jresp["response_time"] = td
    jresp["model"] = args.model
    jresp["categFull"] = pr.categs_as13[int(json.loads(resp[0])["category"])]
    print(f"# Processing stage direction: {idx}")
    print(f"- Stage direction: {row['stgdir']}")
    print(f'- Response categ: {json.loads(resp[0])["category"]}. {pr.categs_as13[int(json.loads(resp[0])["category"])]}')
    print(f"- Response: {resp[0]}")
    print(f"- Response time: {td} ms")
    print()
    out_comp_fn = os.path.join(cf.completions_dir.format(batch_id=args.batch_name),
                               f"completion_{str.zfill(str(idx), 4)}_{args.model}.json")
    with (open(out_comp_fn, "w") as out_comp_fh):
      jso = completion.model_dump_json()
      json.dump(jso, out_comp_fh, indent=2)
    out_resp_fn = os.path.join(cf.postpro_response_dir.format(batch_id=args.batch_name),
                               f"postpro_response_{str.zfill(str(idx), 4)}_{args.model}.json")
    with (open(out_resp_fn, "w") as out_resp_fh):
      json.dump(jresp, out_resp_fh, indent=2)
    out_prompt_fn = os.path.join(cf.prompts_dir.format(batch_id=args.batch_name),
                                 f"prompt_{str.zfill(str(idx), 4)}_{args.model}.txt")
    with (open(out_prompt_fn, "w") as out_prompt_fh):
      out_prompt_fh.write(prompt)
