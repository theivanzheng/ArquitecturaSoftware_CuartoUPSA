from fastapi import FastAPI

app = FastAPI(title="Taller de Coches — API con base de datos")


@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API del Taller de Coches con persistencia"}
