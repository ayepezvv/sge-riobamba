import re

path = "src/menu-items/administrativo.tsx"
with open(path, "r") as f:
    content = f.read()

# Add IconBriefcase
content = content.replace("import { IconUsers, IconBuildingCommunity, IconUserCircle } from '@tabler/icons-react';", "import { IconUsers, IconBuildingCommunity, IconUserCircle, IconBriefcase } from '@tabler/icons-react';")
content = content.replace("IconUserCircle: IconUserCircle", "IconUserCircle: IconUserCircle,\n  IconBriefcase: IconBriefcase")

new_item = """      url: '/administrativo/personal',
      icon: icons.IconUserCircle,
      breadcrumbs: false
    },
    {
      id: 'puestos',
      title: <FormattedMessage id="puestos" defaultMessage="Catálogo de Puestos" />,
      type: 'item',
      url: '/administrativo/puestos',
      icon: icons.IconBriefcase,
      breadcrumbs: false
    }"""
content = content.replace("""      url: '/administrativo/personal',
      icon: icons.IconUserCircle,
      breadcrumbs: false
    }""", new_item)

with open(path, "w") as f:
    f.write(content)
