"""Config for the project."""

import os

# OpenAI API key

# IO --------------------------------------------------------------------------
corpus_dir = "data"
corpus_file  = os.path.join(corpus_dir, "stgdir_labelGeneric_woDuplicates.csv")
testset_file = os.path.join(corpus_dir, "stgdir_labelGeneric_trainvalid_100-test.csv")
sep = "|"
sep_test = ","
log_dir = "logs"

response_dir = "outputs/model_responses"
completions_dir = "outputs/model_responses/completions"
postpro_response_dir = "outputs/model_responses/postprocessed"

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

