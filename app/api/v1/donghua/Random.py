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
from app.api.models.DonghuaModel import DonghuaRandomResponse
from app.api.models.parser.DonghuaParser import DonghuaParser

router = APIRouter()
parser = DonghuaParser()

@router.get(
    "/random",
    response_model=BaseResponse[DonghuaRandomResponse],
    summary="Random Donghua",
    description="Get a random donghua series with full details"
)
async def get_random_donghua(
    apikey: str = Query(None, description="Optional")
):
    try:
        result = parser.get_random()
        
        if "error" in result and result["error"]:
            return ErrorResponse(
                status=500,
                success=False,
                message=result["error"]
            )
            
        response_data = DonghuaRandomResponse(**result)
        
        return BaseResponse[DonghuaRandomResponse](
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