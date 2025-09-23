from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://user:password@localhost:5432/mydb")

try:
    with engine.connect() as conn:
        print("Database OK")
        print(conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';").fetchall())
except Exception as e:
    print("DB not reachable:", e)

