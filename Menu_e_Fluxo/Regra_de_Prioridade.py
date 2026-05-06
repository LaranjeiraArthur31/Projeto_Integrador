import mysql.connector as mysql_connector
from dotenv import load_dotenv

load_dotenv()

class MySQLDatabase:
    self._host = os.getenv("HOST")
    self._username = os.getenv("USERNAME")
    self._passwd = os.getenv("PASSWD")
    self._database = os.getenv("DATABASE")
    self.conn = None

def _connecting(self):
    return mysql_connector.connect(
        host= self._username,
        password=self._passwd,
        host=self._host,
        database=._database
    )