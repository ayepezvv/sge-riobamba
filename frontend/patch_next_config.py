import re

path = "next.config.ts"
with open(path, "r") as f:
    content = f.read()

# I will use a simple split/join strategy to append the experimental block inside nextConfig
new_config = """    ]
  },
  experimental: {
    // Next.js 14 server actions allowed origins
    serverActions: {
        allowedOrigins: ['192.168.1.15', 'localhost', '192.168.1.15:3000']
    }
  }
};"""

content = content.replace("    ]\n  }\n};", new_config)

with open(path, "w") as f:
    f.write(content)
