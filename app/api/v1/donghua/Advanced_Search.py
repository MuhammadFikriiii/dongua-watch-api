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
from typing import Optional, List
from app.api.models.BaseResponse import BaseResponse, ErrorResponse
from app.api.models.DonghuaModel import DonghuaFiltersResponse, DonghuaListResponse
from app.api.models.parser.DonghuaParser import DonghuaParser

router = APIRouter()
parser = DonghuaParser()

@router.get(
    "/filters/value",
    response_model=BaseResponse[DonghuaFiltersResponse],
    summary="Advanced Search Filters",
    description="Get available filters for advanced donghua search"
)
async def get_donghua_filters(
    apikey: str = Query(None, description="Optional")
):
    try:
        result = parser.parse_advanced_search_filters()
        
        if "error" in result and result["error"]:
            return ErrorResponse(
                status=500,
                success=False,
                message=result["error"]
            )
            
        response_data = DonghuaFiltersResponse(**result)
        
        return BaseResponse[DonghuaFiltersResponse](
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
        
@router.get(
    "/filters/list-mode",
    response_model=BaseResponse[dict],
    summary="Advanced Search Text Mode",
    description="Get donghua list in text mode for advanced search"
)
async def get_donghua_filters_text_mode(
    apikey: str = Query(None, description="Optional")
):
    try:
        result = parser.parse_advanced_search_text()
        
        if "error" in result and result["error"]:
            return ErrorResponse(
                status=500,
                success=False,
                message=result["error"]
            )
            
        return BaseResponse[dict](
            status=200,
            success=True,
            data=result
        )
        
    except Exception as e:
        return ErrorResponse(
            status=500,
            success=False,
            message=f"Internal server error: {str(e)}"
        )
        
@router.get(
    "/filters",
    response_model=BaseResponse[DonghuaListResponse],
    summary="Advanced Search",
    description="Search donghua using advanced filters"
)
@router.get(
    "/filters/{page}",
    response_model=BaseResponse[DonghuaListResponse],
    summary="Advanced Search with Page",
    description="Search donghua using advanced filters with pagination"
)
async def advanced_search_donghua(
    status: Optional[str] = Query(None, description="Donghua status filter"),
    type: Optional[str] = Query(None, description="Donghua type filter"),
    sub: Optional[str] = Query(None, description="Subtitle filter"),
    order: Optional[str] = Query(None, description="Sort order"),
    genre: Optional[str] = Query(None, description="Genre filter (comma or + separated)"),
    studio: Optional[str] = Query(None, description="Studio filter (comma or + separated)"),
    season: Optional[str] = Query(None, description="Season filter (comma or + separated)"),
    page: str = "1",
    apikey: str = Query(None, description="Optional")
):
    try:
        filters = {}
        
        if status:
            filters["status"] = status
        if type:
            filters["type"] = type
        if sub:
            filters["sub"] = sub
        if order:
            filters["order"] = order
        if genre:
            filters["genre[]"] = genre.replace(',', '+')
        if studio:
            filters["studio[]"] = studio.replace(',', '+')
        if season:
            filters["season[]"] = season.replace(',', '+')
        
        result = parser.parse_advanced_search_image(filters, page)
        
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