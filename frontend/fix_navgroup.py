import re

path = "src/layout/MainLayout/MenuList/NavGroup/index.tsx"
with open(path, "r") as f:
    content = f.read()

# Replace <FormattedMessage id={currentItem.title} /> with {currentItem.title}
content = content.replace("<FormattedMessage id={currentItem.title} />", "{currentItem.title}")

# Replace <FormattedMessage id={currentItem.caption} /> with {currentItem.caption}
content = content.replace("<FormattedMessage id={currentItem.caption} />", "{currentItem.caption}")

# Replace <FormattedMessage id={item.title} /> with {item.title}
content = content.replace("<FormattedMessage id={item.title} />", "{item.title}")

# Replace <FormattedMessage id={item.caption} /> with {item.caption}
content = content.replace("<FormattedMessage id={item.caption} />", "{item.caption}")

# Replace <FormattedMessage id="more-items" /> with {'Más opciones'}
content = content.replace('<FormattedMessage id="more-items" />', "{'Más opciones'}")

with open(path, "w") as f:
    f.write(content)
