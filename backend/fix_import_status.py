path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

content = content.replace("from fastapi import APIRouter, Depends, HTTPException", "from fastapi import APIRouter, Depends, HTTPException, status")

with open(path, "w") as f:
    f.write(content)
