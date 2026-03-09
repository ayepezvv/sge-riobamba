import re

path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

# Replace the simple get_render_data with a recursive one that traverses lists of dictionaries
new_get_render_data = """def get_render_data(doc, req_datos):
    from docxtpl import InlineImage
    from docx.shared import Mm
    import base64
    import io

    def procesar_valor(val):
        # Si es un string base64 de imagen
        if isinstance(val, str) and val.startswith("data:image"):
            try:
                header, encoded = val.split(",", 1)
                image_data = base64.b64decode(encoded)
                image_stream = io.BytesIO(image_data)
                return InlineImage(doc, image_stream, width=Mm(50))
            except Exception:
                return val
        # Si es una lista (para tablas dinamicas), aplicar recursividad
        elif isinstance(val, list):
            nueva_lista = []
            for item in val:
                if isinstance(item, dict):
                    nueva_lista.append(procesar_valor(item))
                else:
                    nueva_lista.append(item)
            return nueva_lista
        # Si es un diccionario
        elif isinstance(val, dict):
            nuevo_dict = {}
            for k, v in val.items():
                nuevo_dict[k] = procesar_valor(v)
            return nuevo_dict
        
        # Cualquier otra cosa se queda igual
        return val

    return procesar_valor(req_datos)"""

content = re.sub(r'def get_render_data\(doc, req_datos\):.*?return datos_para_render', new_get_render_data, content, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(content)
