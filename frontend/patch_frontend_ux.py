import re

path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/app/(dashboard)/contratacion/procesos/[id]/page.tsx"
with open(path, "r") as f:
    content = f.read()

# 1. Imports
if "CardContent" not in content:
    content = content.replace("import { Box, Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField, Snackbar, Alert, Typography, Grid, IconButton, Tooltip, FormControl, InputLabel, Select, MenuItem, Chip, CircularProgress } from '@mui/material';", "import { Box, Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField, Snackbar, Alert, Typography, Grid, IconButton, Tooltip, FormControl, InputLabel, Select, MenuItem, Chip, CircularProgress, Card, CardContent } from '@mui/material';")

# 2. Date initialization
old_init = """            } else if (v.nombre === 'fecha' || v.nombre === 'fecha_actual') {
              initialData[v.nombre] = new Date().toISOString().split('T')[0];"""
new_init = """            } else if (v.nombre.toLowerCase().includes('fecha')) {
              initialData[v.nombre] = new Date().toLocaleDateString('es-EC');"""

content = content.replace(old_init, new_init)

# 3. Context Renderer logic
render_func = """  const renderContexto = (contextoStr: string, variableNombre: string) => {
    if (!contextoStr) return null;
    const parts = contextoStr.split(`[ ${variableNombre} ]`);
    if (parts.length === 1) return <Typography variant="caption" color="textSecondary">{contextoStr}</Typography>;
    return (
      <Typography variant="caption" color="textSecondary" component="span" sx={{ display: 'block', mt: 0.5, lineHeight: 1.2 }}>
        {parts[0]}
        <Typography component="span" fontWeight="bold" color="primary.main" sx={{ bgcolor: 'primary.light', px: 0.5, borderRadius: 1 }}>
          {variableNombre}
        </Typography>
        {parts[1]}
      </Typography>
    );
  };"""

if "const renderContexto" not in content:
    content = content.replace("  const [toast, setToast] = useState", render_func + "\n\n  const [toast, setToast] = useState")

# 4. Use the Context Renderer in the JSX
content = content.replace("helperText={v.contexto}", "helperText={renderContexto(v.contexto, v.nombre)}")
content = content.replace("<Typography variant=\"caption\" color=\"textSecondary\" display=\"block\" sx={{mt: 1}}>{v.contexto}</Typography>", "{renderContexto(v.contexto, v.nombre)}")
content = content.replace("<Typography variant=\"caption\" color=\"textSecondary\" display=\"block\" sx={{mb: 2}}>{v.contexto}</Typography>", "{renderContexto(v.contexto, v.nombre)}")

with open(path, "w") as f:
    f.write(content)
