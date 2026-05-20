from fastapi import APIRouter

from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import handle_chat


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:
    return await handle_chat(payload)
