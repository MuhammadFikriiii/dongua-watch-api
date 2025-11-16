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
from app.api.models.AnimeModel import AnimeRandomResponse
from app.api.models.parser.AnimeParser import AnimeParser

router = APIRouter()
parser = AnimeParser()

@router.get(
    "/random",
    response_model=BaseResponse[AnimeRandomResponse],
    summary="Random Anime",
    description="Get a random anime series with full details"
)
async def get_random_anime(
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
            
        response_data = AnimeRandomResponse(**result)
        
        return BaseResponse[AnimeRandomResponse](
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