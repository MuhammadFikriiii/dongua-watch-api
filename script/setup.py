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

#!/usr/bin/env python3
import os
import json
import secrets
import string
from pathlib import Path

def generate_secure_key(length=64):
    alphabet = string.ascii_letters + string.digits + "_-"
    return ''.join(secrets.choice(alphabet) for _ in range(length))
    
def setup_directories():
  
    directories = [
        "data",
        "data/logs",
        "data/logs/console", 
        "data/logs/ip_log",
        "data/logs/stats",
        "app/static/css"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")
        
def setup_config_files():
  
    free_keys_file = "data/free_keys.json"
    if not os.path.exists(free_keys_file):
        with open(free_keys_file, 'w') as f:
            json.dump({}, f, indent=2)
        print(f"✓ Created: {free_keys_file}")
    
    banned_file = "data/banned.json"
    if not os.path.exists(banned_file):
        with open(banned_file, 'w') as f:
            json.dump([], f, indent=2)
        print(f"✓ Created: {banned_file}")
    
    env_file = ".env"
    if not os.path.exists(env_file):
        adm_key = generate_secure_key(32)
        dev_key = generate_secure_key(32)
        own_key = generate_secure_key(32)
        env_content = f"""#
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

# Admin Privilege
ADM_KEY={adm_key}
DEV_KEY={dev_key}
OWN_KEY={own_key}

# Rate Limiting
GUEST_LIMIT_PER_MINUTE=60
FREE_LIMIT_PER_MINUTE=100

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Redis Configuration (Optional)
# REDIS_URL=redis://:password@host:port
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"✓ Created: {env_file}")
        print("Please review and edit the .env file with your preferred keys")
    else:
        print(f"✓ Already exists: {env_file}")
        
def create_static_files():
    css_file = "app/static/css/obsidian.css"
    if not os.path.exists(css_file):
        css_content = """
body {
    background: #0f0f23 !important;
    color: #e0e0e0 !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
}

.swagger-ui {
    background: #0f0f23 !important;
    color: #e0e0e0 !important;
}

.swagger-ui .topbar {
    display: none !important;
}

.swagger-ui .info {
    background: #1a1a2e !important;
    border: 1px solid #8b5cf6 !important;
    border-radius: 8px !important;
    padding: 20px !important;
    margin: 20px 0 !important;
}

.swagger-ui .info .title {
    color: #8b5cf6 !important;
    font-size: 2em !important;
    font-weight: bold !important;
    border-bottom: 2px solid #8b5cf6 !important;
    padding-bottom: 10px !important;
    margin-bottom: 15px !important;
}

.swagger-ui .opblock-tag {
    color: #8b5cf6 !important;
    font-size: 1.3em !important;
    font-weight: bold !important;
    border-bottom: 2px solid #8b5cf6 !important;
    padding: 10px 0 !important;
    margin: 20px 0 10px 0 !important;
}

.swagger-ui .opblock {
    background: #1a1a2e !important;
    border: 1px solid #2d2d4d !important;
    border-radius: 8px !important;
    margin: 10px 0 !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
}

.swagger-ui .opblock .opblock-summary-method {
    background: #8b5cf6 !important;
    color: white !important;
    font-weight: bold !important;
    border-radius: 4px !important;
    padding: 5px 10px !important;
    min-width: 80px !important;
    text-align: center !important;
}

.swagger-ui .opblock.opblock-get {
    border-left: 4px solid #8b5cf6 !important;
}

.swagger-ui .opblock.opblock-post {
    border-left: 4px solid #10b981 !important;
}

.swagger-ui .opblock.opblock-post .opblock-summary-method {
    background: #10b981 !important;
}

.swagger-ui .opblock.opblock-put {
    border-left: 4px solid #f59e0b !important;
}

.swagger-ui .opblock.opblock-put .opblock-summary-method {
    background: #f59e0b !important;
}

.swagger-ui .opblock.opblock-delete {
    border-left: 4px solid #ef4444 !important;
}

.swagger-ui .opblock.opblock-delete .opblock-summary-method {
    background: #ef4444 !important;
}
"""
        with open(css_file, 'w') as f:
            f.write(css_content)
        print(f"✓ Created: {css_file}")
        
def main():
    print("Setting up Anidong API...")
    print()
    setup_directories()
    print()
    setup_config_files()
    print()
    create_static_files()
    print()
    print("Setup completed successfully!")
    print()
    print("Next steps:")
    print("1. Review and edit the .env file if needed")
    print("2. Run: python script/setup_adm_key.py (optional)")
    print("3. Start the server: python start.py")
    print("4. Access the API at: http://localhost:8000")
    print("5. View documentation at: http://localhost:8000/docs")

if __name__ == "__main__":
    main()