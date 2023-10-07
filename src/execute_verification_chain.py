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



class ExecuteVerificationChain(Chain):
    """
    Implements the logic to execute the verification question for factual acuracy
    """

    prompt: BasePromptTemplate
    llm: BaseLanguageModel
    input_key: str = "verification_questions"
    output_key: str = "verification_answers"
    use_search_tool: bool = True
    search_tool: Any = DuckDuckGoSearchRun()

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @property
    def input_keys(self) -> List[str]:
        """Will be whatever keys the prompt expects.

        :meta private:
        """
        return [self.input_key]

    @property
    def output_keys(self) -> List[str]:
        """Will always return text key.

        :meta private:
        """
        return [self.output_key]

    def search_for_verification_question(self,
                                         verification_question: str
                                        ) -> str:
        search_result = self.search_tool.run(verification_question)
        return search_result
    
    def _call(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        verification_answers_list = list() # Will contain the answers of each verification questions
        question_answer_pair = "" # Final output of verification question and answer pair
        
        # Convert all the verification questions into a list of string
        sub_inputs = {k:v for k,v in inputs.items() if k==self.input_key}
        verification_questions_prompt_value = self.prompt.format_prompt(**sub_inputs)
        verification_questions_str = verification_questions_prompt_value.text
        verification_questions_list = verification_questions_str.split("\n")
        
        # Setting up prompt for both search tool and llm self evaluation
        execution_prompt_search_tool = PromptTemplate.from_template(prompts.EXECUTE_PLAN_PROMPT_SEARCH_TOOL)
        execution_prompt_self_llm = PromptTemplate.from_template(prompts.EXECUTE_PLAN_PROMPT_SELF_LLM)
        
        # Executing the verification questions, either using search tool or self llm
        for question in verification_questions_list:
            if self.use_search_tool:
                search_result = self.search_for_verification_question(question)
                execution_prompt_value = execution_prompt_search_tool.format_prompt(**{"search_result": search_result, "verification_question": question})
            else:
                execution_prompt_value = execution_prompt_self_llm.format_prompt(**{"verification_question": question})
            verification_answer_llm_result = self.llm.generate_prompt([execution_prompt_value], callbacks=run_manager.get_child() if run_manager else None)
            verification_answer_str = verification_answer_llm_result.generations[0][0].text
            verification_answers_list.append(verification_answer_str)
        
        # Create verification question and answer pair
        for question, answer in itertools.zip_longest(verification_questions_list, verification_answers_list):
            question_answer_pair += "Question: {} Answer: {}\n".format(question, answer)

        if run_manager:
            run_manager.on_text("Log something about this run")

        return {self.output_key: question_answer_pair}

    async def _acall(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[AsyncCallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        # Your custom chain logic goes here
        # This is just an example that mimics LLMChain
        prompt_value = self.prompt.format_prompt(**inputs)

        # Whenever you call a language model, or another chain, you should pass
        # a callback manager to it. This allows the inner run to be tracked by
        # any callbacks that are registered on the outer run.
        # You can always obtain a callback manager for this by calling
        # `run_manager.get_child()` as shown below.
        response = await self.llm.agenerate_prompt(
            [prompt_value], callbacks=run_manager.get_child() if run_manager else None
        )

        # If you want to log something about this run, you can do so by calling
        # methods on the `run_manager`, as shown below. This will trigger any
        # callbacks that are registered for that event.
        if run_manager:
            await run_manager.on_text("Log something about this run")

        return {self.output_key: response.generations[0][0].text}

    @property
    def _chain_type(self) -> str:
        return "execute_verification_chain"