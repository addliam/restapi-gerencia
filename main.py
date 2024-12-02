from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from gpt import Gpt
from repository import Repository
from csvformatter import Csvformatter
from pydantic import BaseModel
from typing import List
import json


class Recomendacion(BaseModel):
    titulo: str
    descripcion: str


class Respuesta(BaseModel):
    recomendaciones: List[Recomendacion]

class Gasto(BaseModel):
    categoria: str
    nombre: str
    monto: str
    fecha: str

class InfoPersonal(BaseModel):
    fecha_nacimiento: str
    ocupacion: str
    ingresos: str

# Definir el modelo para la solicitud que recibe la data v1
class DataRequest(BaseModel):
    gastos: List[Gasto]  # Una lista de objetos tipo Gasto
    infopersonal: InfoPersonal

app = FastAPI()
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
gpt = Gpt()
repository = Repository()
csvformatter = Csvformatter()


# TODO: to csv pasarlo a clase externa, agnostica del tipo de objeto
def infopersonal_to_csv(obj: InfoPersonal):
    return f"""fecha_nacimiento, ocupacion, ingresos\n{obj.fecha_nacimiento}, {obj.ocupacion}, {obj.ingresos}"""

def gastos_to_csv(listgasto: List[Gasto]):
    gastoscsv = ""
    for gasto in listgasto:
        gastoscsv += f"""{gasto.categoria}, {gasto.nombre}, {gasto.monto}, {gasto.fecha}\n"""
    return f"""categoria, nombre, monto, fecha\n{gastoscsv}"""

# Usar data pasada por body JSON {gastos, infopersonal}
@app.post("/sugerencia", response_model=Respuesta)
def getsugerenciacondata(data: DataRequest):
    gastos = data.gastos
    info_personal = data.infopersonal
    info_personal_csv = infopersonal_to_csv(info_personal)
    gastos_csv = gastos_to_csv(gastos)
    userprompt = f"{gastos_csv}\n{info_personal_csv}"
    response_txt = gpt.answer(userprompt)
    response_json = json.loads(response_txt)
    return (response_json)

# Esta ruta hace consulta MYSQL a tabla gasto y personal en base a userid
@app.get("/ia", response_model=Respuesta)
def getsugerenciaia(userid: Optional[int] = None):
    if not userid:
        raise HTTPException(
            status_code=404, detail="No se proporcionó el parámetro obligatorio 'userid'.")
    if not repository.check_user_exists(userid):
        raise HTTPException(
            status_code=404, detail="No existe el usuario con el 'userid' proporcionado.")
    gastos = repository.get_gasto_from_userid(userid)
    gastos_csv = csvformatter.format(gastos)
    # Consultar información personal del usuario
    infopersonal = repository.get_info_personal_from_userid(userid)
    infopersonal_csv = csvformatter.format(infopersonal)
    userprompt = f"{gastos_csv}\n\n{infopersonal_csv}"
    response_txt = gpt.answer(userprompt)
    response_json = json.loads(response_txt)
    return (response_json)



@app.get("/checkia")
def read_root():
    response = gpt.answer(
        "Quién fue el primer presidente de los Estados Unidos")
    return {"response": response}
