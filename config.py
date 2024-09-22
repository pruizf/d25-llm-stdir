"""Config for the project."""

import os


# IO --------------------------------------------------------------------------
batch_id = "batch_005" # obsolete, this is now passed as an argument

corpus_dir = "data"
corpus_file  = os.path.join(corpus_dir, "stgdir_labelGeneric_woDuplicates.csv")
testset_file = os.path.join(corpus_dir, "stgdir_labelGeneric_trainvalid_100-test.csv")
testset_30 = os.path.join(corpus_dir, "stgdir_labelGeneric_trainvalid_100-test_30.csv")
log_dir = "logs"

response_base_dir = "outputs"
response_dir = "outputs/{batch_id}/model_responses"
completions_dir = "outputs/{batch_id}/model_responses/completions"
postpro_response_dir = "outputs/{batch_id}/model_responses/postprocessed"
prompts_dir = f"outputs/{batch_id}/prompts_run"

plot_dir = "outputs/{batch_id}/plots"

# Open AI ---------------------------------------------------------------------
oai_config = {
  "temperature": 1,
  "top_p": 1,
  "seed": 14
}

# Other ----------------------------------------------------------------------

prompting_modes = ["definition", "two-shot", "few-shot"]

llm_list = ["gpt-4o", "gpt-4o-mini", "llama-3", "llama-3.1"]  # , "gpt-4", "gpt-4-turbo"]

categ_col_map = {"gold": "goldStr", "sys": "sysStr", "label": "labelStr"}
categ_col_order = ["text", "gold", "goldStr", "text2", "sys", "sysStr", "cf_sents"]
