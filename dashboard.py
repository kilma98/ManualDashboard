import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Measurement, User  # import your existing SQLAlchemy models
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from models import Measurement, User 
import os
# Use the same database URL you use in FastAPI
DATABASE_URL= os.getenv("DATABASE_URL")

load_dotenv()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_user_measurements(user_id):
    db = SessionLocal()
    measurements = db.query(Measurement).filter(Measurement.user_id == user_id).all()
    db.close()
    
    data = {
        "temperature": [m.temperature for m in measurements],
        "humidity": [m.humidity for m in measurements],
        "water_temperature": [m.water_temperature for m in measurements],
        "timestamp": [m.timestamp for m in measurements]  # if you have a timestamp
    }
    return pd.DataFrame(data)



st.title("Admin Dashboard - Measurements Overview")

# Replace with actual user IDs from your database
user_id = st.selectbox("Select a user", options=[1, 2, 3])

df = get_user_measurements(user_id)

if not df.empty:
    st.write(f"Measurements for User {user_id}")
    
    # Temperature graph
    st.subheader("Temperature")
    st.line_chart(df[["timestamp", "temperature"]].set_index("timestamp"))

    # Humidity graph
    st.subheader("Humidity")
    st.line_chart(df[["timestamp", "humidity"]].set_index("timestamp"))

    # Water temperature graph
    st.subheader("Water Temperature")
    st.line_chart(df[["timestamp", "water_temperature"]].set_index("timestamp"))
else:
    st.warning("No measurements found for this user.")
