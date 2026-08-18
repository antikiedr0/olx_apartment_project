from fastapi import FastAPI
from pydantic import BaseModel
from ..model import make_prediction
import uvicorn

class Item(BaseModel):
    powierzchnia : int
    liczba_pokoi : int
    miasto : str
    rynek : str
    rodzaj_zabudowy : str
    umeblowane : bool | None = None

class MyServer:
    @app.get("/")
    def healthcheck():
        return {"Server is running"}

    @app.post("/predict")
    def predict_outcome(item: Item):
        respone = make_prediction.predict(item.powierzchnia, item.liczba_pokoi, item.miasto, item.rynek, item.rodzaj_zabudowy, item.umeblowane)
        return {"cena_m2": respone}
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 5000)