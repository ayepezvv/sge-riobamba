import re

path = "src/app/(dashboard)/contratacion/procesos/[id]/page.tsx"
with open(path, "r") as f:
    content = f.read()

# Add miPerfil state
state_search = "const [dinamicData, setDinamicData] = useState<any>({});"
state_replace = "const [dinamicData, setDinamicData] = useState<any>({});\n  const [miPerfil, setMiPerfil] = useState<any>(null);"
content = content.replace(state_search, state_replace)

# Add fetchMiPerfil in useEffect
effect_search = """  const fetchProceso = async () => {
    try {
      const response = await axios.get(`/api/contratacion/procesos/${procesoId}`);
      setProceso(response.data);
    } catch (e) {
      console.error(e);
      setToast({ open: true, message: 'Error cargando proceso', severity: 'error' });
    }
  };"""

effect_replace = """  const fetchProceso = async () => {
    try {
      const response = await axios.get(`/api/contratacion/procesos/${procesoId}`);
      setProceso(response.data);
    } catch (e) {
      console.error(e);
      setToast({ open: true, message: 'Error cargando proceso', severity: 'error' });
    }
  };

  const fetchMiPerfil = async () => {
    try {
      const token = window.localStorage.getItem('serviceToken');
      const response = await fetch('http://192.168.1.15:8000/api/administrativo/personal/me', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        setMiPerfil(await response.json());
      }
    } catch (e) {
      console.error("No se pudo cargar el perfil para autocompletado");
    }
  };"""
content = content.replace(effect_search, effect_replace)

call_search = """    if (procesoId) {
      fetchProceso();
    }"""
call_replace = """    if (procesoId) {
      fetchProceso();
    }
    fetchMiPerfil();"""
content = content.replace(call_search, call_replace)

# Inject Auto-completion mapping
mapping_search = """            res.data.variables.forEach((v: any) => {
              if (v.nombre === 'nombre_proyecto' || v.nombre === 'objeto_contratacion') {
                initialData[v.nombre] = proceso?.nombre_proyecto || '';
              } else if (v.nombre === 'codigo_proceso') {
                initialData[v.nombre] = proceso?.codigo_proceso || '';
              } else if (v.nombre.toLowerCase().includes('fecha')) {
                initialData[v.nombre] = new Date().toLocaleDateString('es-EC');
              } else {
                initialData[v.nombre] = '';
              }
            });"""

mapping_replace = """            res.data.variables.forEach((v: any) => {
              const k = v.nombre.toLowerCase();
              if (v.nombre === 'nombre_proyecto' || v.nombre === 'objeto_contratacion') {
                initialData[v.nombre] = proceso?.nombre_proyecto || '';
              } else if (v.nombre === 'codigo_proceso') {
                initialData[v.nombre] = proceso?.codigo_proceso || '';
              } else if (k.includes('fecha')) {
                initialData[v.nombre] = new Date().toLocaleDateString('es-EC');
              } else if (miPerfil) {
                // Diccionario de Mapeo Inteligente (Autocompletado)
                if (k.includes('persona_elabora')) initialData[v.nombre] = `${miPerfil.nombres} ${miPerfil.apellidos}`;
                else if (k.includes('cargo_elabora')) initialData[v.nombre] = miPerfil.cargo || '';
                else if (k.includes('unidad_requirente')) initialData[v.nombre] = miPerfil.unidad?.nombre || '';
                else if (k.includes('cedula_elabora')) initialData[v.nombre] = miPerfil.cedula || '';
                else if (k.includes('certificacion_elabora') || k.includes('codigo_sercop')) initialData[v.nombre] = miPerfil.codigo_certificacion_sercop || '';
                else initialData[v.nombre] = '';
              } else {
                initialData[v.nombre] = '';
              }
            });"""
content = content.replace(mapping_search, mapping_replace)

# Add miPerfil to dependencies of the schema fetch useEffect
dep_search = "  }, [selectedPlantillaId, editingDocId, proceso]);"
dep_replace = "  }, [selectedPlantillaId, editingDocId, proceso, miPerfil]);"
content = content.replace(dep_search, dep_replace)

with open(path, "w") as f:
    f.write(content)
