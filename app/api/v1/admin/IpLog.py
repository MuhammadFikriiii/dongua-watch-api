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
import os
import json
from typing import List, Optional
from app.api.models.BaseResponse import BaseResponse, ErrorResponse
from app.api.models.AdminModel import IpLogsResponse
from app.api.models.ApiKeyValidator import ApiKeyValidator

router = APIRouter()

@router.get(
    "/ip_logs",
    response_model=BaseResponse[IpLogsResponse],
    summary="IP Logs",
    description="Get IP address access logs (Admin/Dev/Owner only)",
    include_in_schema=False
)
async def get_ip_logs(
    request: Request,
    ip: Optional[str] = Query(None, description="Specific IP address to filter logs"),
    limit: int = Query(100, description="Number of logs to return"),
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
        
        logs = []
        ip_log_dir = "data/logs/ip_log"
        
        if ip:
            ip_log_file = os.path.join(ip_log_dir, f"{ip}.json")
            if os.path.exists(ip_log_file):
                with open(ip_log_file, 'r') as f:
                    try:
                        ip_logs = json.load(f)
                        logs.extend(ip_logs[-limit:])
                    except json.JSONDecodeError:
                        pass
        else:
            for filename in os.listdir(ip_log_dir):
                if filename.endswith('.json'):
                    ip_log_file = os.path.join(ip_log_dir, filename)
                    with open(ip_log_file, 'r') as f:
                        try:
                            ip_logs = json.load(f)
                            logs.extend(ip_logs[-10:])
                        except json.JSONDecodeError:
                            pass
        
        logs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        logs = logs[:limit]
        
        response_data = IpLogsResponse(
            success=True,
            logs=logs,
            total_logs=len(logs)
        )
        
        return BaseResponse[IpLogsResponse](
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
