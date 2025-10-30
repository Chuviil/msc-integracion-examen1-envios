from apiflask import Schema
from apiflask.fields import String

class EnvioIn(Schema):
    id_envio = String(required=True)
    cliente = String(required=True)
    direccion = String(required=True)
    estado = String(required=True)
