import re

path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/app/(dashboard)/contratacion/administracion/page.tsx"
with open(path, "r") as f:
    content = f.read()

# Make sure error handling is robust when types or templates are undefined
robust_catch = """  const fetchData = async () => {
    setLoading(true);
    try {
      const [resTipos, resPlan] = await Promise.all([
        axios.get('/api/contratacion/tipos'),
        axios.get('/api/contratacion/plantillas')
      ]);
      setTipos(Array.isArray(resTipos.data) ? resTipos.data : []);
      setPlantillas(Array.isArray(resPlan.data) ? resPlan.data : []);
    } catch (error: any) {
      console.error(error);
      setToast({ open: true, message: error.message || 'Error cargando datos', severity: 'error' });
      setTipos([]);
      setPlantillas([]);
    } finally {
      setLoading(false);
    }
  };"""

content = re.sub(r'const fetchData = async \(\) => \{.*?\n  \};', robust_catch, content, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(content)
