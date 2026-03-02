import re

path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/views/pages/authentication/jwt/AuthLogin.tsx"
with open(path, "r") as f:
    content = f.read()

content = content.replace("Sign in", "Ingresar")
content = content.replace("Sign In", "{isSubmitting ? 'Iniciando sesión...' : 'Ingresar'}")

with open(path, "w") as f:
    f.write(content)
