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
from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from dotenv import load_dotenv
import redis

load_dotenv()

class ApiKeyTier(BaseModel):
    name: str
    monthly_limit: int
    requests_per_minute: int
    requests_per_second: Optional[int] = None

class ApiKeyData(BaseModel):
    key: str
    tier: str
    user: Optional[str] = None
    monthly_requests: int = 0
    total_requests: int = 0
    created_at: str
    last_used: Optional[str] = None
    is_active: bool = True

class ApiKeyValidator:
    TIERS = {
        "guest": ApiKeyTier(name="guest", monthly_limit=1000, requests_per_minute=60),
        "free": ApiKeyTier(name="free", monthly_limit=5000, requests_per_minute=100),
        "admin": ApiKeyTier(name="admin", monthly_limit=100000, requests_per_minute=1000),
        "dev": ApiKeyTier(name="dev", monthly_limit=-1, requests_per_minute=1000, requests_per_second=1000),
        "owner": ApiKeyTier(name="owner", monthly_limit=-1, requests_per_minute=10000, requests_per_second=10000)
    }

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.free_keys_file = os.path.join(data_dir, "free_keys.json")
        
        self.redis_url = os.getenv("REDIS_URL")
        self.redis_client = None
        self._init_redis()
        
        self.admin_keys = {
            "admin": os.getenv("ADM_KEY", ""),
            "dev": os.getenv("DEV_KEY", ""),
            "owner": os.getenv("OWN_KEY", "")
        }
        
        self.free_keys = self._load_free_keys()

    def _init_redis(self):
        try:
            if self.redis_url:
                self.redis_client = redis.from_url(self.redis_url)
        except Exception as e:
            print(f"Redis connection failed: {e}")

    def _load_free_keys(self) -> Dict[str, Any]:
        try:
            if self.redis_client:
                keys_data = self.redis_client.get("api_free_keys")
                if keys_data:
                    return json.loads(keys_data)
        except Exception as e:
            print(f"Failed to load from Redis: {e}")
        
        return {}

    def _save_free_keys(self):
        try:
            if self.redis_client:
                self.redis_client.set("api_free_keys", json.dumps(self.free_keys))
                return True
        except Exception as e:
            print(f"Failed to save to Redis: {e}")
        
        return False

    def validate_key(self, api_key: Optional[str]) -> Dict[str, Any]:
        if not api_key:
            return {
                "valid": True,
                "tier": "guest",
                "monthly_limit": self.TIERS["guest"].monthly_limit,
                "requests_per_minute": self.TIERS["guest"].requests_per_minute
            }

        if api_key in self.free_keys:
            key_data = self.free_keys[api_key]
            if not key_data.get("is_active", True):
                return {"valid": False, "error": "API key is inactive"}
            
            tier_name = key_data.get("tier", "free")
            if tier_name not in self.TIERS:
                tier_name = "free"
            
            tier = self.TIERS[tier_name]
            
            if tier.monthly_limit != -1 and key_data.get("monthly_requests", 0) >= tier.monthly_limit:
                return {"valid": False, "error": "Monthly limit exceeded"}
            
            key_data["last_used"] = datetime.now().isoformat()
            key_data["total_requests"] = key_data.get("total_requests", 0) + 1
            key_data["monthly_requests"] = key_data.get("monthly_requests", 0) + 1
            
            self.free_keys[api_key] = key_data
            self._save_free_keys()
            
            return {
                "valid": True,
                "tier": tier_name,
                "monthly_limit": tier.monthly_limit,
                "requests_per_minute": tier.requests_per_minute,
                "requests_per_second": tier.requests_per_second,
                "user": key_data.get("user"),
                "monthly_requests": key_data.get("monthly_requests", 0),
                "total_requests": key_data.get("total_requests", 0)
            }

        for tier_name, env_key in self.admin_keys.items():
            if env_key and api_key == env_key:
                tier = self.TIERS[tier_name]
                return {
                    "valid": True,
                    "tier": tier_name,
                    "monthly_limit": tier.monthly_limit,
                    "requests_per_minute": tier.requests_per_minute,
                    "requests_per_second": tier.requests_per_second
                }

        return {"valid": False, "error": "Invalid API key"}

    def generate_key(self, user: Optional[str] = None, custom_key: Optional[str] = None, 
                    limit: int = 5000, admin_key: str = None) -> Dict[str, Any]:
        admin_validation = self.validate_key(admin_key)
        if not admin_validation["valid"] or admin_validation["tier"] not in ["admin", "dev", "owner"]:
            return {"success": False, "error": "Invalid admin API key"}

        if custom_key:
            if custom_key in self.free_keys:
                return {"success": False, "error": "Custom key already exists"}
            new_key = custom_key
        else:
            import secrets
            import string
            characters = string.ascii_letters + string.digits
            new_key = f"SK_Free_Anidong_Keys_{''.join(secrets.choice(characters) for _ in range(16))}"

        key_data = {
            "key": new_key,
            "tier": "free",
            "user": user,
            "monthly_limit": limit,
            "monthly_requests": 0,
            "total_requests": 0,
            "created_at": datetime.now().isoformat(),
            "last_used": None,
            "is_active": True
        }

        self.free_keys[new_key] = key_data
        self._save_free_keys()

        return {
            "success": True,
            "key": new_key,
            "user": user,
            "monthly_limit": limit,
            "created_at": key_data["created_at"]
        }

    def remove_key(self, key: str, admin_key: str) -> Dict[str, Any]:
        admin_validation = self.validate_key(admin_key)
        if not admin_validation["valid"] or admin_validation["tier"] not in ["admin", "dev", "owner"]:
            return {"success": False, "error": "Invalid admin API key"}

        if key in self.free_keys:
            del self.free_keys[key]
            self._save_free_keys()
            return {"success": True, "message": "Key removed successfully"}
        else:
            return {"success": False, "error": "Key not found"}

    def get_key_stats(self, api_key: str) -> Dict[str, Any]:
        validation = self.validate_key(api_key)
        if not validation["valid"]:
            return validation

        if api_key in self.free_keys:
            key_data = self.free_keys[api_key]
            return {
                "valid": True,
                "key": api_key,
                "tier": key_data.get("tier", "free"),
                "user": key_data.get("user"),
                "monthly_requests": key_data.get("monthly_requests", 0),
                "total_requests": key_data.get("total_requests", 0),
                "monthly_limit": key_data.get("monthly_limit", 5000),
                "created_at": key_data.get("created_at"),
                "last_used": key_data.get("last_used"),
                "is_active": key_data.get("is_active", True)
            }

        return {
            "valid": True,
            "key": api_key,
            "tier": validation["tier"],
            "monthly_requests": 0,
            "total_requests": 0,
            "monthly_limit": validation["monthly_limit"]
        }

    def reset_monthly_limits(self):
        current_month = datetime.now().strftime("%Y-%m")
        for key_data in self.free_keys.values():
            created_month = datetime.fromisoformat(key_data["created_at"]).strftime("%Y-%m")
            if created_month != current_month:
                key_data["monthly_requests"] = 0
        self._save_free_keys()

    def get_all_free_keys(self, admin_key: str) -> Dict[str, Any]:
        admin_validation = self.validate_key(admin_key)
        if not admin_validation["valid"] or admin_validation["tier"] not in ["admin", "dev", "owner"]:
            return {"success": False, "error": "Invalid admin API key"}

        return {
            "success": True,
            "keys": self.free_keys,
            "total_keys": len(self.free_keys)
        }
