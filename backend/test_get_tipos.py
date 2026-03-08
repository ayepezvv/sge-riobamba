import requests

# 1. Get Token
url_login = "http://localhost:8000/api/auth/login"
data = {"username": "admin@riobambaep.gob.ec", "password": "Admin123*"}
resp = requests.post(url_login, data=data)
if resp.status_code != 200:
    print("Login Falló:", resp.text)
    exit(1)

token = resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# 2. Get Tipos
resp_tipos = requests.get("http://localhost:8000/api/contratacion/tipos", headers=headers)
print("GET /tipos Status:", resp_tipos.status_code)
print("GET /tipos Response:", resp_tipos.text[:500])

# 3. Get Plantillas
resp_plan = requests.get("http://localhost:8000/api/contratacion/plantillas", headers=headers)
print("GET /plantillas Status:", resp_plan.status_code)
print("GET /plantillas Response:", resp_plan.text[:500])
