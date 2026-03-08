import re
path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/menu-items/contratacion.tsx"
with open(path, "r") as f:
    content = f.read()

new_item = """{
      id: 'mis-procesos',
      title: 'mis-procesos',
      type: 'item',
      url: '/contratacion/procesos',
      icon: icons.IconFileAnalytics,
      breadcrumbs: false
    },
    {
      id: 'admin-plantillas',
      title: 'admin-plantillas',
      type: 'item',
      url: '/contratacion/administracion',
      icon: icons.IconBriefcase,
      breadcrumbs: false
    }"""

content = re.sub(r"\{\s*id: 'mis-procesos'.*?\}\s*\}", new_item, content, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(content)
