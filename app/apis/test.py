from fastapi import APIRouter, HTTPException, Depends, Form
from pydantic import BaseModel
from sqlmodel import Session
from app.database import get_session
from app.repositories.auth_repository import AuthRepository
from app.requests.thirdparty_ai_request import ThirdPartyAIRequest
from app.services.auth_service import AuthService
from app.apis.responses.signup_resp import SignUpResponse
from app.apis.responses.signin_resp import SignInResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class TestAICompletionParam(BaseModel):
    ai_model: str
    system_prompt: str
    request: str
    temperature: float

class TestAICompletionResponse(BaseModel):
    message: str

@router.post("/api/test/ai_summary", response_model=TestAICompletionResponse)
async def ai_summary(
    test_ai_completion_param: TestAICompletionParam
):
    ai_request = ThirdPartyAIRequest(test_ai_completion_param)
    result = await ai_request.summary(
        test_ai_completion_param.ai_model,
        test_ai_completion_param.system_prompt,
        test_ai_completion_param.request,
        test_ai_completion_param.temperature
    )
    return TestAICompletionResponse(message=result)
