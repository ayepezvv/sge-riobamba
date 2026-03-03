path = "src/contexts/JWTContext.tsx"
with open(path, "r") as f:
    content = f.read()

mapping_logic = """const rawUser = response.data;
          const user = {
            ...rawUser,
            id: String(rawUser.id),
            name: `${rawUser.nombres} ${rawUser.apellidos}`,
            email: rawUser.correo,
            role: 'Admin'
          };"""

mapping_logic_login = """const rawUser = meResponse.data;
    const user = {
      ...rawUser,
      id: String(rawUser.id),
      name: `${rawUser.nombres} ${rawUser.apellidos}`,
      email: rawUser.correo,
      role: 'Admin'
    };"""

content = content.replace("const user = response.data;", mapping_logic, 1)
content = content.replace("const user = meResponse.data;", mapping_logic_login, 1)

with open(path, "w") as f:
    f.write(content)
