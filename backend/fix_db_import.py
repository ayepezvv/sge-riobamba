path = "app/api/routes/informatica.py"
import os
if os.path.exists(path):
    with open(path, "r") as f:
        content = f.read()
    content = content.replace("from app.db.session import get_db", "from app.api.deps import get_db")
    with open(path, "w") as f:
        f.write(content)
