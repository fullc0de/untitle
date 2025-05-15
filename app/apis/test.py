from fastapi import APIRouter
from pydantic import BaseModel
from app.requests.prompt_context import PromptContext
from app.requests.thirdparty_ai_request import ThirdPartyAIRequest
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
    prompt_context = PromptContext()
    prompt_context.summary_prompt_template = test_ai_completion_param.system_prompt
    ai_request = ThirdPartyAIRequest(prompt_context)
    result = await ai_request.summary(
        test_ai_completion_param.ai_model,
        test_ai_completion_param.request,
        test_ai_completion_param.temperature
    )
    return TestAICompletionResponse(message=result)
