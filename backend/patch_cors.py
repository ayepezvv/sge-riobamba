with open("app/main.py", "r") as f:
    content = f.read()

import re
content = re.sub(r'allow_origins=\[.*?\]', 'allow_origins=["http://192.168.1.15:3000", "http://localhost:3000"]', content)

with open("app/main.py", "w") as f:
    f.write(content)
