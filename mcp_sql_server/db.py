import pymysql
from pymysql.cursors import DictCursor

class Database:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.database = database
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            cursorclass=DictCursor
        )

    def list_tables(self) -> list[str]:
        with self.conn.cursor() as cur:
            cur.execute("SHOW TABLES;")
            return [row[list(row.keys())[0]] for row in cur.fetchall()]

    def get_table_schema(self, table: str) -> list[dict]:
        with self.conn.cursor() as cur:
            cur.execute(f"DESCRIBE `{table}`;")
            return cur.fetchall()

    def run_query(self, sql: str) -> list[dict]:
        lowered = sql.strip().lower()
        if lowered.startswith(("insert", "update", "delete", "drop", "alter")):
            raise ValueError("Only SELECT queries are allowed.")
        with self.conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

    def explain_query(self, sql: str) -> list[dict]:
        with self.conn.cursor() as cur:
            cur.execute("EXPLAIN " + sql)
            return cur.fetchall()
    
    def get_database_schema(self) -> dict:
      with self.conn.cursor() as cur:
          cur.execute("""
              SELECT
                  c.TABLE_NAME,
                  c.COLUMN_NAME,
                  c.COLUMN_TYPE,
                  c.IS_NULLABLE,
                  c.COLUMN_DEFAULT,
                  c.COLUMN_KEY,
                  kcu.REFERENCED_TABLE_NAME,
                  kcu.REFERENCED_COLUMN_NAME
              FROM INFORMATION_SCHEMA.COLUMNS c
              LEFT JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu
                  ON c.TABLE_SCHEMA = kcu.TABLE_SCHEMA
                AND c.TABLE_NAME = kcu.TABLE_NAME
                AND c.COLUMN_NAME = kcu.COLUMN_NAME
              WHERE c.TABLE_SCHEMA = %s
              ORDER BY c.TABLE_NAME, c.ORDINAL_POSITION;
          """, (self.database,))
          rows = cur.fetchall()

      schema = {}
      for row in rows:
          tname = row["TABLE_NAME"]
          schema.setdefault(tname, {"columns": [], "foreign_keys": []})
          schema[tname]["columns"].append({
              "name": row["COLUMN_NAME"],
              "type": row["COLUMN_TYPE"],
              "nullable": row["IS_NULLABLE"] == "YES",
              "key": row["COLUMN_KEY"]
          })
          if row["REFERENCED_TABLE_NAME"]:
              schema[tname]["foreign_keys"].append({
                  "column": row["COLUMN_NAME"],
                  "references": f"{row['REFERENCED_TABLE_NAME']}({row['REFERENCED_COLUMN_NAME']})"
              })

      return {"tables": schema}

