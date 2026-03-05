import re
path = "app/main.py"
with open(path, "r") as f:
    content = f.read()

content = re.sub(r'allow_origins=\[.*?\]', 'allow_origins=["*"]', content)

with open(path, "w") as f:
    f.write(content)
