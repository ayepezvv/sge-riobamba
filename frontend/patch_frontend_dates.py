import re

path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/app/(dashboard)/contratacion/procesos/page.tsx"
with open(path, "r") as f:
    content = f.read()

# Fix list view date
content = content.replace("valueGetter: (params) => params.value ? new Date(params.value).toLocaleString() : 'N/A'", "valueGetter: (params) => params.value ? new Date(params.value).toLocaleString('es-EC') : 'Sin fecha'")
content = content.replace("valueGetter: (params) => new Date(params.value).toLocaleString()", "valueGetter: (params) => params.value ? new Date(params.value).toLocaleString('es-EC') : 'Sin fecha'")

with open(path, "w") as f:
    f.write(content)

path2 = "/home/ayepez/.openclaw/workspace/sge/frontend/src/app/(dashboard)/contratacion/procesos/[id]/page.tsx"
with open(path2, "r") as f:
    content2 = f.read()

content2 = content2.replace("valueGetter: (params) => params.value ? new Date(params.value).toLocaleString() : 'N/A'", "valueGetter: (params) => params.value ? new Date(params.value).toLocaleString('es-EC') : 'Sin fecha'")
content2 = content2.replace("valueGetter: (params) => new Date(params.value).toLocaleString()", "valueGetter: (params) => params.value ? new Date(params.value).toLocaleString('es-EC') : 'Sin fecha'")

with open(path2, "w") as f:
    f.write(content2)
