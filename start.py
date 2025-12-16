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

import uvicorn
from decouple import config

if __name__ == "__main__":
    host = config("HOST", default="0.0.0.0")
    port = config("PORT", default=8008, cast=int)
    debug = config("DEBUG", default=False, cast=bool)
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
        access_log=True
    )