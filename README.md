# Auto Trade

Automate your real-time trades with AI.


## Getting Started

###  Frontend
In AutoTrade-master folder, run following commands in order
Create virtual environment using venv in python
```
python3 -m venv dash_env
```

Above command will create a ‘dash_env’ folder. After that folder is created, run the following command to activate the environment
```
source dash_env/bin/activate
```
The virtual environment should be activated, you will see (dash_env) written at the beginning of your terminal prompt.
After that go to frontend folder and  install the dependencies from the requirements.txt file using the command:
```
pip install -r requirements.txt
```

The front-end is now setup. To see a demo of just the front-end run the command,

```
python app.py 
```

###  User Login
Go to [mysql](https://dev.mysql.com/downloads/mysql/) and download *mysql 5.7*  and install it 
Log into installed mysql database and create a database and run following mysql query
```
	CREATE TABLE users (
        userID varchar(25) NOT NULL,
	password varchar(255) NOT NULL,
	account varchar(50),
        PRIMARY KEY (userID)
);
```
In the AutoTrade-master folder go to user_login folder and do following
Open config file and set db user, db password, database name and database host
Install dependencies using following command

```
pip install mysql-connector==2.2.9
```

The user-login is now setup. To see a user login run the command,
```
python app.py 
```


### Deep Learning Model
##### Prerequisites 

```
Anaconda (python 3.7)
keras 2.2.4
tensorflow 1.13.1
numpy 1.16.2
pandas 0.23.4
scikit-learn-0.20.1

```


## Versioning
For the versions available, see the tags on this repository.
