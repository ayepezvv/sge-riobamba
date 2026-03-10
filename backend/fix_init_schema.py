# that __init__.py in schemas was broken maybe from earlier
path = "app/schemas/__init__.py"
content = """from .role import RoleCreate, RoleResponse
from .user import UserCreate, UserResponse
from .token import Token, TokenPayload
"""
with open(path, "w") as f:
    f.write(content)
