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
import secrets
import base64
import string
import os
from pathlib import Path

def generate_secure_key(key_type="admin", length=64):
    alphabet = string.ascii_letters + string.digits + "_-"
    key = ''.join(secrets.choice(alphabet) for _ in range(length))
    key_bytes = key.encode('utf-8')
    base64_key = base64.urlsafe_b64encode(key_bytes).decode('utf-8').rstrip('=')
    
    return key, base64_key
    
def update_env_file(adm_key, dev_key, own_key):
    env_file = ".env"
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            lines = f.readlines()
            
        new_lines = []
        for line in lines:
            if line.startswith('ADM_KEY='):
                new_lines.append(f'ADM_KEY={adm_key}\n')
            elif line.startswith('DEV_KEY='):
                new_lines.append(f'DEV_KEY={dev_key}\n')
            elif line.startswith('OWN_KEY='):
                new_lines.append(f'OWN_KEY={own_key}\n')
            else:
                new_lines.append(line)
                
        with open(env_file, 'w') as f:
            f.writelines(new_lines)
    else:
      
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
            
def main():
    print("Generating secure API keys for Anidong API...")
    print()
    
    adm_key, adm_base64 = generate_secure_key("admin")
    dev_key, dev_base64 = generate_secure_key("dev") 
    own_key, own_base64 = generate_secure_key("owner")
    
    update_env_file(adm_key, dev_key, own_key)
    print("Updated .env file with new keys")
    print()

if __name__ == "__main__":
    main()