import re
import os

path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/views/pages/landing/Header.tsx"
if not os.path.exists(path):
    path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/views/pages/landing/index.tsx"

if os.path.exists(path):
    with open(path, "r") as f:
        content = f.read()

    content = content.replace("Live Preview", "Ingresar al Sistema")
    content = content.replace('href="https://berrydashboard.io/"', 'href="/login"')

    with open(path, "w") as f:
        f.write(content)
else:
    print("Landing page not found")
