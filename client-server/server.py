from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/area")
def calcular_area(base: float, altura: float):
    if base <= 0 or altura <= 0:
        raise HTTPException(status_code=400, detail="Valores devem ser positivos")

    area = (base * altura) / 2
    return {"area": area}