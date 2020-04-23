from flask import Flask
from flask_restful import Api, Resource, reqparse
import datetime
from models import dict_cashe, User, Deposit_data, Transaction_data
app = Flask(__name__)
api = Api(app)


class AddUser(Resource):
    """
    this is class add user with url "/user/create" and input format json like:
    {
        "id": "1",
        "balance": 0.0,
        "token": "testtoken"
    }
    """

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("balance")
        parser.add_argument("token")
        params = parser.parse_args()
        for item in dict_cashe:
            if params["id"] == item["id_user"]:
                return {"error":f"The user with id = {params['id']} already exists"} 
        try:
            float(params["balance"])
        except ValueError:
            return {"error":"your balance shoud be integer like 0.0"} 
        item = {
            "id_user": params["id"],
            "balance":float(params["balance"]),
            "token": params["token"]
        }
        dict_cashe.append(item)
        for i in ['depositCount', 'depositSum', 'betCount', 'betSum', 'winCount', 'winSum']:
            if item.get(f'{i}', None) == None:
                item[f'{i}'] = 0
        return {"error":""}


class GetUser(Resource):
    """
    this is class get user with url "/user/get" and input format json like:
    {
        "id": "1",
        "token": "testtoken"
    }
    """

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("token")
        params = parser.parse_args()
        for key in dict_cashe:
            if key["id_user"] == params["id"] and key["token"] == params["token"]:
                return key
        return {'error' : f'The user with id = {params["id"]} and token = \'{params["token"]}\' not found'}
   

class AddDeposit(Resource):
    """
    this is class add deposit for user with url "/user/deposit" and input format json like:
    {
        "userId": "1",
        "depositId" : 1258,
        "amount" : 20,
        "token": "testtoken"
    }
    """

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("userId")
        parser.add_argument("depositId")
        parser.add_argument("amount")
        parser.add_argument("token")
        params = parser.parse_args()
        for key in dict_cashe:
            if key["id_user"] == params["userId"] and key["token"] == params["token"]:
                item = {
                    "userId" : params["userId"],
                    "depositId" : params["depositId"],
                    'befor_balance' : key['balance'],
                    'after_balance' : float(key['balance']) + float(params['amount']),
                    "time" : datetime.datetime.now()
                }
                Deposit_data(**item).save()
                key['balance'] += float(params['amount'])
                key['depositSum'] += float(params['amount'])
                key['depositCount'] += 1
                user_up = User.objects(id_user=key["id_user"], token=key["token"])
                if user_up:
                    user_up.update(**key)
                else:
                    User(**key).save() 
                return {'error':'', 'balance':key['balance']}
        return {'error':'Something wrong'}


class Transaction(Resource):
    """
    this is class add deposit for user with url "/user/transaction" and input format json like:
    {
        "userId": "1",
        "transactionId": 1260,
        "type": "Win",
        "amount": 30.0,
        "token": "testtoken"
    }
    """

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("userId")
        parser.add_argument("transactionId")
        parser.add_argument("type")
        parser.add_argument("amount")
        parser.add_argument("token")
        params = parser.parse_args()
        if (params['type'] == 'Bet') or (params['type'] == 'Win'):
            for key in dict_cashe:
                if key["id_user"] == params["userId"] and key["token"] == params["token"]:
                    if key['balance'] < 0:
                        return {'error':'You cannot do this operation, because your balance negative'}
                    item = {
                        "userId" : params["userId"],
                        "transactionId" : params["transactionId"],
                        'amount_of_change' : params["amount"],
                        'befor_balance' : key['balance'],
                        'after_balance' : float(key['balance']) + float(params['amount']),
                        "time" : datetime.datetime.now()
                    }
                    Transaction_data(**item).save()
                    key[f"{params['type'].lower()}Count"] += 1
                    key[f"{params['type'].lower()}Sum"] += float(params['amount'])

                    key['balance'] += float(params['amount'])
                    user_up = User.objects(id_user=key["id_user"], token=key["token"])
                    if user_up:
                        user_up.update(**key)
                    else:
                        User(**key).save()
                    return {'error':'', 'balance':key['balance']}
        else:
            return {'error':'In type should be \'Win\' or \'Bet\''}    
        return {'error' : f'The user with id = {params["userId"]} and token = \'{params["token"]}\' not found'}


api.add_resource(AddUser, "/user/create")
api.add_resource(GetUser, "/user/get")
api.add_resource(AddDeposit, "/user/deposit")
api.add_resource(Transaction, "/user/transaction")


if __name__ == '__main__':
    app.run()
