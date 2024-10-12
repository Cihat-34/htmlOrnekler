from flask import Flask, request, jsonify
import pyodbc
from datetime import datetime
import traceback

app = Flask(__name__)

def get_db_connection():
    try:
        # Veritabanı bağlantısı için gerekli ayarları yapıyoruz
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DESKTOP-ON79G27\SQLEXPRESS;'  # Dikkat: Çift ters çizgi kaçış karakteri için gerekli
            'DATABASE=nova_akademi;'
            'Trusted_Connection=yes'
        )
        return conn
    except pyodbc.Error as e:
        print(f"Veritabanı bağlantı hatası: {e}")
        return None

@app.route('/add-user', methods=['POST'])
def add_user():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Veritabanına bağlanılamadı"}), 500

    try:
        # İstemciden gelen JSON verisini alıyoruz
        data = request.json
        print(f"Alınan veri: {data}")  # Hata ayıklama için alınan veriyi yazdırıyoruz

        # Gerekli verileri alıyoruz
        
        BookName = data.get('BookName')
        ReleaseYear = data.get('ReleaseYear')

        # Verilerin eksik olup olmadığını kontrol ediyoruz
        if BookName is None or ReleaseYear is None:
            return jsonify({"error": "Eksik veri: BookName ve ReleaseYear gerekli"}), 400

        # Yayın yılını doğrulama ve formatlama
        try:
            ReleaseYear = datetime.strptime(ReleaseYear, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "ReleaseYear formatı 'YYYY-MM-DD' olmalı"}), 400

        # Veritabanı işlemleri
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO Books (BookName, ReleaseYear)
            VALUES (?, ?)
        """
        cursor.execute(insert_query, (BookName, ReleaseYear))
        conn.commit()  # Veritabanına yapılan değişiklikleri kaydediyoruz
        cursor.close()

        return jsonify({"message": "Kitap başarıyla eklendi"}), 201

    except Exception as e:
        # Hata durumunda detaylı bilgi veriyoruz
        print(f"Hata: {traceback.format_exc()}")
        return jsonify({"error": "Bir hata oluştu", "details": str(e)}), 500

    finally:
        # Veritabanı bağlantısını kapatıyoruz
        conn.close()

@app.route('/delete-book', methods=['DELETE'])
def delete_book():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Veritabanına bağlanılamadı"}), 500
    
    try:
        data = request.json
        print(f"Alınan veri: {data}")  # Hata ayıklama için alınan veriyi yazdırıyoruz
        BookID = data.get('BookID')

        if BookID is None:
            return jsonify({"error": "Eksik veri: BookID gerekli"}), 400
        
        cursor = conn.cursor()
        delete_query = "DELETE FROM Books WHERE BookID = ?"
        cursor.execute(delete_query, (BookID,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Kitap bulunamadı"}), 404
        
        cursor.close()
        return jsonify({"message": "Kitap başarıyla silindi"}), 200

    except Exception as e:
        print(f"Hata: {traceback.format_exc()}")
        return jsonify({"error": "Bir hata oluştu", "details": str(e)}), 500

    finally:
        conn.close()


@app.route('/update-book', methods=['PUT'])
def update_book():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Veritabanına bağlanılamadı"}), 500

    try:
        # İstemciden gelen JSON verisini alıyoruz
        data = request.json
        print(f"Alınan veri: {data}")

        # Gerekli verileri alıyoruz
        BookID = data.get('BookID')
        BookName = data.get('BookName')
        ReleaseYear = data.get('ReleaseYear')

        # Verilerin eksik olup olmadığını kontrol ediyoruz
        if BookID is None or BookName is None or ReleaseYear is None:
            return jsonify({"error": "Eksik veri: BookID, BookName ve ReleaseYear gerekli"}), 400

        # Yayın yılını doğrulama ve formatlama
        try:
            ReleaseYear = datetime.strptime(ReleaseYear, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "ReleaseYear formatı 'YYYY-MM-DD' olmalı"}), 400

        # Veritabanı işlemleri
        cursor = conn.cursor()
        # Kitap güncelleme sorgusunu hazırlıyoruz
        update_query = """
            UPDATE Books
            SET BookName = ?, ReleaseYear = ?
            WHERE BookID = ?
        """
        # Sorguyu çalıştırıyoruz
        cursor.execute(update_query, (BookName, ReleaseYear, BookID))
        conn.commit()  # Değişiklikleri kaydediyoruz

        # Etkilenen satır sayısını kontrol ediyoruz
        if cursor.rowcount == 0:
            return jsonify({"error": "Kitap bulunamadı"}), 404

        cursor.close()

        return jsonify({"message": "Kitap başarıyla güncellendi"}), 200

    except Exception as e:
        # Hata durumunda detaylı bilgi veriyoruz
        print(f"Hata: {traceback.format_exc()}")
        return jsonify({"error": "Bir hata oluştu", "details": str(e)}), 500

    finally:
        # Veritabanı bağlantısını kapatıyoruz
        conn.close()

if __name__ == '__main__':
    # Uygulamayı başlatıyoruz, debug modunda
    app.run(debug=True)