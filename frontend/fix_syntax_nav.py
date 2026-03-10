import re

path = "src/layout/MainLayout/MenuList/NavCollapse/index.tsx"
with open(path, "r") as f:
    content = f.read()

# Fix the double brace issue
content = content.replace('title={{menu.title}}', 'title={menu.title}')

with open(path, "w") as f:
    f.write(content)

path2 = "src/layout/MainLayout/MenuList/NavItem/index.tsx"
with open(path2, "r") as f:
    content2 = f.read()

# Fix the double brace issue just in case
content2 = content2.replace('title={{item.title}}', 'title={item.title}')

with open(path2, "w") as f:
    f.write(content2)

path3 = "src/layout/MainLayout/MenuList/NavGroup/index.tsx"
with open(path3, "r") as f:
    content3 = f.read()

# Fix the double brace issue just in case
content3 = content3.replace('title={{item.title}}', 'title={item.title}')

with open(path3, "w") as f:
    f.write(content3)
