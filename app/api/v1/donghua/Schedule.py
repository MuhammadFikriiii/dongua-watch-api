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
from app.api.models.DonghuaModel import DonghuaScheduleResponse
from app.api.models.parser.DonghuaParser import DonghuaParser

router = APIRouter()
parser = DonghuaParser()

@router.get(
    "/schedule",
    response_model=BaseResponse[DonghuaScheduleResponse],
    summary="Donghua Schedule",
    description="Get weekly donghua release schedule"
)
async def get_donghua_schedule(
    apikey: str = Query(None, description="Optional")
):
    try:
        result = parser.parse_schedule()
        
        if "error" in result and result["error"]:
            return ErrorResponse(
                status=500,
                success=False,
                message=result["error"]
            )
            
        response_data = DonghuaScheduleResponse(**result)
        
        return BaseResponse[DonghuaScheduleResponse](
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