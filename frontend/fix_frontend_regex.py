import re
path = "src/app/(dashboard)/contratacion/procesos/[id]/page.tsx"
with open(path, "r") as f:
    content = f.read()

safe_block = """          let fileName = `Proceso_${procesoId}_Generado.docx`;
          const disposition = response.headers['content-disposition'];
          if (disposition && disposition.includes('filename=')) {
              fileName = disposition.split('filename=')[1].replace(/['"]/g, '').split(';')[0];
          }
          link.setAttribute('download', fileName);"""

content = re.sub(r'let fileName =.*?link\.setAttribute\(\'download\', fileName\);', safe_block, content, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(content)
