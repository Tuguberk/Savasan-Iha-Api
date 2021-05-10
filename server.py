from typing import Optional

from fastapi import FastAPI

from pydantic import BaseModel
##############
import datetime

app = FastAPI()


class Telemetri(BaseModel):
    class GPSSaatiSubClass(BaseModel):
        saat: int
        dakika: int
        saniye: int
        milisaniye: int
    takim_numarasi: int
    IHA_enlem: float
    IHA_boyla: float
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

class Kilitlenme(BaseModel):
    class BaslangicSubClass(BaseModel):
        saat: int
        dakika: int
        saniye: int
        milisaniye: int

    class BitisSubClass(BaseModel):
        saat: int
        dakika: int
        saniye: int
        milisaniye: int

    kilitlenmeBaslangicZamani: Optional[BaslangicSubClass] = None
    kilitlenmeBitisZamani: Optional[BitisSubClass] = None
    otonom_kilitlenme: bool


def saatAl():
    time = str(datetime.datetime.now())
    print(time)
    saat = time[11:23].split(":")
    return {"saat":saat[0],"dakika":saat[1],"saniye":saat[2].split(".")[0],"milisaniye":saat[2].split(".")[1]}

@app.get("/")
def read_root():
    return {"Docs": "/docs",
            "Redocs":"/redoc",
            "Owner":"@Tuguberk"}

@app.get("/api/sunucusaati")
def sunucusaati():
    return saatAl()

@app.post("/api/telemetri_gonder")
async def telemetri_gonder(item: Telemetri):
    return {"sistemSaati":saatAl(),
            "konumBilgileri":[
                {
                    "takim_numarasi":1,
                    "iha_enlem":500,
                    "iha_boylam":500,
                    "iha_irtifa":500,
                    "iha_dikilme":5,
                    "iha_yonelme":256,
                    "iha_yatis":0,
                    "zaman_farki":93 #dinamik hale getir
                    },
                ]}

@app.post("/api/kilitlenme_bilgisi")
def kilitlenme_bilgisi(item: Kilitlenme):
    return item

# @app.post("/api/giris")
# def giris():
    # return {}

# @app.get("/api/cikis")
# def cikis():
    # return {}
