# Installation and Running

```
git clone https://github.com/BUYA-GH/bearrobotics_assign.git {folder name which you want to clone}

cd {folder name which you want to clone}

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

First, You need Python to run.

I developed this project in Python version 3.8.13, so Running this project in python version 3.8 won't cause any problems.

After cloning this project and installing additional package by pip, just running this command `python manage.py migrate` and `python manage.py runserver`

# do Test
If you want to running test codes, just run this command

```
python manage.py test accounts.tests.ATMTestCase
```

# API List
All of the API's method is `POST`, because data associated with card and account should be handled safely.

Below is API List

and BASE URL is http://127.0.0.1:8000/atm/v0/

```json
[   
    {
        "id": 1,
        "method": "post",
        "path": "card/create/",
        "name": "create card and account",
        "request_body": {
            "pinNum": "1234"
        },
        "response": {
                "cardNum": "4495137780342310",
                "accountNumber": "110-091-762798"
        }
    },

    {
        "id": 2,
        "method": "post",
        "path": "card/",
        "name": "insert card and check pin number",
        "request_body": {
	        "cardNum": "4495137780342310",
	        "pinNum": "9443"
        },
        "response": {
	        "cardNum": "4495137780342310",
	        "accountNumber": "110-091-762798"
        }
    },

    {
        "id": 3,
        "method": "post",
        "path": "transaction/balance/",
        "name": "check account's balance",
        "request_body": {
	        "accountNumber": "110-091-762798"
        },
        "response": {
	        "accountNumber": "110-091-762798",
	        "balance": 30,
	        "author": "4495137780342310"
        }
    },

    {
        "id": 4,
        "method": "post",
        "path": "transaction/deposit/",
        "name": "do deposit",
        "request_body": {
	        "accountNumber": "110-091-762798",
	        "receivedPaid": 30
        },
        "response": {
            "account": "110-091-762798",
            "receivedPaid": 30,
            "is_deposit": true,
            "transact_at": "2022-12-04T11:59:27.705448Z",
            "balance": 90
        }
    },

    {
        "id": 5,
        "method": "post",
        "path": "transaction/withdraw/",
        "name": "do withdraw",
        "request_body": {
	        "accountNumber": "110-091-762798",
	        "receivedPaid": 30
        },
        "response": {
            "account": "110-091-762798",
            "receivedPaid": 30,
            "is_deposit": false,
            "transact_at": "2022-12-04T11:59:27.705448Z",
            "balance": 90
        }
    },

    {
        "id": 6,
        "method": "post",
        "path": "transaction/list/",
        "name": "get transaction list",
        "request_body": {
            "accountNumber": "110-091-762798"
        },
        "response": [
            {
                "account": "110-091-762798",
                "receivedPaid": 30,
                "is_deposit": true,
                "transact_at": "2022-12-04T11:05:52.293779Z"
            },
            {
                "account": "110-091-762798",
                "receivedPaid": 30,
                "is_deposit": false,
                "transact_at": "2022-12-04T11:05:28.950724Z"
            }
        ]
    }
]
```