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
from app.api.models.AnimeModel import AnimeHomeResponse
from app.api.models.parser.AnimeParser import AnimeParser

router = APIRouter()
parser = AnimeParser()

@router.get(
    "/home",
    response_model=BaseResponse[AnimeHomeResponse],
    summary="Anime Homepage",
    description="Get anime homepage content with popular, latest, and recommendations"
)
@router.get(
    "/home/{page}",
    response_model=BaseResponse[AnimeHomeResponse],
    summary="Anime Homepage with Page",
    description="Get anime homepage content for specific page"
)
async def get_anime_home(
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
            
        response_data = AnimeHomeResponse(**result)
        
        return BaseResponse[AnimeHomeResponse](
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