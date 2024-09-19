"""Open AI client"""

from importlib import reload
import json
import os
import re
import time

from openai import OpenAI
from openai.types.chat import ChatCompletion
import pandas as pd

import config as cf
import prompts as pr
import utils as ut

"""TODO
- log responses
- then will parse them to get the category etc.
- restrict this to the test set
"""


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
  # make sure to import updated modules
  for module in [cf, pr, ut]:
    reload(module)
  reload(pr.catinfo)

  # IO
  for mydir in [cf.log_dir, cf.response_dir, cf.completions_dir, cf.postpro_response_dir]:
    if not os.path.exists(mydir):
      os.makedirs(mydir)

  # run the client
  oa_client = OpenAI()
  stdirs = ut.get_and_format_data()
  for idx, row in stdirs.iterrows():
    if idx == 0:
      continue
    elif idx > 3:
      break
    prompt = pr.gen_promt.format(
      numbered_categories=pr.number_categories(pr.categs_as13),
      stdir=row["stgdir"],
      category_details=pr.get_category_info(cf))
    completion, resp, td = get_openai_response(oa_client, cf.oai_models[0], prompt, cf)
    #print(f"Prompt: {prompt}")
    jresp = json.loads(resp[0])
    jresp["stgdir"] = row["stgdir"]
    jresp["response_time"] = td
    jresp["model"] = cf.oai_models[0]
    jresp["categFull"] = pr.categs_as13[int(json.loads(resp[0])["category"])]
    print(f"Stage direction: {row['stgdir']}")
    print(f"Response: {resp[0]}")
    print(f'Response categ: {json.loads(resp[0])["category"]}. {pr.categs_as13[int(json.loads(resp[0])["category"])]}')
    print(f"Response time: {td} ms")
    print()
    out_comp_fn = os.path.join(cf.completions_dir, f"completion_{str.zfill(str(idx), 4)}_{cf.oai_models[0]}.json")
    with (open(out_comp_fn, "w") as out_comp_fh):
      jso = completion.model_dump_json()
      json.dump(jso, out_comp_fh, indent=2)
    out_resp_fn = os.path.join(cf.postpro_response_dir, f"postpro_response_{str.zfill(str(idx), 4)}_{cf.oai_models[0]}.json")
    with (open(out_resp_fn, "w") as out_resp_fh):
      json.dump(jresp, out_resp_fh, indent=2)

