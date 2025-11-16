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
from urllib.parse import unquote
from app.api.models.BaseResponse import BaseResponse, ErrorResponse
from app.api.models.AnimeModel import AnimeSearchResponse
from app.api.models.parser.AnimeParser import AnimeParser

router = APIRouter()
parser = AnimeParser()

@router.get(
    "/search",
    response_model=BaseResponse[AnimeSearchResponse],
    summary="Search Anime",
    description="Search anime by query string"
)
@router.get(
    "/search/{page}",
    response_model=BaseResponse[AnimeSearchResponse],
    summary="Search Anime with Page",
    description="Search anime by query string with pagination"
)
async def search_anime(
    s: str = Query(..., description="Search query"),
    page: str = "1",
    apikey: str = Query(None, description="Optional")
):
    try:
        if not s or s.strip() == "":
            return ErrorResponse(
                status=400,
                success=False,
                message="Search query cannot be empty"
            )
            
        decoded_query = unquote(s.strip())
        result = parser.parse_search(decoded_query, page)
        
        if "error" in result and result["error"]:
            return ErrorResponse(
                status=500,
                success=False,
                message=result["error"]
            )
            
        response_data = AnimeSearchResponse(**result)
        
        return BaseResponse[AnimeSearchResponse](
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