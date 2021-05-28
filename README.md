# python_DevOps

## Install virtual env and check python version
 ```sh
 python3 --version
 python3 -m pip install --upgrade pip
 pip3 install virtualenv
 ```
 
## Mount a enviroment for our api
```sh
virtualenv p --python=python3
source p/bin/activate
deactivate 
```
## Install the requirements
```sh
requirements.txt
```



## Run Notebook

```sh
cd notebooks
jupyter notebook
```

```sh
Intro_python
Intro_pandas
Intro_lambdas
Check_disponibilty
Get_all_assets_website for a CDN
```


## Install and configure Postgresql

```sh
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt install postgresql -y

sudo su postgres
psql -U postgres -c "CREATE ROLE ubuntu;"
psql -U postgres -c "ALTER ROLE  ubuntu  WITH LOGIN;"
psql -U postgres -c "ALTER USER  ubuntu  CREATEDB;"
psql -U postgres -c "ALTER USER  ubuntu  WITH PASSWORD 'ubuntu';"
exit
```

## Generate database and seed it
```sh
flask db_create && flask db_seed 
```

### Check  API

-  health
```sh
curl localhost:5000/
```
- GET all quotes
```sh
curl --location --request GET 'http://0.0.0.0:5000/quotes' --data-raw ''
```
- POST a quote

```sh
curl --location --request POST 'http://0.0.0.0:5000/add_quote' \
--form 'quote_desc=D'\''oh!' \
--form 'quote_type=Motivation' \
--form 'author=Homero Simpson'
```
- PUT a quote

```sh
curl --location --request PUT 'http://0.0.0.0:5000/update_quote/6' \
--form 'quote_desc=D'\''oh!' \
--form 'quote_type=Motivation' \
--form 'author=Homero Jay  Simpson'
```
- POST a quote

```sh
curl --location --request POST 'http://0.0.0.0:5000/add_quote' \
--form 'quote_desc=Tienes el micronfono apagado' \
--form 'quote_type=Motivation' \
--form 'author=Benjamin'
```
- DELETE a quote

```sh
curl --location --request DELETE 'http://0.0.0.0:5000/remove_quote/7'
```


# webhooks

```sh
import pymsteams
myTeamsMessage = pymsteams.connectorcard("")
myTeamsMessage.text("this is my text")
myTeamsMessage.send()

```
## Sender
```sh
import requests
import json 

webhook_url='http://127.0.0.1:5000/webhook'

data ={'name' : 'Benjamin', 
        'Chanel URL': 'Test url'}

r = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type':'application/json'})

```

## Receiver 
```sh

from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        print(request.json)
        return 'success', 200
    else:
        abort(400)

if __name__ == '__main__':
    app.run()

```




