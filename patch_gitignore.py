with open(".gitignore", "r") as f:
    content = f.read()

if "db_backups/" not in content:
    content += "\n# Backups permitidos\n!db_backups/sge_replica_inicial.sql\n"

with open(".gitignore", "w") as f:
    f.write(content)
