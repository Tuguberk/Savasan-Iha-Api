#!/usr/bin/env python
from typing import Optional
from typing import List
from fastapi import FastAPI,status,Response,Request
import json
from pydantic import BaseModel
import datetime
import random
import os

app = FastAPI()

class post_Telemetri(BaseModel): #İHA telemetri bilgilerini gönderirken kullanılacak veri yapısı
    class konumBilgileri(BaseModel): #İHA telemetri bilgileri
        takim_numarasi: int
        IHA_enlem: float
        IHA_boylam: float
        IHA_irtifa: float
        IHA_dikilme: int
        IHA_yonelme: int
        IHA_yatis: int
        zaman_farki:int
    class sunucuSaati(BaseModel): # Sunucunun saati
        saat: int
        dakika: int
        saniye: int
        milisaniye: int
    sunucuSaati: Optional[sunucuSaati] = None
    konumBilgileri: Optional[List[konumBilgileri]] = None

class user(BaseModel): #Kullanıcı bilgileri için kullanılacak veri yapısı
    kadi: str
    sifre: str

class takim_numarasi(BaseModel): #Takım numarası için kullanılacak veri yapısı
    takim_numarasi: int
class Telemetri(BaseModel): #İHA telemetri bilgileri için kullanılacak veri yapısı
    class GPSSaatiSubClass(BaseModel):#İHA'nın saati
        saat: int
        dakika: int
        saniye: int
        milisaniye: int
    takim_numarasi: int
    IHA_enlem: float
    IHA_boylam: float
    IHA_irtifa: float
    IHA_dikilme: int
    IHA_yonelme: int
    IHA_yatis: int
    IHA_hiz: int
    IHA_batarya: int
    IHA_otonom: bool
    IHA_kilitlenme: bool
    Hedef_merkez_X: int
    Hedef_merkez_Y: int
    Hedef_genislik: int
    Hedef_yukseklik: int
    GPSSaati: Optional[GPSSaatiSubClass] = None

class Kilitlenme(BaseModel): #İHA'nın kilitlenme bilgileri için kullanılacak veri yapısı
    class BaslangicSubClass(BaseModel): #İHA'nın kilitlenme başlangıç saati
        saat: int
        dakika: int
        saniye: int
        milisaniye: int

    class BitisSubClass(BaseModel): #İHA'nın kilitlenme bitiş saati
        saat: int
        dakika: int
        saniye: int
        milisaniye: int

    kilitlenmeBaslangicZamani: Optional[BaslangicSubClass] = None
    kilitlenmeBitisZamani: Optional[BitisSubClass] = None
    otonom_kilitlenme: bool



user_list = [] #Kullanıcı listesi
İHA = {} #İHA listesi
İHA_List = [] #İHA listesi
post_Telemetri_List = post_Telemetri() #İHA telemetri bilgileri
konumBilgileri_List = [] 
users_List = []

def saatAl(): #Sunucunun saati
    time = str(datetime.datetime.now())
    print(time)
    saat = time[11:23].split(":")
    return {"saat":saat[0],
    "dakika":saat[1],
    "saniye":saat[2].split(".")[0],
    "milisaniye":saat[2].split(".")[1]}


def connection_test(takim_numarasi):#İHA'nın bağlantı durumunu kontrol eder
    check = [i["takim_numarasi"] for i in users_List] #İHA listesindeki takım numaralarını alır
    for k in check:
        if k == takim_numarasi:
            return True
    return False

def İHA2post_Telemetri(item):#İHA telemetri bilgilerini post_Telemetri veri yapısına dönüştürür
    sununcuZamanı = saatAl()["milisaniye"]
    İHA_zamanı = item.GPSSaati.milisaniye
    return {"takim_numarasi":item.takim_numarasi,
            "IHA_enlem":item.IHA_enlem,
            "IHA_boylam":item.IHA_boylam,
            "IHA_irtifa":item.IHA_irtifa,
            "IHA_dikilme":item.IHA_dikilme,
            "IHA_yonelme":item.IHA_yonelme,
            "IHA_yatis":item.IHA_yatis,
            "zaman_farki":-(int(sununcuZamanı)-int(İHA_zamanı))#İHA'nın sunucuya gönderdiği zaman ile sunucunun saati arasındaki fark
            }

@app.get("/api/telemetri_al/")#İHA telemetri bilgilerini döndürür
def telemetri_al():
    post_Telemetri_List.sunucuSaati = saatAl()
    return post_Telemetri_List

