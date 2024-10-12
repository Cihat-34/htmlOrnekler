try:
    with open("veriler.txt","r")as dosya:
        icerik = dosya.read()
except FileNotFoundError:
    print("Dosya bulunamadı.")