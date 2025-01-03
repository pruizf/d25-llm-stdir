"""Mistral client"""

import argparse
from importlib import reload
import json
import os
import random
import time

from mistralai import Mistral

from data import category_info as catinfo
import config as cf
import prompts as pr
import prompts_grouped as prg
import utils as ut


def get_mistral_response(m_client, model, prompt, cf):
  """
  Returns Open AI response and response time.

  Args:
      m_client (mistralai.Mistral): The Mistral client.
      model (str): The model to use for generating the response.
      prompt: The prompt to use for generating the response.
      cf (module): The configuration module.

  Returns:
      tuple: A tuple containing the response and the response time in seconds.
  """
  t1 = time.time()
  completion = m_client.chat.complete(
    model=model,
    messages=[
      {"role": "user", "content": prompt},
    ],
    temperature=cf.mistral_config["temperature"],
    top_p=cf.mistral_config["top_p"],
    response_format={"type": "json_object"},
    random_seed=cf.mistral_config["random_seed"]
  )
  td = 1000 * (time.time() - t1)
  #breakpoint()
  resps = [resp.message.content for resp in completion.choices]
  return completion, resps, td


if __name__ == "__main__":
  # cli args
  parser = argparse.ArgumentParser(description="Mistral client")
  parser.add_argument("batch_name", help="Batch name used as prefix on outputs")
  parser.add_argument("corpus", help="Corpus to run the model on")
  parser.add_argument("model", help="Model to use for generating the response")
  parser.add_argument("prompt_mode", help="Prompting strategy to use")
  parser.add_argument("prompt_lang", help="Language for prompts")
  parser.add_argument("--ignore-existing", "-i", action="store_true",
                      help="Run even if results for same batch_name already exist (Used to continue an interrupted batch")
  parser.add_argument("--group-size", "-g",
                      help="Number of stage directions to group together", type=int)

  args = parser.parse_args()
  assert args.model in cf.llm_list, f"Model {args.model} not in {cf.llm_list}"
  if not args.ignore_existing:
    assert args.batch_name not in os.listdir(cf.response_base_dir), f"Batch {args.batch_name} already exists"
  assert args.batch_name.startswith("batch_"), "Batch name must start with 'batch_'"
  assert args.prompt_mode in cf.prompting_modes, f"Prompting strategy {args.prompting} not in {cf.prompting_modes}"
  assert args.prompt_lang in cf.prompting_langs, f"Prompting language {args.prompt_lang} not in {cf.prompting_langs}"

  print(f"{args.batch_name}: Running [{args.model}] on [{args.corpus}], mode [{args.prompt_mode}]\n")

  # make sure to import updated modules
  for module in [cf, pr, prg, ut, catinfo, ut.catinfo]:
    reload(module)

  # IO
  for mydir in [cf.response_dir, cf.completions_dir, cf.postpro_response_dir,
                cf.prompts_dir]:
    if not os.path.exists(mydir.format(batch_id=args.batch_name)):
      os.makedirs(mydir.format(batch_id=args.batch_name))
  if not os.path.exists(cf.log_dir):
    os.makedirs(cf.log_dir)

  # run the client
  batch_start_time = time.time()
  #mistral_client = Mistral(api_key=os.getenv("MISTRAL_API_KEY_P"))
  mistral_client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
  corpus_sep = "\t" if "30" in args.corpus else ","
  stdirs = ut.get_and_format_data(args.corpus, corpus_sep)
  #TODO change CLI args making group_size obligatory
  if args.group_size:
    # create stage direction groups
    #TODO refactor as a function
    #stdirs = ut.group_stage_directions(stdirs, args.group_size)
    stdirs = stdirs.copy()
    stdirs['groupNbr'] = (stdirs.index // args.group_size) + 1
    # iterate over groups, getting one response per group
    # enumerate cos we use zero indexes everywhere in this app
    for gidx, grpn in enumerate(stdirs['groupNbr'].unique()):
      if False and grpn > 1:
        break
      print(f"# Group: {gidx}")
      stdirs_grp = stdirs[stdirs['groupNbr'] == grpn]
      stdirs_for_grp = stdirs_grp['stgdir'].tolist()
      stdirs_for_prompt = []
      for sidx, stgdir in enumerate(stdirs_for_grp):
        global_idx = gidx * args.group_size + sidx
        # add the concatenation of the stage directions to the prompt
        stdirs_for_prompt.append(f"{global_idx}. {stgdir}")
        print(f"- Stage direction {sidx}: {stgdir}")
      stdirs_as_str = "\n".join(stdirs_for_prompt)

      # back to group level
      # IO
      out_comp_fn = os.path.join(cf.completions_dir.format(batch_id=args.batch_name),
                                 f"completion_group_{str.zfill(str(gidx), 3)}_{args.model}.json")
      out_resp_fn = os.path.join(cf.postpro_response_dir.format(batch_id=args.batch_name),
                                 f"postpro_response_group_{str.zfill(str(gidx), 3)}_{args.model}.json")
      out_prompt_fn = os.path.join(cf.prompts_dir.format(batch_id=args.batch_name),
                                   f"prompt_group_{str.zfill(str(gidx), 4)}_{args.model}.txt")
      # do not call API if the response is already available
      if os.path.exists(out_comp_fn) and os.path.exists(out_resp_fn) and os.path.exists(out_prompt_fn):
        print(f"# Skipping group: {gidx}")
        continue

      # per-group prompts (note value of `stdir` in the prompt)
      # general prompt (brief definition and two or three examples)
      if args.prompt_mode == "two-shot":
        # Note: Prompt is English, the two examples are in French, and we did
        # not implement the choice to use a French prompt here
        prompt_template = prg.gen_prompt if args.prompt_lang == "en" else prg.gen_prompt_fr
        prompt = prompt_template.format(
          numbered_categories=ut.number_categories(cf.categs_as13),
          stdir=stdirs_as_str,
          category_details=ut.get_category_info_two_shot().rstrip())
      # prompt with a detailed definition only (no examples)
      elif args.prompt_mode == "definition":
        prompt_template = prg.prompt_def_only if args.prompt_lang == "en" else prg.prompt_def_only_fr
        catinfo_template = catinfo.defs_detailed_en if args.prompt_lang == "en" else catinfo.defs_detailed_fr
        prompt = prompt_template.format(
          numbered_categories=ut.number_categories(cf.categs_as13),
          stdir=stdirs_as_str,
          category_details=catinfo_template.rstrip())
      # few-shot, without detailed definition
      elif args.prompt_mode == "few-shot":
        prompt_template = prg.gen_prompt if args.prompt_lang == "en" else prg.gen_prompt_fr
        catinfo_template = catinfo.few_shot_defs_simple_en if args.prompt_lang == "en" else catinfo.few_shot_defs_simple_fr
        shots_per_cat = ut.format_examples_for_few_shot_prompt(cf.sampled_df_for_prompts, args.prompt_lang)
        prompt = prompt_template.format(
          numbered_categories=ut.number_categories(cf.categs_as13),
          stdir=stdirs_as_str,
          category_details=catinfo_template.format(**shots_per_cat).rstrip())
      # few-shot, with detailed definition (mode def-few-shot)
      else:
        prompt_template = prg.gen_prompt if args.prompt_lang == "en" else prg.gen_prompt_fr
        catinfo_template = catinfo.few_shot_defs_detailed_en if args.prompt_lang == "en" else catinfo.few_shot_defs_detailed_fr
        shots_per_cat = ut.format_examples_for_few_shot_prompt(cf.sampled_df_for_prompts, args.prompt_lang)
        prompt = prompt_template.format(
          numbered_categories=ut.number_categories(cf.categs_as13),
          stdir=stdirs_as_str,
          category_details=catinfo_template.format(**shots_per_cat).rstrip())

      # obtain response for group
      completion, resp, td = get_mistral_response(mistral_client, args.model, prompt, cf)
      time.sleep(1)

      # postprocess response
      try:
        jresp = json.loads(resp[0])
      except json.JSONDecodeError:
        # based on attested errors
        if not resp[0].endswith("}]}"):
          jresp = json.loads(resp[0] + "}]}")
      for ridx, result in enumerate(jresp["result_list"]):
        result["stgdir"] = stdirs_for_grp[ridx]
        try:
          result["categFull"] = cf.categs_as13[int(result["category"])]
        # Category output as string, not number
        except ValueError:
          try:
            assert result["category"] in cf.categs_as13, f"Category {result['category']} not in {cf.categs_as13}"
          except AssertionError:
            # saw one case where Mistral finds no suitable category and outputs the string 'null'
            orig_categ = result["category"]
            rand_categ = random.choice(cf.categs_as13)
            print(f"- >>> Hallucinated category {result['stgdir_nbr']} filled with random category {rand_categ}")
            result["category"] = rand_categ
            with open(os.path.join("logs", f"hallucinated_categs_{args.batch_name}.txt"), "a") as out_ac:
              out_ac.write(f"{result['stgdir_nbr']}\t{orig_categ}\t{rand_categ}\n")

          print(f"- >>> String label used, group index [{gidx}], group number [{grpn}], result number [{ridx}]")
          # bring back label to a numberic label (for evaluation)
          result["categFull"] = result["category"]
        # Category hallucination (seen in one crashed batch, added to allow batch to finish if happens again)
        except IndexError:
          print(f"- >>> Missing category, group index [{gidx}], group number [{grpn}], result number [{ridx}]")
          orig_categ = result["category"]
          rand_categ = random.choice(cf.categs_as13)
          print(f"      Hallucinated category [{result['stgdir_nbr']}] filled with random category [{rand_categ}]")
          result["category"] = rand_categ
          with open(os.path.join("logs", f"hallucinated_categs_{args.batch_name}.txt"), "a") as out_ac:
            out_ac.write(f"{result['stgdir_nbr']}\t{orig_categ}\t{rand_categ}\n")
      jresp["response_time"] = td
      jresp["model"] = args.model
      print(f"## Processing group: {grpn}")
      for jidx, result in enumerate(jresp["result_list"]):
        print(f"- Stage direction: {result['stgdir']}")
        try:
          print(f'- Response categ: {result["category"]}. {cf.categs_as13[int(result["category"])]}')
        except ValueError:
          print(f'- Response categ: {result["category"]}. {result["category"]}')

          print(f"- >>> String label used, group index [{gidx}], group number [{grpn}], result number [{jidx}]")
          # bring back label to a numberic label (for evaluation)
          result["category"] = cf.categs_as13.index(result["category"])
        print(f"- Response: {result}")
      print(f"- Response time: {td} ms")
      print()

      with (open(out_comp_fn, "w") as out_comp_fh):
        jso = completion.model_dump_json()
        json.dump(jso, out_comp_fh, indent=2)

      with (open(out_resp_fn, "w") as out_resp_fh):
        json.dump(jresp, out_resp_fh, indent=2)

      with (open(out_prompt_fn, "w") as out_prompt_fh):
        out_prompt_fh.write(prompt)

  batch_end_time = time.time()
  print(f"\nBatch duration: {batch_end_time - batch_start_time:.2f} seconds")