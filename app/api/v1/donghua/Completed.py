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
from app.api.models.DonghuaModel import DonghuaComletedResponse
from app.api.models.parser.DonghuaParser import DonghuaParser

router = APIRouter()
parser = DonghuaParser()

@router.get(
    "/completed",
    response_model=BaseResponse[DonghuaComletedResponse],
    summary="Completed Donghua",
    description="Get list of completed donghua series"
)
@router.get(
    "/completed/{page}",
    response_model=BaseResponse[DonghuaComletedResponse],
    summary="Completed Donghua with Page",
    description="Get list of completed donghua series with pagination"
)
async def get_completed_donghua(
    page: str = "1",
    apikey: str = Query(None, description="Optional")
):
    try:
        result = parser.parse_completed(page)
        
        if "error" in result and result["error"]:
            return ErrorResponse(
                status=500,
                success=False,
                message=result["error"]
            )
            
        response_data = DonghuaComletedResponse(**result)
        
        return BaseResponse[DonghuaComletedResponse](
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