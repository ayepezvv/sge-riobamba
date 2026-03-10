import re

path = "src/layout/MainLayout/MenuList/NavItem/index.tsx"
with open(path, "r") as f:
    content = f.read()

# Replace <FormattedMessage id={item.title} /> with {item.title}
content = content.replace("<FormattedMessage id={item.title} />", "{item.title}")

# Replace <FormattedMessage id={item.caption} /> with {item.caption}
content = content.replace("<FormattedMessage id={item.caption} />", "{item.caption}")

with open(path, "w") as f:
    f.write(content)
