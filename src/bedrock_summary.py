#!/usr/bin/env python3
import json
import os
import sys
import glob

import boto3

from constants import OUTPUT_DIR

MODELS = { 
    # Claude model
    "claude" : {
        "maxTokens": 200000,
        "modelId": "anthropic.claude-v2",
        "params": {
            "max_tokens_to_sample": 300,
            "temperature": 0.1,
            "top_p": 0.9
        },
        "prompt": """

Human: You are a geologist writing a report. Please provide a paragraph summary of the following text. Do not add any information that is not mentioned in the text below.

<text>
{text}
</text>

Assistant:
    """
    },
}

def run_claude(text):
    """ Run claude summarizer

    :param text: text string to be summarized
    :returns: summary text
    """
    brt = boto3.client(service_name='bedrock-runtime')
    body, modelId = run_model('claude', brt, text)
    accept = 'application/json'
    contentType = 'application/json'
    response = brt.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())
    summary = response_body.get('completion')
    #print(f"\nSUMMARY: {summary}")
    return summary

def run_model(model_name, brt, text):
    """ Runs a model using config

    :param model_name: name of model
    :param brt: AWS boto3 client object, connected to 'bedrock-runtime'
    :param text: text string to be summarized
    """
    config = MODELS[model_name]
    body = json.dumps({
        "prompt": config["prompt"].format(text=text),
        **config["params"]
    })
    return body, config['modelId']
        

if __name__ == "__main__":
    # List foundation models
    # boto3_bedrock = boto3.client('bedrock')
    # print(boto3_bedrock.list_foundation_models())

    # Run claude
    brt = boto3.client(service_name='bedrock-runtime')
    for file in glob.glob(os.path.join(OUTPUT_DIR,'*.txt')):
        print(f"{file=}")
        file_stats = os.stat(file)
        file_size = file_stats.st_size
        print(f"{file_size=}")
        if file_size > MODELS["claude"]["maxTokens"]:
            print("SKIP - too big")
            continue
        # Read text file
        with open(os.path.join(file), 'r') as fd:
            text = fd.read()
        print(f"{text[:90]=}")
        summary = run_claude(text)
        print(f"\nSUMMARY: {summary}")
