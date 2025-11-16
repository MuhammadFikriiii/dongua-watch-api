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
from app.api.models.DonghuaModel import DonghuaHomeResponse
from app.api.models.parser.DonghuaParser import DonghuaParser

router = APIRouter()
parser = DonghuaParser()

@router.get(
    "/home",
    response_model=BaseResponse[DonghuaHomeResponse],
    summary="Donghua Homepage",
    description="Get donghua homepage content with popular, latest, and recommendations"
)
@router.get(
    "/home/{page}",
    response_model=BaseResponse[DonghuaHomeResponse],
    summary="Donghua Homepage with Page",
    description="Get donghua homepage content for specific page"
)
async def get_donghua_home(
    page: str = "1",
    apikey: str = Query(None, description="Optional")
):
    try:
        result = parser.parse_home(page)
        
        if "error" in result and result["error"]:
            return ErrorResponse(
                status=500,
                success=False,
                message=result["error"]
            )
            
        response_data = DonghuaHomeResponse(**result)
        
        return BaseResponse[DonghuaHomeResponse](
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