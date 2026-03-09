import re

path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/app/(dashboard)/contratacion/procesos/[id]/page.tsx"
with open(path, "r") as f:
    content = f.read()

# When parsing schema to pre-fill dynamicData, use the saved formData from Proceso if available
old_fill = """          // Pre-poblar el formulario con datos del proceso si los nombres coinciden
          const initialData: any = {};
          res.data.variables.forEach((v: any) => {
            if (v.nombre === 'nombre_proyecto' || v.nombre === 'objeto_contratacion') {
              initialData[v.nombre] = proceso?.nombre_proyecto || '';
            } else if (v.nombre === 'codigo_proceso') {
              initialData[v.nombre] = proceso?.codigo_proceso || '';
            } else if (v.nombre.toLowerCase().includes('fecha')) {
              initialData[v.nombre] = new Date().toLocaleDateString('es-EC');
            } else {
              initialData[v.nombre] = '';
            }
          });
          setDinamicData(initialData);"""

new_fill = """          // Persistencia de memoria: Si el expediente ya tiene datos guardados, usarlos. Si no, pre-poblar.
          if (proceso?.datos_formulario && Object.keys(proceso.datos_formulario).length > 0) {
            setDinamicData(proceso.datos_formulario);
          } else {
            const initialData: any = {};
            res.data.variables.forEach((v: any) => {
              if (v.nombre === 'nombre_proyecto' || v.nombre === 'objeto_contratacion') {
                initialData[v.nombre] = proceso?.nombre_proyecto || '';
              } else if (v.nombre === 'codigo_proceso') {
                initialData[v.nombre] = proceso?.codigo_proceso || '';
              } else if (v.nombre.toLowerCase().includes('fecha')) {
                initialData[v.nombre] = new Date().toLocaleDateString('es-EC');
              } else {
                initialData[v.nombre] = '';
              }
            });
            setDinamicData(initialData);
          }"""

content = content.replace(old_fill, new_fill)

with open(path, "w") as f:
    f.write(content)
