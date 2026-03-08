import re
path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/app/(dashboard)/contratacion/procesos/page.tsx"
with open(path, "r") as f:
    content = f.read()

# Fix logic so the ID is passed securely to backend
new_submit = """  const handleSubmit = async () => {
    try {
      const payload = {
        codigo_proceso: wizardData.codigo_proceso,
        nombre_proyecto: wizardData.nombre_proyecto,
        descripcion: `[${tipoRecomendado?.nombre || 'Proceso'}] ${wizardData.descripcion}`,
        tipo_proceso_id: tipoRecomendado?.id || null
      };
      await axios.post('/api/contratacion/procesos', payload);
      setToast({ open: true, message: 'Expediente creado correctamente', severity: 'success' });
      setOpen(false);
      setActiveStep(0);
      setWizardData({ categoria: '', catalogo_electronico: '', monto: '', codigo_proceso: '', nombre_proyecto: '', descripcion: '' });
      fetchProcesos();
    } catch (error: any) {
      setToast({ open: true, message: error.response?.data?.detail || 'Error', severity: 'error' });
    }
  };"""

content = re.sub(r'  const handleSubmit = async \(\) => \{.*?\n  \};', new_submit, content, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(content)
