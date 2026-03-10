import glob
import os

pages = glob.glob("src/app/(dashboard)/administrativo/*/page.tsx") + ["src/app/(dashboard)/contratacion/pac/page.tsx", "src/app/(dashboard)/contratacion/procesos/page.tsx"]

for page in pages:
    with open(page, "r") as f:
        content = f.read()

    # Replace GET fetch
    content = content.replace("const res = await fetch('http://192.168.1.15:8000/api/", "const res = await fetch('http://192.168.1.15:8000/api/", 1) # dummy
    
    import re
    # Add token to GET fetch
    content = re.sub(
        r"await fetch\('http://192\.168\.1\.15:8000/api/([^']*)'\);", 
        r"await fetch('http://192.168.1.15:8000/api/\1', { headers: { 'Authorization': `Bearer ${window.localStorage.getItem('serviceToken')}` } });", 
        content
    )
    
    # Add token to POST/PUT fetch (this one has headers: {'Content-Type': 'application/json'})
    content = content.replace(
        "headers: { 'Content-Type': 'application/json' }", 
        "headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${window.localStorage.getItem('serviceToken')}` }"
    )
    
    # Add token to DELETE fetch (this one might not have headers)
    content = re.sub(
        r"await fetch\(`http://192\.168\.1\.15:8000/api/([^`]*)`, { method: 'DELETE' }\);",
        r"await fetch(`http://192.168.1.15:8000/api/\1`, { method: 'DELETE', headers: { 'Authorization': `Bearer ${window.localStorage.getItem('serviceToken')}` } });",
        content
    )

    with open(page, "w") as f:
        f.write(content)
        
