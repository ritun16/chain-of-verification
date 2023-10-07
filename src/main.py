import argparse
from dotenv import load_dotenv
from pprint import pprint

from langchain.chat_models import ChatOpenAI

from route_chain import RouteCOVEChain

load_dotenv("/workspace/.env")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description ='Chain of Verification (CoVE) parser.')
    parser.add_argument('--question',  
                        type = str,
                        required = True,
                        help ='The original question user wants to ask')
    parser.add_argument('--llm-name',  
                        type = str,
                        required = False,
                        default = "gpt-3.5-turbo-0613",
                        help ='The openai llm name')
    parser.add_argument('--temperature',  
                        type = float,
                        required = False,
                        default = 0.1,
                        help ='The temperature of the llm')
    parser.add_argument('--max-tokens',  
                        type = int,
                        required = False,
                        default = 500,
                        help ='The max_tokens of the llm')
    parser.add_argument('--show-intermediate-steps',  
                        type = bool,
                        required = False,
                        default = True,
                        help ='The max_tokens of the llm')
    args = parser.parse_args()
    
    original_query = args.question
    chain_llm = ChatOpenAI(model_name=args.llm_name,
                     temperature=args.temperature,
                     max_tokens=args.max_tokens)
    
    route_llm = ChatOpenAI(model_name="gpt-3.5-turbo-0613",
                     temperature=0.1,
                     max_tokens=500)
    
    router_cove_chain_instance = RouteCOVEChain(original_query, route_llm, chain_llm, args.show_intermediate_steps)
    router_cove_chain = router_cove_chain_instance()
    router_cove_chain_result = router_cove_chain({"original_question":original_query})
    
    if args.show_intermediate_steps:
        print("\n" + 80*"#" + "\n")
        pprint(router_cove_chain_result)
        print("\n" + 80*"#" + "\n")
    print("Final Answer: {}".format(router_cove_chain_result["final_answer"]))
    