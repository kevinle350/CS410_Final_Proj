# imports for bedrock
# from langchain.chains import LLMChain
# from langchain.llms.bedrock import Bedrock
# from langchain.prompts import PromptTemplate
# import boto3

import os

def setup():
    return 
    # TODO: figure out the Bedrock API and client setup
    # os.environ["AWS_PROFILE"] = "TODO"

    # bedrock_client = boto3.client(
    #     service_name="bedrock-runtime",
    #     region_name="us-east-1"
    # )

    # modelID = "anthropic.claude-v2"

    # global llm
    # llm = Bedrock(
    #     model_id=modelID,
    #     client=bedrock_client,
    #     model_kwargs={"max_tokens_to_sample": 2000,"temperature":0.9}
    # )


def ask_chatbot(question):
    return "This function is not implemented yet."

    # TODO: uncomment when setup() is working
    # bedrock_chain = LLMChain(llm=llm)
    # response = bedrock_chain({'input': question})
    # return response['text']
