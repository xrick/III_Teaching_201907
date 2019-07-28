import sqlite3
from sqlite3 import Error
import time
import os
#STOCK_TA
QUERY_EXISTED = False

def checkAndCreatDB(DBName):
    if_file = os.path.isfile(DBName)
    _res = None
    if not if_file:
       _res = CreateDB(DBName)
    return _res

def CreateDB(DBName):
    try:
        conn = sqlite3.connect(DBName) 
        c = conn.cursor()
        c.execute('CREATE TABLE CLIENTS([reply_token] text ,[query_time] text, [sessionstatus] integer, [qyeryType] text)')
        c.close()
        return conn
    except Error as e:
        print("The error is {}".format(e))
        return None
  

def BuildConnectionToRecordDB(DBName):
    try:
        conn = checkAndCreatDB(DBName)
        if conn:
            return conn
        else:
           conn = sqlite3.connect(DBName)
        return conn
    except Error as e:
        print(e)
        return None

def insertNewQueryRecord(cur,requestID,queryType):
    newSql = 'insert into queryrecordtb(reply_token,querytime,sessionstatus,queryType) VALUES(?,?,?,?)'
    cur.execute(newSql,(requestID,str(time.time()),1,queryType))
    return cur.lastrowid

def checkIfQueryExist(cur,requestID):
    QUERY_EXISTED = False
    cur.execute("select reply_token, queryType from queryrecordtb where reply_token='{}' order by querytime".format(requestID))
    row = cur.fetchone()
    if row :
        QUERY_EXISTED = True
        return QUERY_EXISTED,row
    return QUERY_EXISTED, None

def delAnsweredQuery(cur,requestID,queryType):
    delSQL = "delete from queryrecordtb where reply_token='{}' and queryType='{}'".format(
        requestID, queryType)
    print(delSQL)
    cur.execute(delSQL)

def delAllRowsOfID(cur,requestID):
    delall = "delete from queryrecordtb where reply_token='{}'".format(requestID)
    print(delall)
    cur.execute(delall)

