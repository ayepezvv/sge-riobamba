path = "src/utils/axios.ts"
with open(path, "r") as f:
    content = f.read()

new_reject = """    if (error.response?.status === 401 && !window.location.href.includes('/login')) {
      window.location.pathname = '/login';
    }
    return Promise.reject((error.response && error.response.data) || error || 'Wrong Services');"""

content = content.replace("""    if (error.response?.status === 401 && !window.location.href.includes('/login')) {
      window.location.pathname = '/login';
    }
    return Promise.reject((error.response && error.response.data) || 'Wrong Services');""", new_reject)

with open(path, "w") as f:
    f.write(content)
