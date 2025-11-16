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

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
import os
from decouple import config

from app.api.router import public_router, private_router
from app.api.middleware import LoggingMiddleware, RateLimitMiddleware, StatsMiddleware
from app.api.models.ApiKeyValidator import ApiKeyValidator

description = f"""
### About
- **Github**: [Anidong](https://github.com/zhadevv/anidong-api)
- **Version**: `v1.0.0`

### Credit
- Project ini terinspirasi dari bang Sanka yang udh bnyk ngebuat Api kayak Anime, Donghua, Komik, Dll.
- Project ini dibangun atas dasar gabut aja si🗿
"""
version = f"1.0.0"
tags_metadata = [
    {
        "name": "Anime",
        "description": "Anime Api Endpoint",
    },
    {
        "name": "Donghua",
        "description": "Donghua Api Endpoint",
    },
    {
        "name": "Key Management", 
        "description": "Api Key Management",
    },
]

api_key_validator = ApiKeyValidator()

app = FastAPI(
    title="Anidong Api",
    description=description,
    version=version,
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/api/v1/openapi.json",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "docExpansion": "none",
        "filter": True,
        "showExtensions": True,
        "showCommonExtensions": True,
        "syntaxHighlight": {
            "theme": "obsidian"
        }
    },
    swagger_favicon_url=""
)

api_key_validator = ApiKeyValidator()
rate_limit_middleware = RateLimitMiddleware(app, api_key_validator)
stats_middleware = StatsMiddleware(app)

app.state.api_key_validator = api_key_validator
app.state.stats_middleware = stats_middleware
app.state.rate_limit_middleware = rate_limit_middleware

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(LoggingMiddleware)
app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(lambda app: rate_limit_middleware)
app.add_middleware(lambda app: stats_middleware)

app.include_router(public_router, prefix="/api/v1")
app.include_router(private_router, prefix="/api/v1")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/api/v1/openapi.json",
        title="Anidong Api",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "docExpansion": "none",
            "filter": True,
            "showExtensions": True,
            "showCommonExtensions": True,
            "syntaxHighlight": {
                "theme": "obsidian"
            }
        },
        swagger_favicon_url="",
        swagger_css_url="/static/css/obsidian.css"
    )
    
@app.get("/")
async def root():
    return {
        "message": "Welcome to Anidong Api",
        "version": "1.0.0",
        "author": "zhadevv",
        "docs": "/docs",
        "endpoints": {
            "anime": "/api/v1/anime",
            "donghua": "/api/v1/donghua",
            "key_check": "/api/v1/keycheck"
        }
    }
    
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "status": 404,
            "success": False,
            "author": "zhadevv",
            "data": None,
            "message": "Endpoint not found"
        }
    )
    
@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "status": 500,
            "success": False,
            "author": "zhadevv",
            "data": None,
            "message": "Internal server error"
        }
    )
    
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Anidong Api",
        version=version,
        description=description,
        routes=app.routes,
    )
    
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "query",
            "name": "apikey",
            "description": "Kalo udah punya aja, Guest ga perlu Apikey."
        }
    }
    
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if method in ["get", "post", "put", "delete"]:
                openapi_schema["paths"][path][method]["security"] = [{"ApiKeyAuth": []}]
                
    app.openapi_schema = openapi_schema
    return app.openapi_schema
    
app.openapi = custom_openapi

app = app
