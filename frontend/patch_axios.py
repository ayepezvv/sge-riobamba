with open("src/utils/axios.ts", "r") as f:
    content = f.read()

content = content.replace("error.response.status === 401", "error.response?.status === 401")

with open("src/utils/axios.ts", "w") as f:
    f.write(content)
