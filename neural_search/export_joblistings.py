import psycopg2
import pandas as pd

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="tech_lister",
    user="techlister",
    password="techlister",
    host="localhost",
    port="5432"
)

# Construct the SQL query to join job listings with their skills
query = """
SELECT jl.*, COALESCE(STRING_AGG(js.skill_name, ', '), '') AS skills
FROM website_joblisting AS jl
LEFT JOIN website_jobskill AS js ON jl.id = js.job_id
GROUP BY jl.id;
"""

# Read the SQL query result into a DataFrame
df = pd.read_sql_query(query, conn)

# Combine the 'about' column with the 'skills' column separated by '<br />'
df['about'] = df['city'] + ', ' + df['state'] + '<br />' + df['skills'] + '<br />' + df['about']

# Drop the 'skills' column as it's no longer needed
df.drop(columns=['skills'], inplace=True)

# Export DataFrame to a JSON file with each object on its own line
df.to_json('job_listings.json', orient='records', lines=True)

# Close connection
conn.close()

# Now try reading the JSON file back
df = pd.read_json("./job_listings.json", lines=True)
print(df)
