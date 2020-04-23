from mongoengine import *

connect('cash')
dict_cashe = []


class User(Document):
    id_user = StringField(max_lenght=100)
    balance = FloatField(default=0.0)
    depositCount = IntField(default=0)
    depositSum = FloatField(default=0.0)
    betCount = IntField(default=0)
    betSum = FloatField(default=0.0)
    winCount = IntField(default=0)
    winSum = FloatField(default=0.0)
    token = StringField(max_lenght=100)


class Deposit_data(Document):
    userId = StringField(max_lenght=100)
    depositId = StringField(max_lenght=100)
    befor_balance = FloatField(default=0.0)
    after_balance = FloatField(default=0.0)
    time = DateTimeField()


class Transaction_data(Document):
    userId = StringField(max_lenght=100)
    transactionId = StringField(max_lenght=100)
    amount_of_change = FloatField(default=0.0)
    befor_balance = FloatField(default=0.0)
    after_balance = FloatField(default=0.0)
    time = DateTimeField()                  