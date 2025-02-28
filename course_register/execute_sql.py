import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# Read SQL file and execute the query
with open("course_data.sql", "r", encoding="utf-8") as f:
    sql_query = f.read().strip()  # Read and clean up the SQL command

try:
    cursor.execute(sql_query)  # Execute query
    results = cursor.fetchall()  # Fetch results

    if results:
        print("Query Results:")
        for row in results:
            print(row)  # Print each row
    else:
        print("No data found in course_registration_course.")

except sqlite3.OperationalError as e:
    print(f"SQL Error: {e}")

# Close connection
conn.close()
