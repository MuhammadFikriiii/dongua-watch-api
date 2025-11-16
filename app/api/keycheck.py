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

from fastapi import APIRouter, Query, HTTPException
from app.api.models.BaseResponse import BaseResponse, ErrorResponse
from app.api.models.AdminModel import KeyCheckResponse
from app.api.models.ApiKeyValidator import ApiKeyValidator

router = APIRouter()
api_key_validator = ApiKeyValidator()

@router.get(
    "/keycheck",
    response_model=BaseResponse[KeyCheckResponse],
    summary="Cek Apikey Kamu!",
    description="Cek Penggunaan Apikey Kamu!"
)
async def check_api_key(apikey: str = Query(..., description="Tulis Apikey Kamu Disini.")):
    try:
        key_stats = api_key_validator.get_key_stats(apikey)
        
        if not key_stats["valid"]:
            return ErrorResponse(
                status=401,
                success=False,
                message=key_stats["error"]
            )
            
        response_data = KeyCheckResponse(**key_stats)
        
        return BaseResponse[KeyCheckResponse](
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