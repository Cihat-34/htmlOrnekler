from flask import Flask,request,jsonify
import pyodbc
from datetime import datetime
import traceback

app = Flask(__name__)

def get_db_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER = {ODBC Driver 17 for SQL Server};'
            'SERVER = DESKTOP-ON79G27\SQLEXPRESS;'
            'DATABASE = nova_akademi;'
            'Trusted_Connection = yes'
        )
        return conn
    except pyodbc.Error as e:
        print(f"veritabanı bağlantı hatası: {e}")
        return None
    
app.route('/add-book',methods=['POST'])
def add_book():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error":"Veritabanına bağlanılamadı"}),500
    
    try:
        data = request.json
        print(f"Alınan veri: {data}") #debug için alınan veriyi yazdırıyoruz

        BookID = data.get('BookID')
        BookName = data.get('BookName')
        ReleaseYear = data.get('ReleaseYear')

        if BookID is None or BookName is None or ReleaseYear is None:
            return jsonify({"error":"Eksik veri: BookID,BookName ve ReleaseYear gerekli"}),400
        
        #yayın yılını doğrulama veya formatlama
        try:
            ReleaseYear = datetime.strptime(ReleaseYear, '%y-%m-%d').date()
        except ValueError:
            return jsonify("error":"ReleaseYear format ")
