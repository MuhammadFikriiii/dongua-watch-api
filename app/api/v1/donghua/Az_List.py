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
from app.api.models.DonghuaModel import DonghuaListResponse
from app.api.models.parser.DonghuaParser import DonghuaParser

router = APIRouter()
parser = DonghuaParser()

@router.get(
    "/a-z",
    response_model=BaseResponse[DonghuaListResponse],
    summary="Donghua A-Z List",
    description="Get donghua list in alphabetical order"
)
@router.get(
    "/a-z/{page}",
    response_model=BaseResponse[DonghuaListResponse],
    summary="Donghua A-Z List with Page",
    description="Get donghua list in alphabetical order with pagination"
)
@router.get(
    "/a-z/{show}/{page}",
    response_model=BaseResponse[DonghuaListResponse],
    summary="Donghua A-Z List by Show",
    description="Get donghua list by specific show letter with pagination"
)
async def get_az_donghua(
    show: str = None,
    page: str = "1",
    apikey: str = Query(None, description="Optional")
):
    try:
        result = parser.parse_az_list(show, page)
        
        if "error" in result and result["error"]:
            return ErrorResponse(
                status=500,
                success=False,
                message=result["error"]
            )
            
        response_data = DonghuaListResponse(**result)
        
        return BaseResponse[DonghuaListResponse](
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