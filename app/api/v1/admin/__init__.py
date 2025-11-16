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
from app.api.v1.admin.GenerateKey import router as generate_key_router
from app.api.v1.admin.RemoveKey import router as remove_key_router
from app.api.v1.admin.BanIp import router as ban_ip_router
from app.api.v1.admin.UnbanIp import router as unban_ip_router
from app.api.v1.admin.Health import router as health_router
from app.api.v1.admin.TotalReq import router as stats_router
from app.api.v1.admin.IpLog import router as ip_log_router
from app.api.v1.admin.Keys import router as keys_router

router = APIRouter()

router.include_router(generate_key_router, prefix="")
router.include_router(remove_key_router, prefix="")
router.include_router(ban_ip_router, prefix="")
router.include_router(unban_ip_router, prefix="")
router.include_router(health_router, prefix="")
router.include_router(stats_router, prefix="")
router.include_router(ip_log_router, prefix="")
router.include_router(keys_router, prefix="")