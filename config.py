"""Config for the project."""

import os

# OpenAI API key

# IO --------------------------------------------------------------------------
batch_id = "batch_003"

corpus_dir = "data"
corpus_file  = os.path.join(corpus_dir, "stgdir_labelGeneric_woDuplicates.csv")
#testset_file = os.path.join(corpus_dir, "stgdir_labelGeneric_trainvalid_100-test.csv")
testset_30 = os.path.join(corpus_dir, "stgdir_labelGeneric_trainvalid_100-test_30.csv")
testset_file = testset_30
sep = "|"
sep_test = ","
sep_test = "\t"
log_dir = "logs"

response_base_dir = "outputs"
response_dir = f"outputs/{batch_id}/model_responses"
completions_dir = f"outputs/{batch_id}/model_responses/completions"
postpro_response_dir = f"outputs/{batch_id}/model_responses/postprocessed"
prompts_dir = f"outputs/{batch_id}/prompts_run"

plot_dir = f"outputs/{batch_id}/plots"

# Open AI ---------------------------------------------------------------------
oai_config = {
  "temperature": 1,
  "top_p": 1,
  "seed": 14
}

#oai_models = ["gpt-3.5-turbo"]  # , "gpt-4", "gpt-4-turbo", "gpt-4o"]
#oai_models = ["gpt-4o"]  # , "gpt-4", "gpt-4-turbo", "gpt-4o"]
oai_models = ["gpt-4o-mini"]  # , "gpt-4", "gpt-4-turbo", "gpt-4o"]
#oai_models = ["gpt-3.5-turbo", "gpt-4o"]  # , "gpt-4", "gpt-4-turbo", "gpt-4o"]

# Other

categ_col_map = {"gold": "goldStr", "sys": "sysStr"}
categ_col_order = ["text", "gold", "goldStr", "text2", "sys", "sysStr", "cf_sents"]
