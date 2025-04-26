import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="weather_db",     # use the name you created in pgAdmin
        user="postgres",         # default PostgreSQL user
        password="admin123",  # the password you set during installation
        host="localhost",
        port="5432"
    )
