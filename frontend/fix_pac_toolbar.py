import re

path = "src/app/(dashboard)/contratacion/pac/page.tsx"
with open(path, "r") as f:
    content = f.read()

# Add GridToolbar to imports if missing
if "GridToolbar" not in content:
    content = content.replace("DataGrid, GridColDef", "DataGrid, GridColDef, GridToolbar")

# Add to the DataGrid inside the Detail Modal
modal_grid_search = """<DataGrid 
                rows={detailItems} 
                columns={["""
modal_grid_replace = """<DataGrid 
                rows={detailItems} 
                slots={{ toolbar: GridToolbar }}
                slotProps={{ toolbar: { showQuickFilter: true } }}
                columns={["""

content = content.replace(modal_grid_search, modal_grid_replace)

with open(path, "w") as f:
    f.write(content)
