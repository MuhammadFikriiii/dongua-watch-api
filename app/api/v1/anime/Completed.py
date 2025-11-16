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
from app.api.models.AnimeModel import AnimeListResponse
from app.api.models.parser.AnimeParser import AnimeParser

router = APIRouter()
parser = AnimeParser()

@router.get(
    "/completed",
    response_model=BaseResponse[AnimeListResponse],
    summary="Completed Anime",
    description="Get list of completed anime series"
)
@router.get(
    "/completed/{page}",
    response_model=BaseResponse[AnimeListResponse],
    summary="Completed Anime with Page",
    description="Get list of completed anime series with pagination"
)
async def get_completed_anime(
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
            
        response_data = AnimeListResponse(**result)
        
        return BaseResponse[AnimeListResponse](
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