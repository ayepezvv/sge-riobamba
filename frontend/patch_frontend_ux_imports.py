import re

path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/app/(dashboard)/contratacion/procesos/[id]/page.tsx"
with open(path, "r") as f:
    content = f.read()

# Replace the specific import line to include Card and CardContent
new_imports = "import { Box, Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField, Snackbar, Alert, Typography, Grid, IconButton, Tooltip, FormControl, InputLabel, Select, MenuItem, Chip, CircularProgress, Card, CardContent } from '@mui/material';"
content = re.sub(r"import \{ Box, Button.*?\} from '@mui/material';", new_imports, content, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(content)
