# ===================================
# MCP SQL Server - Dockerfile
# ===================================

# 1️⃣ Base image
FROM python:3.11-slim

# 2️⃣ Set working directory
WORKDIR /app

# 3️⃣ Copy requirements first (for layer caching)
COPY requirements.txt .

# 4️⃣ Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5️⃣ Copy the application code
COPY . .

# 6️⃣ Optional: Expose a port if you use WebSocket or HTTP transport
EXPOSE 8000

# 7️⃣ Default entrypoint (can be overridden)
ENTRYPOINT ["python", "-m", "mcp_sql_server.server"]
