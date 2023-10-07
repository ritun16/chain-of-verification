# from __future__ import annotations

import os
import re
import itertools
import openai
import tiktoken
import json
from dotenv import load_dotenv

from typing import Any, Dict, List, Optional

from pydantic import Extra

from langchain.schema.language_model import BaseLanguageModel
from langchain.callbacks.manager import (
    AsyncCallbackManagerForChainRun,
    CallbackManagerForChainRun,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chains.base import Chain
from langchain.prompts.base import BasePromptTemplate
from langchain.tools import DuckDuckGoSearchRun
import langchain
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain

import prompts
from execute_verification_chain import ExecuteVerificationChain


class WikiDataCategoryListCOVEChain(object):
    def __init__(self, llm):
        self.llm = llm
        
    def __call__(self):
        # Create baseline response chain
        baseline_response_prompt_template = PromptTemplate(input_variables=["original_question"],
                                                           template=prompts.BASELINE_PROMPT_WIKI)
        baseline_response_chain = LLMChain(llm=self.llm,
                                           prompt=baseline_response_prompt_template,
                                           output_key="baseline_response")
        # Create plan verification chain
        ## Create plan verification template
        verification_question_template_prompt_template = PromptTemplate(input_variables=["original_question"],
                                                                        template=prompts.VERIFICATION_QUESTION_TEMPLATE_PROMPT_WIKI)
        verification_question_template_chain = LLMChain(llm=self.llm,
                                                        prompt=verification_question_template_prompt_template,
                                                        output_key="verification_question_template")
        ## Create plan verification questions
        verification_question_generation_prompt_template = PromptTemplate(input_variables=["original_question",
                                                                                           "baseline_response",
                                                                                           "verification_question_template"],
                                                                          template=prompts.VERIFICATION_QUESTION_PROMPT_WIKI)
        verification_question_generation_chain = LLMChain(llm=self.llm,
                                                          prompt=verification_question_generation_prompt_template,
                                                          output_key="verification_questions")
        # Create execution verification
        execute_verification_question_prompt_template = PromptTemplate(input_variables=["verification_questions"],
                                                                       template=prompts.EXECUTE_PLAN_PROMPT)
        execute_verification_question_chain = ExecuteVerificationChain(llm=self.llm,
                                                                       prompt=execute_verification_question_prompt_template,
                                                                       output_key="verification_answers")
        # Create final refined response
        final_answer_prompt_template = PromptTemplate(input_variables=["original_question",
                                                                       "baseline_response",
                                                                       "verification_answers"],
                                                      template=prompts.FINAL_REFINED_PROMPT)
        final_answer_chain = LLMChain(llm=self.llm,
                                      prompt=final_answer_prompt_template,
                                      output_key="final_answer")
        
        # Create sequesntial chain
        wiki_data_category_list_cove_chain = SequentialChain(
                                                        chains=[baseline_response_chain,
                                                                verification_question_template_chain,
                                                                verification_question_generation_chain,
                                                                execute_verification_question_chain,
                                                                final_answer_chain],
                                                        input_variables=["original_question"],
                                                        # Here we return multiple variables
                                                        output_variables=["original_question",
                                                                          "baseline_response",
                                                                          "verification_question_template",
                                                                          "verification_questions",
                                                                          "verification_answers",
                                                                          "final_answer"],
                                                        verbose=False)
        return wiki_data_category_list_cove_chain

        
class MultiSpanCOVEChain(object):
    def __init__(self, llm):
        self.llm = llm
        
    def __call__(self):
        # Create baseline response chain
        baseline_response_prompt_template = PromptTemplate(input_variables=["original_question"],
                                                           template=prompts.BASELINE_PROMPT_MULTI)
        baseline_response_chain = LLMChain(llm=self.llm,
                                           prompt=baseline_response_prompt_template,
                                           output_key="baseline_response")
        ## Create plan verification questions
        verification_question_generation_prompt_template = PromptTemplate(input_variables=["original_question",
                                                                                           "baseline_response"],
                                                                          template=prompts.VERIFICATION_QUESTION_PROMPT_MULTI)
        verification_question_generation_chain = LLMChain(llm=self.llm,
                                                          prompt=verification_question_generation_prompt_template,
                                                          output_key="verification_questions")
        # Create execution verification
        execute_verification_question_prompt_template = PromptTemplate(input_variables=["verification_questions"],
                                                                       template=prompts.EXECUTE_PLAN_PROMPT)
        execute_verification_question_chain = ExecuteVerificationChain(llm=self.llm,
                                                                       prompt=execute_verification_question_prompt_template,
                                                                       output_key="verification_answers")
        # Create final refined response
        final_answer_prompt_template = PromptTemplate(input_variables=["original_question",
                                                                       "baseline_response",
                                                                       "verification_answers"],
                                                      template=prompts.FINAL_REFINED_PROMPT)
        final_answer_chain = LLMChain(llm=self.llm,
                                      prompt=final_answer_prompt_template,
                                      output_key="final_answer")
        
        # Create sequesntial chain
        multi_span_cove_chain = SequentialChain(
                                                chains=[baseline_response_chain,
                                                        verification_question_generation_chain,
                                                        execute_verification_question_chain,
                                                        final_answer_chain],
                                                input_variables=["original_question"],
                                                # Here we return multiple variables
                                                output_variables=["original_question",
                                                                  "baseline_response",
                                                                  "verification_questions",
                                                                  "verification_answers",
                                                                  "final_answer"],
                                                verbose=False)
        return multi_span_cove_chain
    
    
class LongFormCOVEChain(object):
    def __init__(self, llm):
        self.llm = llm
        
    def __call__(self):
        # Create baseline response chain
        baseline_response_prompt_template = PromptTemplate(input_variables=["original_question"],
                                                           template=prompts.BASELINE_PROMPT_LONG)
        baseline_response_chain = LLMChain(llm=self.llm,
                                           prompt=baseline_response_prompt_template,
                                           output_key="baseline_response")
        ## Create plan verification questions
        verification_question_generation_prompt_template = PromptTemplate(input_variables=["original_question",
                                                                                           "baseline_response"],
                                                                          template=prompts.VERIFICATION_QUESTION_PROMPT_LONG)
        verification_question_generation_chain = LLMChain(llm=self.llm,
                                                          prompt=verification_question_generation_prompt_template,
                                                          output_key="verification_questions")
        # Create execution verification
        execute_verification_question_prompt_template = PromptTemplate(input_variables=["verification_questions"],
                                                                       template=prompts.EXECUTE_PLAN_PROMPT)
        execute_verification_question_chain = ExecuteVerificationChain(llm=self.llm,
                                                                       prompt=execute_verification_question_prompt_template,
                                                                       output_key="verification_answers")
        # Create final refined response
        final_answer_prompt_template = PromptTemplate(input_variables=["original_question",
                                                                       "baseline_response",
                                                                       "verification_answers"],
                                                      template=prompts.FINAL_REFINED_PROMPT)
        final_answer_chain = LLMChain(llm=self.llm,
                                      prompt=final_answer_prompt_template,
                                      output_key="final_answer")
        
        # Create sequesntial chain
        long_form_cove_chain = SequentialChain(
                                                chains=[baseline_response_chain,
                                                        verification_question_generation_chain,
                                                        execute_verification_question_chain,
                                                        final_answer_chain],
                                                input_variables=["original_question"],
                                                # Here we return multiple variables
                                                output_variables=["original_question",
                                                                  "baseline_response",
                                                                  "verification_questions",
                                                                  "verification_answers",
                                                                  "final_answer"],
                                                verbose=False)
        return long_form_cove_chain