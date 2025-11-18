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

from fastapi import APIRouter, Query, Request
import psutil
import os
from datetime import datetime
from app.api.models.BaseResponse import BaseResponse, ErrorResponse
from app.api.models.ApiKeyValidator import ApiKeyValidator

router = APIRouter()

@router.get(
    "/health",
    response_model=BaseResponse[dict],
    summary="API Health Check",
    description="Get API health status and system information",
    include_in_schema=False
)
async def health_check(
    request: Request,
    apikey: str = Query(..., description="Admin API key for authorization")
):
    try:
        api_key_validator = request.app.state.api_key_validator
        admin_validation = api_key_validator.validate_key(apikey)
        if not admin_validation["valid"] or admin_validation["tier"] not in ["admin", "dev", "owner"]:
            return ErrorResponse(
                status=401,
                success=False,
                message="Invalid admin API key"
            )
        
        process = psutil.Process()
        memory_info = process.memory_info()

        stats_data = {}
        try:
            for middleware in request.app.user_middleware:
                if hasattr(middleware.cls, 'get_stats'):
                    stats_instance = middleware.cls(app=request.app)
                    stats_data = stats_instance.get_stats()
                    break
        except Exception as e:
            stats_data = {
                "total_requests": 0,
                "unique_ips_count": 0,
                "start_time": datetime.now().isoformat()
            }
        
        health_data = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "system": {
                "cpu_percent": psutil.cpu_percent(),
                "memory_usage_mb": round(memory_info.rss / 1024 / 1024, 2),
                "memory_percent": round(process.memory_percent(), 2),
                "disk_usage": {
                    "total": getattr(psutil.disk_usage('/'), 'total', 0),
                    "used": getattr(psutil.disk_usage('/'), 'used', 0),
                    "free": getattr(psutil.disk_usage('/'), 'free', 0),
                    "percent": getattr(psutil.disk_usage('/'), 'percent', 0)
                } if hasattr(psutil, 'disk_usage') else {},
                "uptime_seconds": int(psutil.boot_time()) if hasattr(psutil, 'boot_time') else 0
            },
            "api": {
                "total_requests": stats_data.get("total_requests", 0),
                "unique_ips": stats_data.get("unique_ips_count", 0),
                "start_time": stats_data.get("start_time", datetime.now().isoformat())
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
