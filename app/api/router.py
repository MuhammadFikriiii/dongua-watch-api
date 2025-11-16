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

from fastapi import APIRouter
from app.api.v1.anime import router as anime_router
from app.api.v1.donghua import router as donghua_router
from app.api.v1.admin import router as admin_router
from app.api.keycheck import router as keycheck_router

public_router = APIRouter()
private_router = APIRouter()

public_router.include_router(anime_router, prefix="/anime", tags=["Anime"])
public_router.include_router(donghua_router, prefix="/donghua", tags=["Donghua"])
public_router.include_router(keycheck_router, prefix="", tags=["Key Management"])

private_router.include_router(admin_router, prefix="/admin", tags=["Admin"])