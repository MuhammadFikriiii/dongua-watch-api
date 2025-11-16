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

from typing import Any, Dict, Generic, TypeVar, Optional
from pydantic import BaseModel, Field

T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    status: int = Field(..., description="Kode Status HTTP")
    success: bool = Field(..., description="Pesan Sukses")
    author: str = Field("zhadev", description="my Gwej Name")
    data: Optional[T] = Field(None, description="Data ada jika Fetch Berhasil.")
    message: Optional[str] = Field(None, description="Pesan Error jika Data tidak ada.")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": 200,
                "success": True,
                "author": "zhadev",
                "data": {"example": "data"},
                "message": None
            }
        }
        
class ErrorResponse(BaseResponse[None]):
    data: None = None
    class Config:
        json_schema_extra = {
            "example": {
                "status": 400,
                "success": False,
                "author": "zhadev", 
                "data": None,
                "message": "Error message here"
            }
        }
