"""Config for the project."""

import os


# IO --------------------------------------------------------------------------
few_shot_examples_id = "0001"

corpus_dir = "data"
log_dir = "logs"
ana_dir = "ana"
corpus_file = os.path.join(corpus_dir, "stgdir_labelGeneric_woDuplicates.csv")
testset_file = os.path.join(corpus_dir, "stgdir_labelGeneric_trainvalid_100-test.csv")
testset_30 = os.path.join(corpus_dir, "stgdir_labelGeneric_trainvalid_100-test_30.csv")
sampled_df_for_prompts = os.path.join(corpus_dir, f"sampled_df_for_prompts_{few_shot_examples_id}.tsv")

response_base_dir = "outputs"
# batch_id is filled based on cli args
response_dir = "outputs/{batch_id}/model_responses"
completions_dir = "outputs/{batch_id}/model_responses/completions"
postpro_response_dir = "outputs/{batch_id}/model_responses/postprocessed"
prompts_dir = "outputs/{batch_id}/prompts_run"

plot_dir = "outputs/{batch_id}/plots"

# Open AI ---------------------------------------------------------------------
oai_config = {
  "temperature": 1, # # was default on 2024-09-27, https://platform.openai.com/docs/api-reference/chat/create
  "top_p": 1, # ditto
  "seed": 14
}

mistral_config = {
  "temperature": 0.7, # was default on 2024-09-27, https://docs.mistral.ai/api/#tag/chat/operation/chat_completion_v1_chat_completions_post
  "top_p": 1,  # ditto
  "random_seed": 14
}

# Other ----------------------------------------------------------------------

categs_as13 = ["action", "aggression", "aparte", "delivery", "entrance",
               "exit", "interaction", "movement", "music",
               "narration", "object", "setting", "toward",]

prompting_modes = ["definition", "two-shot", "few-shot", "def-few-shot"]
prompting_langs = ["en", "fr"]

llm_list = ["gpt-4o", "gpt-4o-mini", "llama-3.0", "llama-3.1", "mistral-small-latest",
            "mistral-large-latest", "mistral-large-2407"]  # , "gpt-4", "gpt-4-turbo"]

categ_col_map = {"gold": "goldStr", "sys": "sysStr", "label": "labelStr", "labelStr": "label"}
categ_col_order = ["text", "gold", "goldStr", "text2", "sys", "sysStr", "cf_sents"]

batches_for_stats = os.path.join(corpus_dir, "batches_for_stats.txt")
batch_stats_fn_prefix = "batch_stats"
stat_suffixes_orig = ["zero-shot", "few-shot", "indiv", "grouped",
                      "zero-shot-indiv", "zero-shot-grouped", "few-shot-indiv", "few-shot-grouped"]
stat_suffixes = [x + "-fr" for x in stat_suffixes_orig] + [x + "-en" for x in stat_suffixes_orig]
stat_suffixes += stat_suffixes_orig
stat_suffixes = sorted(stat_suffixes)
model_name_mappings = {"mistral-large-2407": "mistral-large-latest"}
