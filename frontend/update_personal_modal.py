import re

path = "src/app/(dashboard)/administrativo/personal/page.tsx"
with open(path, "r") as f:
    content = f.read()

# Add puestos state
state_search = "const [usuarios, setUsuarios] = useState([]);"
state_replace = "const [usuarios, setUsuarios] = useState([]);\n  const [puestos, setPuestos] = useState([]);\n  const [selectedPuesto, setSelectedPuesto] = useState<any>(null);"
content = content.replace(state_search, state_replace)

# Update formData state
form_search = "unidad_id: '', usuario_id: '', foto_perfil: '',"
form_replace = "unidad_id: '', usuario_id: '', puesto_id: '', foto_perfil: '',"
content = content.replace(form_search, form_replace)

# Add fetchPuestos
fetch_search = """  const fetchUsuarios = async () => {"""
fetch_replace = """  const fetchPuestos = async () => {
    try {
      const res = await fetch('http://192.168.1.15:8000/api/administrativo/puestos');
      if (res.ok) setPuestos(await res.json());
    } catch (e) { console.error(e); }
  };

  const fetchUsuarios = async () => {"""
content = content.replace(fetch_search, fetch_replace)

# Add fetchPuestos to useEffect
ue_search = "useEffect(() => { fetchPersonal(); fetchUnidades(); fetchUsuarios(); }, []);"
ue_replace = "useEffect(() => { fetchPersonal(); fetchUnidades(); fetchUsuarios(); fetchPuestos(); }, []);"
content = content.replace(ue_search, ue_replace)

# Update handleOpen to clear/load puesto
open_if_search = "usuario_id: item.usuario_id || '',"
open_if_replace = "usuario_id: item.usuario_id || '',\n        puesto_id: item.puesto_id || '',"
content = content.replace(open_if_search, open_if_replace)

open_else_search = "unidad_id: '', usuario_id: '', foto_perfil: '',"
open_else_replace = "unidad_id: '', usuario_id: '', puesto_id: '', foto_perfil: '',"
content = content.replace(open_else_search, open_else_replace)

# Set selectedPuesto when opening if editing
open_start_search = "const handleOpen = (item = null) => {"
open_start_replace = """const handleOpen = (item = null) => {
    if (item && item.puesto_id) {
      const found = puestos.find((p: any) => p.id === item.puesto_id);
      setSelectedPuesto(found || null);
    } else {
      setSelectedPuesto(null);
    }"""
content = content.replace(open_start_search, open_start_replace)

# Handle Puesto change
handle_puesto = """
  const handlePuestoChange = (e: any) => {
    const val = e.target.value;
    setFormData({ ...formData, puesto_id: val });
    if (val) {
      const found = puestos.find((p: any) => p.id === val);
      setSelectedPuesto(found || null);
    } else {
      setSelectedPuesto(null);
    }
  };
"""
content = content.replace("const handleSave = async () => {", handle_puesto + "\n  const handleSave = async () => {")

# Clean empty strings
payload_search = "if (payload.usuario_id === '') payload.usuario_id = null;"
payload_replace = "if (payload.usuario_id === '') payload.usuario_id = null;\n    if (payload.puesto_id === '') payload.puesto_id = null;"
content = content.replace(payload_search, payload_replace)

# Update tabs
tabs_search = "{editingId && <Tab label=\"Formación Académica\" />}"
tabs_replace = "{editingId && <Tab label=\"Formación Académica\" />}\n            <Tab label=\"Datos Remunerativos\" />"
content = content.replace(tabs_search, tabs_replace)

# Add TAB 5
tab5 = """
          {/* TAB 5: DATOS REMUNERATIVOS */}
          <CustomTabPanel value={tabIndex} index={editingId ? 4 : 3}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>Asignación Presupuestaria del Puesto</Typography>
                <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                  Alerta: Los cargos ahora se controlan estrictamente a través del Catálogo de Puestos Institucionales.
                </Typography>
              </Grid>
              <Grid item xs={12} sm={12}>
                <FormControl fullWidth>
                  <InputLabel>Puesto / Partida</InputLabel>
                  <Select value={formData.puesto_id} label="Puesto / Partida" onChange={handlePuestoChange}>
                    <MenuItem value=""><em>Ninguno</em></MenuItem>
                    {puestos.map((p: any) => <MenuItem key={p.id} value={p.id}>{p.denominacion} (Partida: {p.partida_presupuestaria})</MenuItem>)}
                  </Select>
                </FormControl>
              </Grid>
              {selectedPuesto && (
                <>
                  <Grid item xs={12} sm={4}>
                    <TextField fullWidth disabled label="Escala Ocupacional" value={selectedPuesto.escala_ocupacional || 'N/A'} />
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <TextField fullWidth disabled label="Remuneración Mensual" value={`$${selectedPuesto.remuneracion_mensual.toFixed(2)}`} />
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <TextField fullWidth disabled label="Partida Presupuestaria" value={selectedPuesto.partida_presupuestaria} />
                  </Grid>
                </>
              )}
            </Grid>
          </CustomTabPanel>
"""
content = content.replace("</DialogContent>", tab5 + "</DialogContent>")

with open(path, "w") as f:
    f.write(content)
