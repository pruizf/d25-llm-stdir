"""Open AI client"""

import argparse
from importlib import reload
import json
import os
import time

from openai import OpenAI

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
  parser.add_argument("model", help="Model to use for generating the response")
  parser.add_argument("prompt_mode", help="Prompting strategy to use")
  parser.add_argument("--ignore-existing", "-i", action="store_true",
                      help="Run even if results for same batch_name already exist (Used to continue an interrupted batch")
  args = parser.parse_args()
  assert args.model in cf.llm_list, f"Model {args.model} not in {cf.llm_list}"
  if not args.ignore_existing:
    assert args.batch_name not in os.listdir(cf.response_base_dir), f"Batch {args.batch_name} already exists"
  assert args.batch_name.startswith("batch_"), "Batch name must start with 'batch_'"
  assert args.prompt_mode in cf.prompting_modes, f"Prompting strategy {args.prompting} not in {cf.prompting_modes}"

  print(f"{args.batch_name}: Running [{args.model}] on [{args.corpus}], mode [{args.prompt_mode}]\n")

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

  # run the client
  oa_client = OpenAI()
  corpus_sep = "\t" if "30" in args.corpus else ","
  stdirs = ut.get_and_format_data(args.corpus, corpus_sep)
  for idx, row in stdirs.iterrows():
    if False and idx > 3:
      break

    # do not call API if the response is already available
    out_comp_fn = os.path.join(cf.completions_dir.format(batch_id=args.batch_name),
                               f"completion_{str.zfill(str(idx), 4)}_{args.model}.json")
    out_resp_fn = os.path.join(cf.postpro_response_dir.format(batch_id=args.batch_name),
                               f"postpro_response_{str.zfill(str(idx), 4)}_{args.model}.json")
    out_prompt_fn = os.path.join(cf.prompts_dir.format(batch_id=args.batch_name),
                                 f"prompt_{str.zfill(str(idx), 4)}_{args.model}.txt")
    if os.path.exists(out_comp_fn) and os.path.exists(out_resp_fn) and os.path.exists(out_prompt_fn):
      print(f"# Skipping stage direction: {idx}")
      continue

    # general prompt
    if args.prompt_mode == "two-shot":
      prompt = pr.gen_prompt.format(
        numbered_categories=ut.number_categories(cf.categs_as13),
        stdir=row["stgdir"],
        category_details=ut.get_category_info_two_shot())
    # prompt with definition only
    elif args.prompt_mode == "definition":
      prompt = pr.prompt_def_only.format(
        numbered_categories=ut.number_categories(cf.categs_as13),
        stdir=row["stgdir"],
        category_details=catinfo.cat_info_defs_only_en)
    elif args.prompt_mode == "few-shot":
      prompt = pr.gen_prompt.format(
        numbered_categories=ut.number_categories(cf.categs_as13),
        stdir=row["stgdir"],
        category_details=ut.format_examples_for_few_shot_prompt(cf.sampled_df_for_prompts))
    completion, resp, td = get_openai_response(oa_client, args.model, prompt, cf)
    #print(f"Prompt: {prompt}")
    jresp = json.loads(resp[0])
    jresp["stgdir"] = row["stgdir"]
    jresp["response_time"] = td
    jresp["model"] = args.model
    jresp["categFull"] = cf.categs_as13[int(json.loads(resp[0])["category"])]
    print(f"# Processing stage direction: {idx}")
    print(f"- Stage direction: {row['stgdir']}")
    print(f'- Response categ: {json.loads(resp[0])["category"]}. {cf.categs_as13[int(json.loads(resp[0])["category"])]}')
    print(f"- Response: {resp[0]}")
    print(f"- Response time: {td} ms")
    print()

    with (open(out_comp_fn, "w") as out_comp_fh):
      jso = completion.model_dump_json()
      json.dump(jso, out_comp_fh, indent=2)

    with (open(out_resp_fn, "w") as out_resp_fh):
      json.dump(jresp, out_resp_fh, indent=2)

    with (open(out_prompt_fn, "w") as out_prompt_fh):
      out_prompt_fh.write(prompt)
