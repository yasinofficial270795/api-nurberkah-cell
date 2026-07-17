from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
import os

app = FastAPI()

# Mengizinkan aplikasi frontend mengakses API ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === URL MONGODB ANDA SUDAH DIMASUKKAN DI BAWAH INI ===
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://yasinofficial270795_db_user:iPzbLYU3JKXa6fa5@cluster0.cuxhvsu.mongodb.net/?appName=Cluster0")
# ======================================================

# Menghubungkan ke Database
client = MongoClient(MONGO_URL)
db = client.nurberkah_db
transaksi_collection = db.transaksi

# Format Data
class Transaksi(BaseModel):
    id: int
    tanggal: str
    pelanggan: str
    nohp: str
    produk: str
    modal: float
    jual: float
    metode: str
    lunas: bool
    bukti: str = ""

@app.get("/")
def read_root():
    return {"message": "Server API Nur Berkah Cell Aktif 24 Jam!"}

@app.get("/api/transaksi")
def get_transaksi():
    # Mengambil semua data dari database
    data = list(transaksi_collection.find({}, {"_id": 0}))
    return data

@app.post("/api/transaksi")
def tambah_transaksi(trx: Transaksi):
    # Menyimpan data baru ke database
    transaksi_collection.insert_one(trx.dict())
    return {"message": "Data berhasil disimpan ke Database!"}

@app.put("/api/transaksi/lunas/{id_trx}")
def lunasi_transaksi(id_trx: int):
    # Mengubah status menjadi lunas
    transaksi_collection.update_one({"id": id_trx}, {"$set": {"lunas": True}})
    return {"message": "Status hutang berhasil dilunasi!"}

@app.delete("/api/transaksi/{id_trx}")
def hapus_transaksi(id_trx: int):
    # Menghapus data
    transaksi_collection.delete_one({"id": id_trx})
    return {"message": "Data berhasil dihapus dari Database!"}
