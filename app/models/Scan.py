from mongoengine import *
from ..env.config import db
# from User import User

class APIScan(Document):
    api             = StringField(required=True)
    headers         = StringField(required=True)
    method          = StringField(required=True)
    parameters      = StringField(required=True)
    parameter       = StringField()
    vulnerability   = StringField(required=True)
    scanId          = StringField(required=True)
    updatedTime     = StringField()

#should get reports from here
class APIScanResults(Document):
    apiscans    = ListField(ReferenceField(APIScan))
    scanId      = StringField(required=True)
    hash        = StringField(required=True)
    updatedTime = StringField()
    config      = StringField()
