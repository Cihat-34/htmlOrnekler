from flask import Flask, request, jsonify
import pyodbc
from datetime import datetime
import traceback

app = Flask(__name__)

def get_db_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DESKTOP-ON79G27\SQLEXPRESS;'  
            'DATABASE=nova_akademi;'
            'Trusted_Connection=yes'
        )
        return conn
    except pyodbc.Error as e:
        print(f"Veritabanı bağlantı hatası: {e}")
        return None
    
