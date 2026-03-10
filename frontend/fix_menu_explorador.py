import re

path = "src/menu-items/contratacion.tsx"
with open(path, "r") as f:
    content = f.read()

# Add IconSearch to imports if not there
if "IconSearch" not in content:
    content = content.replace("IconReportMoney } from '@tabler/icons-react';", "IconReportMoney, IconSearch } from '@tabler/icons-react';")

new_item = """        { id: 'pac', title: 'Plan Anual (PAC)', type: 'item', url: '/contratacion/pac' },
        { id: 'pac_explorador', title: 'Explorador de Ítems', type: 'item', url: '/contratacion/pac/explorador', icon: IconSearch }"""

content = content.replace("{ id: 'pac', title: 'Plan Anual (PAC)', type: 'item', url: '/contratacion/pac' }", new_item)

with open(path, "w") as f:
    f.write(content)
