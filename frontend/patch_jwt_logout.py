path = "src/contexts/JWTContext.tsx"
with open(path, "r") as f:
    content = f.read()

# Make sure we clean token on catch
new_catch = """      } catch (err) {
        console.error("JWT Init Error:", err);
        setSession(null);
        dispatch({
          type: LOGOUT
        });
      }"""

content = content.replace("      } catch (err) {\n        console.error(err);\n        dispatch({\n          type: LOGOUT\n        });\n      }", new_catch)

with open(path, "w") as f:
    f.write(content)
