path = "src/menu-items/catastro.tsx"
with open(path, "r") as f:
    content = f.read()

new_item = """{
      id: 'padron-ciudadanos',
      title: 'padron-ciudadanos',
      type: 'item',
      url: '/catastro/ciudadanos',
      icon: icons.IconAddressBook,
      breadcrumbs: false
    },
    {
      id: 'gestion-predios',
      title: 'gestion-predios',
      type: 'item',
      url: '/catastro/predios',
      icon: icons.IconMapPin,
      breadcrumbs: false
    }"""

content = content.replace("import { IconAddressBook } from '@tabler/icons-react';", "import { IconAddressBook, IconMapPin } from '@tabler/icons-react';")
content = content.replace("IconAddressBook: IconAddressBook", "IconAddressBook: IconAddressBook,\n  IconMapPin: IconMapPin")

import re
content = re.sub(r"\{\s*id: 'padron-ciudadanos'.*?\}\s*\}", new_item, content, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(content)
