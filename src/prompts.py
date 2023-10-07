######################################################################## BASELINE PROMPTS ########################################################################
BASELINE_PROMPT_WIKI = """Answer the below question which is asking for a list of entities (names, places, locations etc). Output should be a numbered list and only contains the relevant & concise enitites as answer. NO ADDITIONAL DETAILS.

Question: {original_question}

Answer:"""

BASELINE_PROMPT_MULTI = """Answer the below question correctly and in a concise manner without much details. Only answer what the question is asked.

Question: {original_question}

Answer:"""

BASELINE_PROMPT_LONG = """Answer the below question correctly.

Question: {original_question}

Answer:"""

################################################################### PLAN VERIFICATION PROMPTS ###################################################################
VERIFICATION_QUESTION_TEMPLATE_PROMPT_WIKI = """Your task is to create a verification question based on the below question provided.
Example Question: Who are some movie actors who were born in Boston?
Example Verification Question: Was [movie actor] born in [Boston]
Explanation: In the above example the verification question focused only on the ANSWER_ENTITY (name of the movie actor) and QUESTION_ENTITY (birth place).
Similarly you need to focus on the ANSWER_ENTITY and QUESTION_ENTITY from the actual question and generate verification question.

Actual Question: {original_question}

Final Verification Question:"""

VERIFICATION_QUESTION_PROMPT_WIKI = """Your task is to create a series of verification questions based on the below question, the verfication question template and baseline response.
Example Question: Who are some movie actors who were born in Boston?
Example Verification Question Template: Was [movie actor] born in Boston?
Example Baseline Response: 1. Matt Damon - Famous for his roles in films like "Good Will Hunting," "The Bourne Identity" series, and "The Martian," Damon is an Academy Award-winning actor, screenwriter, and producer.
2. Chris Evans - Famous for his portrayal of Captain America in the Marvel Cinematic Universe, Evans has also appeared in movies like "Snowpiercer" and "Knives Out."
Verification questions: 1. Was Matt Damon born in Boston?
2. Was Chirs Evans born in Boston?
etc.
Example Verification Question: 1. Was Matt Damon born in Boston?
2. Was Chris Evans born in Boston?

Explanation: In the above example the verification questions focused only on the ANSWER_ENTITY (name of the movie actor) and QUESTION_ENTITY (birth place) based on the template and substitutes entity values from the baseline response.
Similarly you need to focus on the ANSWER_ENTITY and QUESTION_ENTITY from the actual question and substitute the entity values from the baseline response to generate verification questions.

Actual Question: {original_question}
Baseline Response: {baseline_response}
Verification Question Template: {verification_question_template}

Final Verification Questions:"""

VERIFICATION_QUESTION_PROMPT_MULTI = """Your task is to create verification questions based on the below original question and the baseline response. The verification questions are meant for verifying the factual acuracy in the baseline response.
Example Question: Who invented the first printing press and in what year?
Example Baseline Response: Johannes Gutenberg, 1450.
Example Verification Questions: 1. Did Johannes Gutenberg invent first printing press?
2. Did Johannes Gutenberg invent first printing press in the year 1450?

Explanation: The verification questions are highly aligned with both the qctual question and baseline response. The actual question is comprises of multiple independent questions which in turn has multiple independent answers in the baseline response. Hence, the verification questions should also be independent for factual verification.

Actual Question: {original_question}
Baseline Response: {baseline_response}

Final Verification Questions:"""

VERIFICATION_QUESTION_PROMPT_LONG = """Your task is to create verification questions based on the below original question and the baseline response. The verification questions are meant for verifying the factual acuracy in the baseline response. Output should be numbered list of verification questions.

Actual Question: {original_question}
Baseline Response: {baseline_response}

Final Verification Questions:"""

################################################################## EXECUTE VERIFICATION PROMPTS ##################################################################
EXECUTE_PLAN_PROMPT_SEARCH_TOOL = """Answer the following question correctly based on the provided context. The question could be tricky as well, so think step by step and answer it correctly.

Context: {search_result}

Question: {verification_question}

Answer:"""


EXECUTE_PLAN_PROMPT_SELF_LLM = """Answer the following question correctly.

Question: {verification_question}

Answer:"""

EXECUTE_PLAN_PROMPT = "{verification_questions}"

################################################################## FINAL REFINED PROMPTS ##################################################################
FINAL_REFINED_PROMPT = """Given the below `Original Query` and `Baseline Answer`, analyze the `Verification Questions & Answers` to finally filter the refined answer.
Original Query: {original_question}
Baseline Answer: {baseline_response}

Verification Questions & Answer Pairs:
{verification_answers}

Final Refined Answer:"""

################################################################## ROUTER PROMPTS ##################################################################
ROUTER_CHAIN_PROMPT = """Please classify the below question in on of the following categories. The output should be a JSON as shown in the Examples.

Categories:
WIKI_CHAIN: Good for answering questions which asks for a list or set of entites as its answer. 
MULTI_CHAIN: Good for answering questions which  comprises of questions that have multiple independent answers (derived from a series of multiple discontiguous spans in the text) and multiple questions are asked in the original question.
LONG_CHAIN: Good for answering questions whose answer is long.

Examples:
WIKI_CHAIN:
    Question: Name some Endemic orchids of Vietnam.
    JSON Output: {{"category": "WIKI_CHAIN"}}
    Question: Who are the scientist won nobel prize in the year 1970?
    JSON Output: {{"category": "WIKI_CHAIN"}}
    Question: List some cricket players who are playing in indian cricket team.
    JSON Output: {{"category": "WIKI_CHAIN"}}
MULTI_CHAIN:
    Question: Who is known for developing the theory of relativity, and in which year was it introduced?
    JSON Output: {{"category": "MULTI_CHAIN"}}
    Question: Who is credited with inventing the telephone, and when did this invention take place?
    JSON Output: {{"category": "MULTI_CHAIN"}}
    Question: Who was the first person to orbit the Earth in space, and during which year did this historic event occur?
    JSON Output: {{"category": "MULTI_CHAIN"}}
LONG_CHAIN:
    Question: Write few lines about Einstein.
    JSON Output: {{"category": "LONG_CHAIN"}}
    Question: Tell me in short about first moon landing.
    JSON Output: {{"category": "LONG_CHAIN"}}
    Question: Write a short biography of Carl Marx.
    JSON Output: {{"category": "LONG_CHAIN"}}
    
Actual Question: {}
Final JSON Output:"""
