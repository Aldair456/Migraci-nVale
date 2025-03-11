import json
from mongoengine import connect
import sys
sys.path.append(r"C:\Users\semin\OneDrive\Escritorio\MARCELO\jhimy\migracion\service-eeff")
from utils.model import FinancialDatapoint  # Modelo en MongoEngine
from utils.response import Response  # Clase Response para formatear respuestas
from utils.serializable import serialize_document
"""
Verifica si el token de autorización está presente y es válido (Bearer Token).

Si falta o es incorrecto → Devuelve 401 Unauthorized.
Lee el cuerpo de la solicitud (body) y extrae:

businessId: El ID del negocio al que pertenecen los datos.
data: Una lista de objetos con información financiera.
Si falta alguno → Devuelve 400 Bad Request.
Inserta los datos financieros en MongoDB:

Recorre cada objeto en data y lo guarda en la colección FinancialDatapoint.
Asigna el businessId a cada registro.
Devuelve 201 Created con los datos insertados.

Si ocurre un error inesperado, devuelve 500 Internal Server Error
"""
##falta probar
def lambda_handler(event, context):
    # todo este codigo Este código es una función AWS Lambda en Python que inserta datos financieros (FinancialDatapoint) en una base de datos MongoDB.


    try:
        # Verificar autorización con el Bearer Token
        headers = event.get("headers", {})
        auth_header = headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return Response(status_code=401, body={"error": "No autorizado"}).to_dict()

        # Leer el cuerpo de la solicitud
        body = json.loads(event.get("body", "{}"))
        business_id = body.get("businessId")
        data = body.get("data", [])

        if not business_id or not data:
            return Response(status_code=400, body={"error": "Faltan datos requeridos"}).to_dict()

        # Insertar los datos en la base de datos
        created_data = []
        for item in data:
            new_datapoint = FinancialDatapoint(
                **item,  # Agrega los datos del objeto
                businessId=business_id  # Asocia el businessId
            )
            
            new_datapoint.save()
            created_data.append(serialize_document(new_datapoint.to_mongo().to_dict()))

        return Response(status_code=201, body=created_data).to_dict()

    except Exception as e:
        return Response(status_code=500, body={"error": "Error interno del servidor", "details": str(e)}).to_dict()


if __name__ == "__main__":
    # Simulación de prueba local
    test_event = {
        "headers": {"Authorization": "Bearer test_token"},
        "body": json.dumps(
            {
                "businessId": "67802e0a80547b162bf07dd0",
                "data":[
                {"value": 32923,
                "details": [
                    {
                        "name": "CASH",
                        "value": 32923,
                    }
                ],
                "accountId": "67899c57c434d7c2c93b39e4",
                "financialStatementId": "67bf82615bf475b6d291e2a2",
                "yearId": "67915f32680ce769f535a7a9"}]
            }
        )
    }



    print(lambda_handler(test_event, None))
