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
from app.api.models.DonghuaModel import DonghuaWatchResponse
from app.api.models.parser.DonghuaParser import DonghuaParser

router = APIRouter()
parser = DonghuaParser()

@router.get(
    "/watch/{slug}/{episode}",
    response_model=BaseResponse[DonghuaWatchResponse],
    summary="Watch Donghua Episode",
    description="Get streaming links and download options for a donghua episode"
)
async def watch_donghua_episode(
    slug: str,
    episode: str,
    apikey: str = Query(None, description="Optional")
):
    try:
        if not slug or slug.strip() == "":
            return ErrorResponse(
                status=400,
                success=False,
                message="Slug cannot be empty"
            )
            
        if not episode or episode.strip() == "":
            return ErrorResponse(
                status=400,
                success=False,
                message="Episode cannot be empty"
            )
            
        result = parser.parse_watch(slug.strip(), episode.strip())
        
        if "error" in result and result["error"]:
            return ErrorResponse(
                status=404,
                success=False,
                message=result["error"]
            )
            
        response_data = DonghuaWatchResponse(**result)
        
        return BaseResponse[DonghuaWatchResponse](
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