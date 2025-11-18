#
#             Zhadevv Project
#             --MIT License--
#
# Feed Me Starnya Bang:>
# Project 100% Open Source
# Bebas Recode, Deploy Production. KECUALI
# Diperjual-Belikan.
#
# Project ini Sepenuhnya Gratis, Makannua ksih Bintang Dong anj:>
# *bercanda ajahh
#
# Regards
# Zhadevv
#

from fastapi import APIRouter, Query, Request
from app.api.models.BaseResponse import BaseResponse, ErrorResponse
from app.api.models.AdminModel import RemoveKeyRequest, RemoveKeyResponse
from app.api.models.ApiKeyValidator import ApiKeyValidator

router = APIRouter()

@router.delete(
    "/remove_keys",
    response_model=BaseResponse[RemoveKeyResponse],
    summary="Remove API Key",
    description="Remove an existing API key (Admin/Dev/Owner only)",
    include_in_schema=False
)
async def remove_api_key(
    request: Request,
    keys: str = Query(..., description="API key to remove"),
    apikey: str = Query(..., description="Admin API key for authorization")
):
    try:
        api_key_validator = request.app.state.api_key_validator
        result = api_key_validator.remove_key(keys, apikey)
        
        if not result["success"]:
            return ErrorResponse(
                status=400,
                success=False,
                message=result["error"]
            )
        
        response_data = RemoveKeyResponse(**result)
        
        return BaseResponse[RemoveKeyResponse](
            status=200,
            success=True,
            data=response_data
        )
        
    except Exception as e:
        return ErrorResponse(
            status=500,
            success=False,
            message=f"Internal server error: {str(e)}"
        )
