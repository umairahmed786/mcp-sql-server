# 🧠 MCP SQL Server

**MCP SQL Server** is a lightweight **Model Context Protocol (MCP)** server that connects to a MySQL database and exposes database schema and query capabilities to compatible LLM-based tools (like the MCP Inspector or OpenAI’s Code Interpreter extensions).

It supports:

- Running locally via Python  
- Deployment via Docker  

---

## 📁 Project Structure

```bash
MCP-SQL-SERVER/
├── mcp_sql_server/
│   ├── __init__.py
│   ├── db.py
│   └── server.py
├── requirements.txt
└── Dockerfile
```

---

## ⚙️ Requirements

- Python 3.11+
- MySQL Server (accessible via network)
- `pip` and `virtualenv` (optional for local dev)
- Docker (optional, for containerized deployment)

---

## 🧩 Installation (Local Setup)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/umairahmed786/mcp-sql-server.git
cd mcp-sql-server
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Run Locally

You can start the MCP SQL Server directly using Python:

```bash
python -m mcp_sql_server.server   --host localhost   --user root   --password "your_password"   --db your_database_name   --transport stdio
```

**Example:**

```bash
python -m mcp_sql_server.server   --host localhost   --user root   --password "123"   --db abc
```

---

## 🐳 Run with Docker

### 1️⃣ Build the Docker image
```bash
docker build -t mcp-sql-server .
```

### 2️⃣ Run the Docker container
```bash
docker run --rm -it   mcp-sql-server   --host host.docker.internal   --user root   --password "123"   --db abc
```

> 💡 **Note:**  
> `host.docker.internal` allows Docker to access your host machine’s MySQL server (works on macOS & Windows).

---

## 🔧 MCP Tools Available

| Tool Name | Description |
|------------|-------------|
| `list_tables()` | Lists all tables in the connected database |
| `get_table_schema(table)` | Retrieves schema for a specific table |
| `get_database_schema()` | Returns a full schema overview with columns, keys, and relationships |
| `run_query(sql)` | Executes read-only `SELECT` queries |
| `explain_query(sql)` | Returns the MySQL `EXPLAIN` plan for a given query |

---

## 🧱 MCP Inspector Configuration

| Setting | Value |
|----------|--------|
| **Transport Type** | `STDIO` |
| **Command** | `python` |
| **Arguments** | `-m mcp_sql_server.server --host localhost --user root --password 123 --db abc` |

> If you are using Docker, replace `python` with the Docker run command above.

---

## ⚡ Environment Variables (Optional)

You can simplify your command by setting environment variables:

```bash
export DB_HOST=localhost
export DB_USER=root
export DB_PASS="123"
export DB_NAME=abc
```

Then run:

```bash
python -m mcp_sql_server.server   --host $DB_HOST   --user $DB_USER   --password $DB_PASS   --db $DB_NAME
```

---

## 🧰 Troubleshooting

| Issue | Possible Fix |
|--------|---------------|
| `ModuleNotFoundError: No module named 'mcp'` | Ensure `mcp` is listed in `requirements.txt` or run `pip install mcp` |
| `Connection Error` in MCP Inspector | Check if MySQL is running and credentials are correct |
| Docker cannot connect to MySQL | Use `host.docker.internal` instead of `localhost` |

---

## 💡 Use Case: LLM Database Context Provider

Once connected, your **MCP SQL Server** acts as a **context provider** — allowing AI systems to:

- **Automatically analyze schema**  
- **Generate valid SQL queries**  
- **Understand foreign key relationships**  
- **Provide context-aware completions**

This enables **smarter and safer AI-assisted database operations**.

---

## 📬 Contact & Support

Please feel free to **use, extend, and customize** this project for your own use cases.  
If you need help, collaboration, or guidance, you can reach out to:

📧 **Email:** [umairahmedpaki7@gmail.com](mailto:umairahmedpaki7@gmail.com)
