from mongoengine import DateTimeField,ObjectIdField,connect ,Document,BooleanField, StringField, FloatField, ListField, EmbeddedDocument, EmbeddedDocumentField, IntField, ReferenceField
import os
import datetime


# 📌 Modelo para Contactos

os.environ['DATABASE_URL'] = "mongodb+srv://admin:gJ66UV7FD1qs6jG0@valetest.8gw0zdt.mongodb.net/vera-app?retryWrites=true&w=majority"
os.environ['MY_DATABASE_NAME'] = "vera-app"

# Conectar a la base de datos usando la URL de conexión completa
connect(db=os.environ['MY_DATABASE_NAME'], host=os.environ['DATABASE_URL'])
class Contact(EmbeddedDocument):
    nombre = StringField(required=True)
    cargo = StringField(required=True)
    telefono = StringField()
    email = StringField()
    meta = {'collection': 'Contact'}

class Evaluator(Document):
    name = StringField(required=True)
    users = ListField(ReferenceField("User"))  # ✅ Usar cadena para evitar dependencias circulares
    businesses = ListField(ReferenceField("Business"))
    deals = ListField(ReferenceField("Deal"))

    createdAt = DateTimeField(default=datetime.datetime.utcnow)
    updatedAt = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'Evaluator'}

class User(Document):
    username = StringField(unique=True, required=True)
    password = StringField(required=True)
    role = StringField(choices=["ADMIN", "ANALYST"], required=True)
    evaluatorId = ReferenceField("Evaluator", required=True, reverse_delete_rule=2)  # Ref a Evaluator
    assignedBusinessIds = ListField(ReferenceField("Business"))  # Relación con Business (en el orm lo maneja como objtos)
    name = StringField()
    image =StringField()
    email = StringField()#se quito el unico
    emailVerified = BooleanField(default=False)
    createdAt = DateTimeField(default=datetime.datetime.utcnow)
    updatedAt = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'User'}


class FinancialStatement(Document):
    businessId = ReferenceField("Business", required=True)
    type = StringField(choices=["official", "draft"])
    years = ListField(IntField())
    datapoints = ListField(ReferenceField("FinancialDatapoint"))
    currency = StringField(default="PEN")
    scaleType = StringField(default="THOUSANDS")
    status = StringField(choices=["pending", "confirmed", "cancelled", "official"])
    createdAt = DateTimeField(default=datetime.datetime.utcnow)
    updatedAt = DateTimeField(default=datetime.datetime.utcnow)
    meta = {'collection': 'FinancialStatement'}


class Business(Document):
    name = StringField(required=True)
    ruc = StringField(required=True)
    razonSocial = StringField(required=True)
    contactos = ListField(EmbeddedDocumentField(Contact))
    ejecutivoCuenta = StringField()

    # Relaciones con analistas
    analistaIds = ListField(ReferenceField("User"))

    # Relaciones con Deals
    deals = ListField(ReferenceField("Deal"))

    # Evaluador
    evaluatorId = ObjectIdField()  # Agregado este campo
    evaluator = ReferenceField(Evaluator)

    # Estado financiero
    financialStatementId = ObjectIdField( required=False)  # Agregado este campo
    financialStatements = ListField(ReferenceField("FinancialStatement"))

    # Campos adicionales
    currency = StringField(default="PEN")
    scaleType = StringField(default="THOUSANDS")

    # Fechas
    createdAt = DateTimeField(default=datetime.datetime.utcnow)
    updatedAt = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'Business'}


# 📌 Modelo para Deal
class Deal(Document):
    title = StringField(required=True)
    status = StringField(required=True)
    business = ReferenceField(Business)
    value = FloatField()
    evaluator = ReferenceField(Evaluator)
    createdAt = IntField()
    updatedAt = IntField()
    meta = {'collection': 'Deal'}

# 📌 Modelo para DetailItem
class DetailItem(EmbeddedDocument):
    name = StringField(required=True)
    value = FloatField(required=True)
    meta = {'collection': 'DetailItem'}
# 📌 Modelo para FinancialDatapoint
class FinancialDatapoint(Document):
    value = FloatField(required=True)
    details = ListField(EmbeddedDocumentField(DetailItem))
    account = ReferenceField("Account")
    financialStatement = ReferenceField("FinancialStatement")
    year = IntField(required=True)
    createdAt = IntField()
    updatedAt = IntField()
    meta = {'collection': 'FinancialDatapoint'}

# 📌 Modelo para Account
class Account(Document):
    name = StringField(unique=True, required=True)
    displayName = StringField()
    statement = StringField()
    tags = ListField(StringField())
    valueType = StringField()
    priority = IntField()
    financialDatapoints = ListField(ReferenceField(FinancialDatapoint))
    meta = {'collection': 'Account'}

