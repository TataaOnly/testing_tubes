import sqlite3, re

sql_script=open('simrs.sql').read()
sql_script = '\n'.join(line for line in sql_script.splitlines() if not line.strip().startswith(('SET', 'FOREIGN_KEY_CHECKS', 'DEFAULT CHARSET', 'START TRANSACTION', 'COMMIT')))

sql_script = sql_script.replace('`', '"')
sql_script = sql_script.replace("\\'", "''")

sql_script = re.sub(r"enum\([^)]+\)", "TEXT", sql_script, flags=re.IGNORECASE)
sql_script = re.sub(r"\)\s*ENGINE=[^;]+;", ");", sql_script, flags=re.IGNORECASE)

sql_script = re.sub(r"ALTER TABLE.*?;\n?", "", sql_script, flags=re.DOTALL | re.IGNORECASE)

try:
    conn=sqlite3.connect(':memory:')
    for stmt in sql_script.split(';'):
        stmt = stmt.strip()
        if not stmt: continue
        try:
            conn.execute(stmt)
        except Exception as e:
            print(f"Error executing:\n{stmt}\n\nError: {e}")
            break
    print("Done")
except Exception as e:
    print(f"Connection Error: {e}")
