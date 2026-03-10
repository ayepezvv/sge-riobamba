import re

path = "src/layout/MainLayout/MenuList/NavGroup/index.tsx"
with open(path, "r") as f:
    content = f.read()

# The ternary operator is wrapped in {} but inside it we put more {} which causes object syntax error.
# {currentItem.id === lastItemId ? {'Más opciones'} : {currentItem.title}}
# should be:
# {currentItem.id === lastItemId ? 'Más opciones' : currentItem.title}

content = content.replace("{currentItem.id === lastItemId ? {'Más opciones'} : {currentItem.title}}", "{currentItem.id === lastItemId ? 'Más opciones' : currentItem.title}")

# Also let's check NavCollapse and NavItem for similar issues just in case
with open(path, "w") as f:
    f.write(content)
