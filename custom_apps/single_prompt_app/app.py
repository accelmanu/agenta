from os import environ
import agenta as ag
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

default_prompt = "What is a good name for a company that makes {product}?"

LLM_MODELS = [
    "gpt-3.5-turbo",
    "gpt-4",
]

ag.init()
ag.config.default(
    prompt_template=ag.TextParam(default_prompt),
    model=ag.MultipleChoiceParam("gpt-3.5-turbo", LLM_MODELS),
    temperature=ag.FloatParam(default=0.5, minval=0, maxval=2),
    max_tokens=ag.IntParam(default=-1, minval=-1, maxval=16000),
    top_p=ag.FloatParam(default=1.0, minval=0, maxval=1),
    presence_penalty=ag.FloatParam(default=0.0, minval=-2, maxval=2),
    frequency_penalty=ag.FloatParam(default=0.0, minval=-2, maxval=2),
    force_json_response=ag.BinaryParam(False),
)


@ag.entrypoint
def generate(inputs: ag.DictInput = ag.DictInput(default_keys=["product"])) -> str:
    llm = ChatOpenAI(
        openai_api_base=environ.get("OPENAI_API_BASE"),
        openai_api_key=environ.get("OPENAI_API_KEY"),
        model=ag.config.model,
        temperature=ag.config.temperature,
        max_tokens=ag.config.max_tokens if ag.config.max_tokens != -1 else None,
        top_p=ag.config.top_p,
        presence_penalty=ag.config.presence_penalty,
        frequency_penalty=ag.config.frequency_penalty,
        model_kwargs={
            "response_format": {"type": "json_object"}
            if ag.config.force_json_response and ag.config.model == "gpt-4"
            else {"type": "text"}
        },
    )

    prompt = PromptTemplate(
        input_variables=["product"], template=ag.config.prompt_template
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    output = chain.run(**inputs)

    return output
