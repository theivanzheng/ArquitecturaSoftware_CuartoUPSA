from fastapi import FastAPI

app = FastAPI(title="Taller de Coches — API básica")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"mensaje": "Bienvenido a la API del Taller de Coches"}
