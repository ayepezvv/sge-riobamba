import re

path = "src/app/(dashboard)/contratacion/procesos/page.tsx"
with open(path, "r") as f:
    content = f.read()

# I need to add state for pac items
pac_state = """  const [pacItems, setPacItems] = useState([]);
  const [selectedPacItems, setSelectedPacItems] = useState<number[]>([]);"""
content = content.replace("const [open, setOpen] = useState(false);", "const [open, setOpen] = useState(false);\n" + pac_state)

fetch_pac = """  const fetchPacItems = async () => {
    try {
      const res = await fetch('http://192.168.1.15:8000/api/contratacion/pac');
      if (res.ok) {
        const pacs = await res.json();
        // Extract active pac items
        let items: any[] = [];
        pacs.forEach((p: any) => {
            if (p.es_activo && p.items) {
                items = [...items, ...p.items];
            }
        });
        setPacItems(items as any);
      }
    } catch (e) { console.error(e); }
  };"""

content = content.replace("const fetchProcesos = async () => {", fetch_pac + "\n  const fetchProcesos = async () => {")
content = content.replace("fetchProcesos(); fetchTipos();", "fetchProcesos(); fetchTipos(); fetchPacItems();")

form_search = "codigo_proceso: '', nombre_proyecto: '', descripcion: '', tipo_proceso_id: ''"
form_replace = "codigo_proceso: '', nombre_proyecto: '', descripcion: '', tipo_proceso_id: '', items_pac_links: []"
content = content.replace(form_search, form_replace)

# Handle item change
handle_pac = """  const handlePacChange = (event: any) => {
    const {
      target: { value },
    } = event;
    setSelectedPacItems(
      typeof value === 'string' ? value.split(',') : value,
    );
  };"""
content = content.replace("const handleSave = async () => {", handle_pac + "\n  const handleSave = async () => {")

# Patch handleSave to do the linking
save_search = """      if (res.ok) {
        setToast({ open: true, message: 'Proceso guardado exitosamente', severity: 'success' });
        setOpen(false);
        fetchProcesos();"""

save_replace = """      if (res.ok) {
        const newProceso = await res.json();
        
        // Vincular PAC si aplica (crear enlaces proporcionales)
        if (selectedPacItems.length > 0) {
            const links = selectedPacItems.map(id => {
                const item: any = pacItems.find((i: any) => i.id === id);
                return { item_pac_id: id, monto_comprometido: item ? item.valor_total : 0 };
            });
            await fetch(`http://192.168.1.15:8000/api/contratacion/procesos/${newProceso.id || editingId}/vincular_pac`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(links)
            });
        }
        
        setToast({ open: true, message: 'Proceso guardado exitosamente', severity: 'success' });
        setOpen(false);
        fetchProcesos();"""
content = content.replace(save_search, save_replace)

# Add select to Modal
select_html = """
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Vincular a Líneas del PAC (Opcional)</InputLabel>
                <Select
                  multiple
                  value={selectedPacItems}
                  onChange={handlePacChange}
                  label="Vincular a Líneas del PAC (Opcional)"
                  renderValue={(selected) => selected.map(id => {
                    const item: any = pacItems.find((i: any) => i.id === id);
                    return item ? item.cpc + ' - ' + item.descripcion.substring(0, 30) : id;
                  }).join(', ')}
                >
                  {pacItems.map((item: any) => (
                    <MenuItem key={item.id} value={item.id}>
                      {item.cpc} | {item.descripcion} (${item.valor_total})
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>"""

content = content.replace("<Grid item xs={12}>\n              <TextField", select_html + "\n              <TextField", 1)

with open(path, "w") as f:
    f.write(content)
