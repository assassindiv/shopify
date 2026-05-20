from fastapi import APIRouter

from app.models.return_request import ReturnCheckRequest, ReturnCheckResponse
from app.services.return_service import check_return


router = APIRouter(prefix="/returns", tags=["returns"])


@router.post("/check", response_model=ReturnCheckResponse)
def check_return_request(payload: ReturnCheckRequest) -> ReturnCheckResponse:
    return check_return(payload)
