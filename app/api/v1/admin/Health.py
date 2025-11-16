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
import psutil
import os
from datetime import datetime
from app.api.models.BaseResponse import BaseResponse, ErrorResponse

router = APIRouter()

@router.get(
    "/health",
    response_model=BaseResponse[dict],
    summary="API Health Check",
    description="Get API health status and system information",
    include_in_schema=False
)
async def health_check(
    apikey: str = Query(..., description="Admin API key for authorization")
):
    try:
        from app.main import rate_limit_middleware
        
        admin_validation = rate_limit_middleware.api_key_validator.validate_key(apikey)
        if not admin_validation["valid"] or admin_validation["tier"] not in ["admin", "dev", "owner"]:
            return ErrorResponse(
                status=401,
                success=False,
                message="Invalid admin API key"
            )
        
        process = psutil.Process()
        memory_info = process.memory_info()
        
        health_data = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "system": {
                "cpu_percent": psutil.cpu_percent(),
                "memory_usage_mb": memory_info.rss / 1024 / 1024,
                "memory_percent": process.memory_percent(),
                "disk_usage": psutil.disk_usage('/')._asdict(),
                "uptime_seconds": psutil.boot_time()
            },
            "api": {
                "total_requests": getattr(rate_limit_middleware.stats_middleware.stats, "total_requests", 0),
                "unique_ips": len(getattr(rate_limit_middleware.stats_middleware.stats, "unique_ips", set())),
                "start_time": getattr(rate_limit_middleware.stats_middleware.stats, "start_time", datetime.now().isoformat())
            }
        }
        
        return BaseResponse[dict](
            status=200,
            success=True,
            data=health_data
        )
        
    except Exception as e:
        return ErrorResponse(
            status=500,
            success=False,
            message=f"Internal server error: {str(e)}"
        )