import re

path = "src/layout/MainLayout/MenuList/NavCollapse/index.tsx"
with open(path, "r") as f:
    content = f.read()

# Replace <FormattedMessage id={menu.title} /> with {menu.title}
content = content.replace("<FormattedMessage id={menu.title} />", "{menu.title}")

# Replace <FormattedMessage id={menu.caption} /> with {menu.caption}
content = content.replace("<FormattedMessage id={menu.caption} />", "{menu.caption}")

with open(path, "w") as f:
    f.write(content)
