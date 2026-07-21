from datetime import date, datetime
from decimal import Decimal
from uuid import UUID
from decouple import config

from pymongo import MongoClient

client = MongoClient(config('MONGO_URI'), uuidRepresentation='standard')
db = client['auditoria_restaurante']
logs_colletion = db['logs_movimientos']


def normalizar_para_mongo(value):
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: normalizar_para_mongo(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalizar_para_mongo(item) for item in value]
    return value