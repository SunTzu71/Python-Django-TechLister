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
SELECT pi.recruiter, pi.active, pi.first_name, pi.last_name, pi.city, pi.state, pi.about,
       pi.profile_image, pi.user_id,  COALESCE(STRING_AGG(us.skill_name, ', '), '') AS skills
FROM website_personalinformation AS pi
LEFT JOIN website_userskill AS us ON pi.user_id = us.user_id
WHERE pi.recruiter = false AND pi.active = true GROUP BY pi.id
"""

# Read the SQL query result into a DataFrame
df = pd.read_sql_query(query, conn)

# Combine the 'about' column with the 'skills' column separated by '<br />'
df['about'] = df['skills'] + '<br />' + df['about']

# Drop the 'skills' column as it's no longer needed
#df.drop(columns=['skills'], inplace=True)

# Export DataFrame to a JSON file with each object on its own line
df.to_json('user_listings.json', orient='records', lines=True)

# Close connection
conn.close()

# Now try reading the JSON file back
#df = pd.read_json("./job_listings.json", lines=True)
#print(df)
