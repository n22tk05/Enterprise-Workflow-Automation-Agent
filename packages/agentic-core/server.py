from pydantic import BaseModel
from fastapi import FastAPI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

from src.agents.work_flow import app

class Request(BaseModel):
    message: str
    thread_id: str

api_app = FastAPI()

@api_app.post('/chat')
async def chat_endpoint(req: Request):
    inputs = {'messages': [HumanMessage(content=req.message)]}

    config = {'configurable': {'thread_id': req.thread_id}}
    result = await app.ainvoke(inputs, config=config)

    last_msg = result['messages'][-1]

    return {
        'thread_id': req.thread_id,
        'response': last_msg.content
    }



