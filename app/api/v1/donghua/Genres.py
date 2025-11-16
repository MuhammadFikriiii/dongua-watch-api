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
    "/genres/{slug}",
    response_model=BaseResponse[DonghuaListResponse],
    summary="Donghua by Genre",
    description="Get donghua list by genre"
)
@router.get(
    "/genres/{slug}/{page}",
    response_model=BaseResponse[DonghuaListResponse],
    summary="Donghua by Genre with Page",
    description="Get donghua list by genre with pagination"
)
async def get_donghua_by_genre(
    slug: str,
    page: str = "1",
    apikey: str = Query(None, description="Optional")
):
    try:
        if not slug or slug.strip() == "":
            return ErrorResponse(
                status=400,
                success=False,
                message="Genre slug cannot be empty"
            )
            
        result = parser.parse_genres(slug.strip(), page)
        
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