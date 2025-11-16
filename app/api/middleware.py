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

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.middleware.base import BaseHTTPMiddleware
from app.api.models.ApiKeyValidator import ApiKeyValidator

class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, data_dir: str = "data"):
        super().__init__(app)
        self.data_dir = data_dir
        self.logs_dir = os.path.join(data_dir, "logs")
        self.ip_log_dir = os.path.join(self.logs_dir, "ip_log")
        self._is_vercel = os.environ.get("VERCEL") == "1"
        
        if not self._is_vercel:
            self.ensure_directories()
            
    def ensure_directories(self):
        try:
            os.makedirs(self.ip_log_dir, exist_ok=True)
        except OSError:
            print("Could not create log directories, using in-memory logging")

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        client_ip = request.client.host
        user_agent = request.headers.get("user-agent", "")
        method = request.method
        url = str(request.url)
        path = request.url.path
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "ip": client_ip,
            "user_agent": user_agent,
            "method": method,
            "url": url,
            "path": path,
            "status_code": response.status_code,
            "process_time": process_time,
            "response_size": int(response.headers.get("content-length", 0))
        }
        
        if not self._is_vercel:
            self.log_ip_request(client_ip, log_data)
            
        return response
        
    def log_ip_request(self, ip: str, log_data: Dict[str, Any]):
        try:
            ip_log_file = os.path.join(self.ip_log_dir, f"{ip}.json")
            logs = []
            
            if os.path.exists(ip_log_file):
                with open(ip_log_file, 'r') as f:
                    try:
                        logs = json.load(f)
                    except json.JSONDecodeError:
                        logs = []
                        
            logs.append(log_data)
            
            if len(logs) > 1000:
                logs = logs[-1000:]
            
            with open(ip_log_file, 'w') as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            print(f"Error logging IP request: {e}")
            
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, api_key_validator: ApiKeyValidator):
        super().__init__(app)
        self.api_key_validator = api_key_validator
        self.rate_limits = {}
        self._is_vercel = os.environ.get("VERCEL") == "1"
        
        if self._is_vercel:
            self.banned_ips = set()
            print("🔧 Using in-memory banned IPs for Vercel")
        else:
            self.banned_ips = set(self.load_banned_ips())
            
    def load_banned_ips(self) -> List[str]:
        banned_file = os.path.join("data", "banned.json")
        if os.path.exists(banned_file):
            try:
                with open(banned_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
        
    def save_banned_ips(self):
        if not self._is_vercel:
            banned_file = os.path.join("data", "banned.json")
            try:
                with open(banned_file, 'w') as f:
                    json.dump(list(self.banned_ips), f, indent=2)
            except OSError:
                print("Could not save banned IPs")

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        
        if client_ip in self.banned_ips:
            return JSONResponse(
                status_code=403,
                content={
                    "status": 403,
                    "success": False,
                    "author": "zhsdevv",
                    "data": None,
                    "message": "IP address is banned"
                }
            )
            
        api_key = request.query_params.get("apikey")
        validation = self.api_key_validator.validate_key(api_key)
        
        if not validation["valid"]:
            return JSONResponse(
                status_code=401,
                content={
                    "status": 401,
                    "success": False,
                    "author": "zhsdevv",
                    "data": None,
                    "message": validation["error"]
                }
            )
            
        tier = validation["tier"]
        requests_per_minute = validation["requests_per_minute"]
        requests_per_second = validation.get("requests_per_second")
        
        rate_limit_key = f"{client_ip}:{tier}"
        current_time = time.time()
        
        if rate_limit_key not in self.rate_limits:
            self.rate_limits[rate_limit_key] = {
                "minute_requests": [],
                "second_requests": [],
                "last_cleanup": current_time
            }
            
        rate_data = self.rate_limits[rate_limit_key]
        
        if requests_per_second:
            current_second = int(current_time)
            second_requests = [t for t in rate_data["second_requests"] if t >= current_second - 1]
            
            if len(second_requests) >= requests_per_second:
                return JSONResponse(
                    status_code=429,
                    content={
                        "status": 429,
                        "success": False,
                        "author": "zhsdevv",
                        "data": None,
                        "message": "Rate limit exceeded: too many requests per second"
                    }
                )
                
            rate_data["second_requests"].append(current_second)
            rate_data["second_requests"] = second_requests[-requests_per_second:]
            
        current_minute = int(current_time / 60)
        minute_requests = [t for t in rate_data["minute_requests"] if t >= current_minute - 1]
        
        if len(minute_requests) >= requests_per_minute:
            return JSONResponse(
                status_code=429,
                content={
                    "status": 429,
                    "success": False,
                    "author": "zhsdevv",
                    "data": None,
                    "message": "Rate limit exceeded: too many requests per minute"
                }
            )
            
        rate_data["minute_requests"].append(current_minute)
        rate_data["minute_requests"] = minute_requests[-requests_per_minute:]
        
        if current_time - rate_data["last_cleanup"] > 300:
            self.cleanup_old_entries()
            rate_data["last_cleanup"] = current_time
            
        response = await call_next(request)
        return response
        
    def cleanup_old_entries(self):
        current_time = time.time()
        current_minute = int(current_time / 60)
        current_second = int(current_time)
        
        for key in list(self.rate_limits.keys()):
            rate_data = self.rate_limits[key]
            rate_data["minute_requests"] = [t for t in rate_data["minute_requests"] if t >= current_minute - 2]
            rate_data["second_requests"] = [t for t in rate_data["second_requests"] if t >= current_second - 2]
            
            if not rate_data["minute_requests"] and not rate_data["second_requests"]:
                del self.rate_limits[key]
                
    def ban_ip(self, ip: str):
        if ip not in self.banned_ips:
            self.banned_ips.add(ip)
            self.save_banned_ips()
            
    def unban_ip(self, ip: str):
        if ip in self.banned_ips:
            self.banned_ips.remove(ip)
            self.save_banned_ips()
            
    def get_banned_ips(self) -> List[str]:
        return list(self.banned_ips)
        
class StatsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, data_dir: str = "data"):
        super().__init__(app)
        self.data_dir = data_dir
        self.stats_dir = os.path.join(data_dir, "logs", "stats")
        self._is_vercel = os.environ.get("VERCEL") == "1"
        
        if not self._is_vercel:
            self.ensure_directories()
            
        self.stats = self.load_stats()
        
    def ensure_directories(self):
        try:
            os.makedirs(self.stats_dir, exist_ok=True)
        except OSError:
            print("Could not create stats directories, using in-memory stats")
            
    def load_stats(self) -> Dict[str, Any]:
        if self._is_vercel:
            return self._get_default_stats()
            
        stats_file = os.path.join(self.stats_dir, "api_stats.json")
        if os.path.exists(stats_file):
            try:
                with open(stats_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
              
        return self._get_default_stats()
        
    def _get_default_stats(self) -> Dict[str, Any]:
        return {
            "total_requests": 0,
            "unique_ips": set(),
            "requests_by_tier": {},
            "endpoint_requests": {},
            "start_time": datetime.now().isoformat()
        }
        
    def save_stats(self):
        if not self._is_vercel:
            stats_file = os.path.join(self.stats_dir, "api_stats.json")
            stats_to_save = self.stats.copy()
            stats_to_save["unique_ips"] = list(stats_to_save["unique_ips"])
            
            try:
                with open(stats_file, 'w') as f:
                    json.dump(stats_to_save, f, indent=2)
            except OSError:
                print("Could not save stats")
                
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        path = request.url.path
        api_key = request.query_params.get("apikey")
        
        response = await call_next(request)
        
        self.stats["total_requests"] += 1
        self.stats["unique_ips"].add(client_ip)
        
        from app.api.models.ApiKeyValidator import ApiKeyValidator
        validator = ApiKeyValidator()
        validation = validator.validate_key(api_key)
        tier = validation.get("tier", "guest")
        
        self.stats["requests_by_tier"][tier] = self.stats["requests_by_tier"].get(tier, 0) + 1
        self.stats["endpoint_requests"][path] = self.stats["endpoint_requests"].get(path, 0) + 1
        
        if self.stats["total_requests"] % 100 == 0 and not self._is_vercel:
            self.save_stats()
            
        return response
        
    def get_stats(self) -> Dict[str, Any]:
        stats = self.stats.copy()
        stats["unique_ips_count"] = len(stats["unique_ips"])
        stats["unique_ips"] = list(stats["unique_ips"])
        
        top_endpoints = sorted(
            stats["endpoint_requests"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        stats["top_endpoints"] = [
            {"endpoint": endpoint, "requests": count}
            for endpoint, count in top_endpoints
        ]
        
        return stats
