path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

import re

# Add imports
imports = """import pandas as pd
import numpy as np
import io\n"""
content = imports + content

# Fix NaN replacements in df
nan_fix = """
    # Clean headers (lower and strip)
    df.columns = df.columns.str.lower().str.strip()
    
    # Prevenir que SQLAlchemy explote por los NaNs nativos de Pandas
    df = df.replace({np.nan: None})
"""
content = content.replace("    # Clean headers (lower and strip)\n    df.columns = df.columns.str.lower().str.strip()", nan_fix)

# Clean up any potential double io imports
content = content.replace("import pandas as pd\nimport io\n", "") # from previous script attempt

with open(path, "w") as f:
    f.write(content)
