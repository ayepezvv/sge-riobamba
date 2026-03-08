import re

path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/app/(dashboard)/contratacion/procesos/[id]/page.tsx"
with open(path, "r") as f:
    content = f.read()

# Update the fetch to get only plantillas for this specific process and active
old_fetch = """      const [resProc, resPlan] = await Promise.all([
        axios.get(`/api/contratacion/procesos/${procesoId}`),
        axios.get('/api/contratacion/plantillas')
      ]);
      setProceso(resProc.data);
      // Solo mostramos plantillas Activas para nuevas generaciones
      setPlantillas(resPlan.data.filter((p: any) => p.is_activa));"""

new_fetch = """      const resProc = await axios.get(`/api/contratacion/procesos/${procesoId}`);
      const proc = resProc.data;
      setProceso(proc);
      
      const resPlan = await axios.get(`/api/contratacion/plantillas?tipo_proceso_id=${proc.tipo_proceso_id}&is_activa=true`);
      setPlantillas(resPlan.data);"""

content = content.replace(old_fetch, new_fetch)

with open(path, "w") as f:
    f.write(content)
