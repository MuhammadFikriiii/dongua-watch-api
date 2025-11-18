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

from fastapi import APIRouter, Query, Request, HTTPException
from app.api.models.BaseResponse import BaseResponse, ErrorResponse
from app.api.models.AdminModel import GenerateKeyRequest, GenerateKeyResponse
from app.api.models.ApiKeyValidator import ApiKeyValidator

router = APIRouter()
api_key_validator = ApiKeyValidator()

@router.get(
    "/generate_key",
    response_model=BaseResponse[GenerateKeyResponse],
    summary="Generate API Key",
    description="Generate a new API key (Admin/Dev/Owner only)",
    include_in_schema=False
)
async def generate_api_key(
    request: Request,
    user: str = Query(None, description="User identifier"),
    keys: str = Query(None, description="Custom API key"),
    limit: int = Query(5000, description="Monthly request limit"),
    apikey: str = Query(..., description="Admin API key for authorization")
):
    try:
        result = api_key_validator.generate_key(user, keys, limit, apikey)
        
        if not result["success"]:
            return ErrorResponse(
                status=400,
                success=False,
                message=result["error"]
            )
        
        response_data = GenerateKeyResponse(**result)
        
        return BaseResponse[GenerateKeyResponse](
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
        
