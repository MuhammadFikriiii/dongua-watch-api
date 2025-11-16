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
from app.api.v1.anime.Home import router as home_router
from app.api.v1.anime.Schedule import router as schedule_router
from app.api.v1.anime.Search import router as search_router
from app.api.v1.anime.Ongoing import router as ongoing_router
from app.api.v1.anime.Completed import router as completed_router
from app.api.v1.anime.Az_List import router as az_list_router
from app.api.v1.anime.Random import router as random_router
from app.api.v1.anime.Detail import router as detail_router
from app.api.v1.anime.Watch import router as watch_router
from app.api.v1.anime.Advanced_Search import router as advanced_search_router

router = APIRouter()

router.include_router(home_router, prefix="")
router.include_router(schedule_router, prefix="")
router.include_router(search_router, prefix="")
router.include_router(ongoing_router, prefix="")
router.include_router(completed_router, prefix="")
router.include_router(az_list_router, prefix="")
router.include_router(random_router, prefix="")
router.include_router(detail_router, prefix="")
router.include_router(watch_router, prefix="")
router.include_router(advanced_search_router, prefix="")