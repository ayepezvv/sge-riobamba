import re

path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/layout/MainLayout/MenuList/index.tsx"
with open(path, "r") as f:
    content = f.read()

# Replace <List key={item.id}>
content = content.replace("<List key={item.id}>", "<List key={`${item.id}-${index}`}>")

# Replace <NavGroup key={item.id}
content = content.replace("key={item.id}", "key={`${item.id}-${index}`}")

with open(path, "w") as f:
    f.write(content)
