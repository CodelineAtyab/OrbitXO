#Create/ Read/ Update/ Delete file - for database operations
from .database import get_connection

# to create history records
def create_history(input_str: str, output_list: list[int]):
    conn = get_connection()
    cursor = conn.cursor()
    output_str = ",".join(map(str, output_list))
    cursor.execute(
        "INSERT INTO history (input_str, output_str) VALUES (?, ?)",
        (input_str, output_str)
    )
    conn.commit()
    conn.close()

#to read history records
def get_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row["id"], "input": row["input_str"], "output": row["output_str"]} for row in rows]
