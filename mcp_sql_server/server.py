import argparse
from mcp.server.fastmcp import FastMCP
from .db import Database

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run MCP SQL Server")
    parser.add_argument("--host", required=True, help="Database host")
    parser.add_argument("--user", required=True, help="Database username")
    parser.add_argument("--password", required=True, help="Database password")
    parser.add_argument("--db", required=True, help="Database name")
    parser.add_argument("--transport", default="stdio", help="MCP transport type (default: stdio)")
    args = parser.parse_args()

    print(f"🔌 Connecting to database `{args.db}` on host `{args.host}` as user `{args.user}`...")

    # Connect to DB
    try:
        db = Database(args.host, args.user, args.password, args.db)
        print("✅ Database connection established successfully.")
    except Exception as e:
        print(f"❌ Failed to connect to the database: {e}")
        return

    # Create MCP server
    mcp = FastMCP("mysql_mcp_server")

    # Register tools
    @mcp.tool()
    def list_tables() -> list[str]:
        """List all tables in the database."""
        return db.list_tables()

    @mcp.tool()
    def get_table_schema(table: str) -> list[dict]:
        """Get schema for a specific table."""
        return db.get_table_schema(table)
    
    @mcp.tool()
    def get_database_schema() -> dict:
        """
        Returns a complete, LLM-friendly schema description of the connected database.
        Includes tables, columns, primary and foreign key relationships.
        """
        return db.get_database_schema()

    @mcp.tool()
    def run_query(sql: str) -> list[dict]:
        """Execute a read-only SELECT query."""
        return db.run_query(sql)

    @mcp.tool()
    def explain_query(sql: str) -> list[dict]:
        """Return EXPLAIN output for a SQL query."""
        return db.explain_query(sql)

    print("🚀 MCP SQL Server is ready and listening for requests...")
    print(f"   Transport: {args.transport}")
    print(f"   Connected DB: {args.db}\n")

    # Run MCP server
    mcp.run(transport=args.transport)

if __name__ == "__main__":
    main()