@app.get("/api/telemetrileri_al/")#İHA telemetri bilgilerini döndürür
def telemetrileri_al():
    return İHA

@app.get("/api/kullanıcı_listele/")#Kullanıcı listesini döndürür
def kullanıcı_listele():
    return users_List

#[ ]Burası detaylandırılacak
@app.get("/")#Ana sayfayı döndürür
def read_root():
    return {"Docs": "/docs",
            "Redocs":"/redoc",
            "Owner":"@Zarqu0n and Tuguberk"}

@app.get("/api/sunucusaati")#Sunucunun saati
def sunucusaati():
    return saatAl()

@app.post("/api/telemetri_gonder",status_code=200)#İHA telemetri bilgilerini alır
async def telemetri_gonder(item: Telemetri,response: Response):

    İHA[item.takim_numarasi].update(item)#İHA telemetri bilgilerini günceller
    check = [t for t in İHA]
    item_post = İHA2post_Telemetri(item)
    if not (connection_test(item_post["takim_numarasi"])):#İHA'nın bağlantı durumunu kontrol eder
        response.status_code = status.HTTP_401_UNAUTHORIZED
        print("İHA bulunamadı")
        return {"Error":"İHA bulunamadı"}

    #FIXME Burası optimize edilecek
    check = [team["takim_numarasi"] for team in konumBilgileri_List]
    if (item_post["takim_numarasi"] in check):
        index = check.index(item_post["takim_numarasi"])
        konumBilgileri_List[index] = item_post
    else:
        konumBilgileri_List.append(item_post)

    post_Telemetri_List.konumBilgileri = konumBilgileri_List
    post_Telemetri_List.sunucuSaati = saatAl()
    return post_Telemetri_List

#[ ]Burasının kurulumu yapılmadı
@app.post("/api/kilitlenme_bilgisi")#İHA'nın kilitlenme bilgilerini alır
def kilitlenme_bilgisi(item: Kilitlenme):
    return item

@app.post("/api/giris",status_code=200 )#Kullanıcı girişi
def giris(item: user,response: Response):
    #get path previous folder and join with users.json
    users_path = "users.json"
    with open(users_path,"r") as f:#Kullanıcı listesini okur
        users = json.load(f)

    #FIXME Burası optimize edilecek
    for user in users: #Kullanıcı listesindeki kullanıcıları kontrol eder
        if user == item.kadi:#Kullanıcı adı kontrolü
            if users[item.kadi] == item.sifre:#Şifre kontrolü

                takim_numarasi = random.randint(343100,643100)#Kullanıcı giriş yaptığında takım numarası oluşturur
                #print(users_List)
                check = [i["kadi"] for i in users_List]#Kullanıcı listesindeki kullanıcı adlarını alır

                if (item.kadi in check):
                        index = check.index(item.kadi)
                        return users_List[index]["takim_numarasi"]#Kullanıcı tekrar giriş yaparsa takım numarasını döndürür
                else:#Kullanıcı ilk giriş yaparsa
                    İHA[takim_numarasi] = {}
                    users_List.append({"kadi":item.kadi,"sifre":item.sifre,"takim_numarasi":takim_numarasi})#Kullanıcı listesine kullanıcıyı ekler

                print(users_List)#Kullanıcı listesini yazdırır
                response.status_code = status.HTTP_200_OK#Kullanıcı girişi başarılı
                print("Success Giriş başarılı")
                return takim_numarasi#Kullanıcı takım numarasını döndürür

            else:#Kullanıcı şifresi yanlışsa
                print("Error Şifre yanlış")
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"Error":"Şifre yanlış"}
                
    #Kullanıcı bulunamazsa
    print("Error Kullanıcı bulunamadı")
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"Error":"Kullanıcı bulunamadı"}
    

@app.post("/api/cikis",status_code=200)#Kullanıcı çıkışı
def cikis(item: takim_numarasi,response: Response):
    if connection_test(item.takim_numarasi):
        #kullancıyı listeden sil
        check = [i["takim_numarasi"] for i in users_List]
        if (item.takim_numarasi in check):
            index = check.index(item.takim_numarasi)
            del users_List[index]
            print(users_List)
            response.status_code = status.HTTP_200_OK
            print("Success Çıkış başarılı")
            return {"Success":"Çıkış başarılı"}
        print("Success İHA çıkışı başarılı")
    else:
        print("Error İHA bulunamadı")
        return {"Error":"İHA bulunamadı"}


