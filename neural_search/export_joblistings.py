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
# Instead of doing select all make sure to only get columns needed for VectorDatabase
query = """
SELECT jl.*, COALESCE(STRING_AGG(js.skill_name, ', '), '') AS skills, wp.profile_image  
FROM website_joblisting AS jl
LEFT JOIN website_jobskill AS js ON jl.id = js.job_id 
LEFT JOIN website_personalinformation AS wp ON jl.user_id = wp.user_id 
WHERE jl.active = TRUE 
GROUP BY jl.id, wp.profile_image;
"""

# Read the SQL query result into a DataFrame
df = pd.read_sql_query(query, conn)

# Combine the 'about' column with the 'skills' column separated by '<br />'
df['description'] = df['skills'] + '<br />' + df['description']

# Drop the 'skills' column as it's no longer needed
#df.drop(columns=['skills'], inplace=True)

# Export DataFrame to a JSON file with each object on its own line
df.to_json('job_listings.json', orient='records', lines=True)

# Close connection
conn.close()

# Now try reading the JSON file back
#df = pd.read_json("./job_listings.json", lines=True)
#print(df)
