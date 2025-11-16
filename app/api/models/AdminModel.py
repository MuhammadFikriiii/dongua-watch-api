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

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class GenerateKeyRequest(BaseModel):
    user: Optional[str] = Field(None, description="User identifier")
    keys: Optional[str] = Field(None, description="Custom API key")
    limit: int = Field(5000, description="Monthly request limit")
    apikey: str = Field(..., description="Admin API key")
    
class GenerateKeyResponse(BaseModel):
    success: bool
    key: Optional[str] = None
    user: Optional[str] = None
    monthly_limit: Optional[int] = None
    created_at: Optional[str] = None
    error: Optional[str] = None
    
class RemoveKeyRequest(BaseModel):
    keys: str = Field(..., description="API key to remove")
    apikey: str = Field(..., description="Admin API key")
    
class RemoveKeyResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    error: Optional[str] = None
    
class BanIpRequest(BaseModel):
    ip: str = Field(..., description="IP address to ban")
    apikey: str = Field(..., description="Admin API key")
    
class BanIpResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    error: Optional[str] = None
    
class UnbanIpRequest(BaseModel):
    ip: str = Field(..., description="IP address to unban")
    apikey: str = Field(..., description="Admin API key")
    
class UnbanIpResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    error: Optional[str] = None
    
class StatsResponse(BaseModel):
    success: bool
    total_requests: int
    unique_ips: int
    active_keys: int
    banned_ips: int
    requests_by_tier: Dict[str, int]
    top_endpoints: List[Dict[str, Any]]
    error: Optional[str] = None
    
class IpLogsResponse(BaseModel):
    success: bool
    logs: List[Dict[str, Any]]
    total_logs: int
    error: Optional[str] = None
    
class BannedIpsResponse(BaseModel):
    success: bool
    banned_ips: List[str]
    total_banned: int
    error: Optional[str] = None
    
class FreeKeysResponse(BaseModel):
    success: bool
    keys: Dict[str, Any]
    total_keys: int
    error: Optional[str] = None
    
class KeyCheckResponse(BaseModel):
    valid: bool
    key: Optional[str] = None
    tier: Optional[str] = None
    user: Optional[str] = None
    monthly_requests: Optional[int] = None
    total_requests: Optional[int] = None
    monthly_limit: Optional[int] = None
    created_at: Optional[str] = None
    last_used: Optional[str] = None
    is_active: Optional[bool] = None
    error: Optional[str] = None