path = "/home/ayepez/.openclaw/workspace/sge/backend/app/api/routes/administrativo.py"
with open(path, "r") as f:
    content = f.read()

content = content.replace("deps.get_current_active_user", "deps.get_current_user")
with open(path, "w") as f:
    f.write(content)
