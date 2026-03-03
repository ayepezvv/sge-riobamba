path = "src/contexts/JWTContext.tsx"
with open(path, "r") as f:
    content = f.read()

new_catch = """      } catch (err: any) {
        console.error("JWT Init Error:", err);
        setSession(null);
        dispatch({
          type: LOGOUT
        });
      }"""

content = content.replace("""      } catch (err) {
        console.error("JWT Init Error:", err);
        setSession(null);
        dispatch({
          type: LOGOUT
        });
      }""", new_catch)

with open(path, "w") as f:
    f.write(content)
