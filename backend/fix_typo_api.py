path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

# Ah, I replaced "ProcesoItemPacLinkCreate" with "ProcesoItemPacLinkCreate, ReformaPacCreate, MovimientoReformaCreate" which broke the List[] type hint inside the function signature!
content = content.replace("req_links: List[ProcesoItemPacLinkCreate, ReformaPacCreate, MovimientoReformaCreate]", "req_links: List[ProcesoItemPacLinkCreate]")

with open(path, "w") as f:
    f.write(content)
