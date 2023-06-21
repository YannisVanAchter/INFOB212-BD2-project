# INFOB212-BD2-project

## How to install the sql requerements for python?
Check you have installed python 3.11 or higher and use the following command
```bash
$ python -m venv venv
...
$ venv/Scripts/activate
$ pip install -r requerements.txt
```

## To run the app
In the repertory with the docker-compose and Dockerfile type:
```bash
$ cls
$ docker-compose build
$ docker-compose up
```
If this isn't the first time you run the app, use:
```bash
$ cls
$ docker-compose down 
$ docker-compose build 
$ docker-compose up
```

⚠️Use python 3.11 or higher⚠️


Into another terminal use (please wait till the docker container has been created and started):
- On first run app running
```bash
$ cd src
src $ python setup.py
src $ python main.py
```
- After first run app running
```bash	
$ cd src
src $ python main.py
```

## Open relational schema
To open Relationship-Association schema model use [DB-Main](https://www.db-main.eu/getit/) the file is stored [here](./schema/conceptual-schema.lun)

