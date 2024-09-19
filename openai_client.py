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
import utils


#import utils as ut


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
    #seed=cf.oai_config["seed"]
  )
  td = 1000 * (time.time() - t1)
  #breakpoint()
  resps = [resp.message.content for resp in completion.choices]
  return completion, resps, td


if __name__ == "__main__":
  for module in [cf, pr, utils]:
    reload(module)
  reload(pr.catinfo)
  oa_client = OpenAI()
  stdirs = utils.get_and_format_data()
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
    print(f"Stage direction: {row['stgdir']}")
    print(f"Response: {resp[0]}")
    print(f'Response categ: {json.loads(resp[0])["category"]}. {pr.categs_as13[int(json.loads(resp[0])["category"]) - 1]}')
    print(f"Response time: {td} ms")
    print()
