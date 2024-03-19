from os import environ
import agenta as ag
from langchain.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

DEFAULT_PROMPT = "You are brilliant in offering ideas to startups"

LLM_MODELS = [
    "gpt-3.5-turbo",
    "gpt-4",
]

ag.init()
ag.config.default(
    system_prompt=ag.TextParam(DEFAULT_PROMPT),
    model=ag.MultipleChoiceParam("gpt-3.5-turbo", LLM_MODELS),
    temperature=ag.FloatParam(default=0.5, minval=0, maxval=2),
    max_tokens=ag.IntParam(default=-1, minval=-1, maxval=16000),
    top_p=ag.FloatParam(default=1.0, minval=0, maxval=1),
    presence_penalty=ag.FloatParam(default=0.0, minval=-2, maxval=2),
    frequency_penalty=ag.FloatParam(default=0.0, minval=-2, maxval=2),
    force_json_response=ag.BinaryParam(False),
)


@ag.entrypoint
def generate(inputs: ag.MessagesInput = ag.MessagesInput([{"role": "user", "content": "Give 2 ideas on a tech based startup"}])):
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

    messages = [
        SystemMessage(content=ag.config.system_prompt),
    ] + inputs

    output = llm.invoke(messages)

    return {
        "message": output.content,
    }
