import os
import json
import sys

with open("config.json") as f:
    env_vars = json.load(f)

HUGGINGFACEHUB_API_TOKEN = env_vars["HF_API_KEY"]
OPENAI_API_KEY = env_vars["OPENAI_API_KEY"]