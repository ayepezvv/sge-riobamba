path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/views/pages/authentication/jwt/AuthLogin.tsx"
with open(path, "r") as f:
    content = f.read()

# Fix the translation bug where I accidentally sed-replaced "Password" inside variable names
buggy_state = "const [showContraseña, setShowPassword] = useState(false);"
fixed_state = "const [showPassword, setShowPassword] = useState(false);"

buggy_handler = """  const handleClickShowContraseña = () => {
    setShowContraseña(!showPassword);
  };"""
fixed_handler = """  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
  };"""

buggy_mouse = "const handleMouseDownContraseña"
fixed_mouse = "const handleMouseDownPassword"

# Replace references in the code
content = content.replace(buggy_state, fixed_state)
content = content.replace(buggy_handler, fixed_handler)
content = content.replace(buggy_mouse, fixed_mouse)
content = content.replace("handleClickShowContraseña", "handleClickShowPassword")
content = content.replace("handleMouseDownContraseña", "handleMouseDownPassword")
content = content.replace("showContraseña", "showPassword")

# Also, let's clear the default Berry credentials so you don't have to delete them every time
content = content.replace("email: 'info@codedthemes.com',", "email: '',")
content = content.replace("password: '123456',", "password: '',")

with open(path, "w") as f:
    f.write(content)
