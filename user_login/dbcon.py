import mysql.connector
import configparser




def get_mysql_connection():
  config = configparser.ConfigParser()
  config.read('configs.ini')
  username = config['SQL']['user']
  password = config['SQL']['password']
  host_ip = config['SQL']['host']
  dbase = config['SQL']['database']
  mydb = mysql.connector.connect(
    host=host_ip,
    user=username,
    passwd=password,
    database=dbase)
  return mydb



