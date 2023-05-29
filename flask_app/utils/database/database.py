import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import hashlib
import os
import cryptography
from cryptography.fernet import Fernet
from pprint import pprint
from math import pow
import random
from .generateNFT import generateRandomJPG
from datetime import datetime

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'
        self.tables         = ['institutions', 'positions', 'experiences', 'skills','feedback', 'users',"nftusers","nftinfo","nftrecord"]
        
        # NEW IN HW 3-----------------------------------------------------------------
        self.encryption     =  {   'oneway': {'salt' : b'averysaltysailortookalongwalkoffashortbridge',
                                                 'n' : int(pow(2,5)),
                                                 'r' : 9,
                                                 'p' : 1
                                             },
                                'reversible': { 'key' : '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='}
                                }
        #-----------------------------------------------------------------------------

    def query(self, query = "SELECT * FROM users", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def createTables(self, purge=False, data_path = 'flask_app/database/'):
        ''' FILL ME IN WITH CODE THAT CREATES YOUR DATABASE TABLES.'''

        #should be in order or creation - this matters if you are using forign keys.
         
        if purge:
            for table in self.tables[::-1]:
                self.query(f"""DROP TABLE IF EXISTS {table}""")
            
        # Execute all SQL queries in the /database/create_tables directory.
        for table in self.tables:
            
            #Create each table using the .sql file in /database/create_tables directory.
            with open(data_path + f"create_tables/{table}.sql") as read_file:
                pprint("create table: " + table)
                create_statement = read_file.read()
            self.query(create_statement)

            # Import the initial data
            try:
                params = []
                with open(data_path + f"initial_data/{table}.csv") as read_file:
                    scsv = read_file.read()            
                for row in csv.reader(StringIO(scsv), delimiter=','):
                    params.append(row)
            
                # Insert the data
                cols = params[0]; params = params[1:] 
                self.insertRows(table = table,  columns = cols, parameters = params)
            except:
                print('no initial data')

    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        
        # Check if there are multiple rows present in the parameters
        has_multiple_rows = any(isinstance(el, list) for el in parameters)
        keys, values      = ','.join(columns), ','.join(['%s' for x in columns])
        
        # Construct the query we will execute to insert the row(s)
        query = f"""INSERT IGNORE INTO {table} ({keys}) VALUES """
        if has_multiple_rows:
            for p in parameters:
                query += f"""({values}),"""
            query     = query[:-1] 
            parameters = list(itertools.chain(*parameters))
        else:
            query += f"""({values}) """                      
        pprint(query)
        pprint(parameters)
        insert_id = self.query(query,parameters)[0]['LAST_INSERT_ID()']         
        return insert_id
    def getResumeData(self):
        result = {}
        institutions = self.query("SELECT * FROM institutions")
        for institution in institutions:
            positions = self.query("SELECT * FROM positions WHERE inst_id = %s",(institution['inst_id'],))
            institution['positions'] = {}
            for position in positions:
                experiences = self.query("SELECT * FROM experiences WHERE position_id=%s",(position['position_id'],))
                position['experiences'] = {}
                for experience in experiences:
                    skills = self.query("SELECT * FROM skills WHERE experience_id=%s",(experience['experience_id'],))
                    experience['skills'] = {}
                    for skill in skills:
                        experience['skills'][int(skill['skill_id'])] = skill
                    position['experiences'][int(experience['experience_id'])] = experience
                institution['positions'][int(position['position_id'])] = position
            result[int(institution['inst_id'])] = institution
        # pprint(result)

        pprint('I create and populate database tables.')
        return result

#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
    def createUser(self, email='me@email.com', password='password', role='user'):
        # Check if the user already exists.
        #encryptedEmail = self.reversibleEncryption('encrypt',email)
        user = self.query("SELECT * FROM users WHERE email = %s",(email,))
        if not user:
            encryptedPassword = self.onewayEncrypt(password)
            insert_id = self.insertRows(table='users',columns=['email', 'password','role'],parameters=[email,encryptedPassword,role])
            if insert_id != 0:
                return {'success': 1}
            else:
                return {'success': 0}
    # create user and generate random token(money)
    def nft_createUser(self, email='me@email.com', password='password', role='user'):
        user = self.query("SELECT * FROM nftusers WHERE email = %s",(email,))
        if not user:
            encryptedPassword = self.onewayEncrypt(password)
            insert_id = self.insertRows(table='nftusers',columns=['email', 'password','role','token'],parameters=[email,encryptedPassword,role,str(random.randint(0,1000))])
            if insert_id!= 0:
                return {'success': 1}
            else:
                return {'success': 1}

    def authenticate(self, email='me@email.com', password='password'):
        encryptedPassword = self.onewayEncrypt(password)
        user = self.query("SELECT * FROM users WHERE email = %s and password = %s",(email,encryptedPassword))
        if user:
            return {'success': 1}
        else:
            return {'success': 0}
        
    def nft_authenticate(self, email='me@email.com', password='password'):
        encryptedPassword = self.onewayEncrypt(password)
        user = self.query("SELECT * FROM nftusers WHERE email = %s and password = %s",(email,encryptedPassword))
        if user:
            return {'success': 1}
        else:
            return {'success': 0}

    def onewayEncrypt(self, string):
        encrypted_string = hashlib.scrypt(string.encode('utf-8'),
                                          salt = self.encryption['oneway']['salt'],
                                          n    = self.encryption['oneway']['n'],
                                          r    = self.encryption['oneway']['r'],
                                          p    = self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string


    def reversibleEncrypt(self, type, message):
        fernet = Fernet(self.encryption['reversible']['key'])
        
        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message

###################
# NFT
###################
    def getUserIDByEmail(self, email):
        user = self.query("SELECT * FROM nftusers WHERE email = %s",(email,))
        if user:
            return user[0]['user_id']
        else:
            return 0
    def createNFT(self,user,description,token):
        userID = self.getUserIDByEmail(user)
        path = generateRandomJPG()
        insert_id = self.insertRows(table='nftinfo',columns=['ownerID','description','token','path'],parameters=[userID,description,token,path])
        if insert_id!= 0:
            return True
        else:
            return False
    def uploadNFT(self,user,description,token,path):
        userID = self.getUserIDByEmail(user)
        insert_id = self.insertRows(table='nftinfo',columns=['ownerID','description','token','path'],parameters=[userID,description,token,path])
        if insert_id!= 0:
            return True
        else:
            return False
    def getUserAllNFTs(self,user):
        userID = self.getUserIDByEmail(user)
        nfts = self.query("SELECT * FROM nftinfo WHERE ownerID = %s",(userID,))
        if nfts:
            return nfts
        else:
            return []
    def getOtherAllNFTs(self,user):
        userID = self.getUserIDByEmail(user)
        nfts = self.query("SELECT * FROM nftinfo WHERE ownerID!= %s",(userID,))
        if nfts:
            return nfts
        else:
            return []
    def buyNFT(self,user,nftID):
        userID = self.getUserIDByEmail(user)
        nft = self.query("SELECT * FROM nftinfo WHERE id = %s",(nftID,))[0]
        user = self.query("SELECT * FROM nftusers WHERE user_id = %s",(userID,))[0]
        if float(user['token']) < float(nft['token']):
            return {
                "success": 0,
                "message": "You don't have enough tokens"
            }
        seller = self.query("SELECT * FROM nftusers WHERE user_id = %s",(nft['ownerID'],))[0]
        self.query("UPDATE nftinfo SET ownerID = %s WHERE id = %s",(userID,nftID))
        self.query("UPDATE nftusers SET token = %s WHERE user_id = %s",(str(float(user['token'])-float(nft['token'])),userID,))
        self.query("UPDATE nftusers SET token = %s WHERE user_id = %s",(str(float(user['token'])+float(nft['token'])),seller['user_id'],))
        # insert a record
        self.insertRows(table='nftrecord',columns=['nftTimeStamp','buyer','seller','currentOwner','cost','imageID'],parameters=[datetime.now().strftime("%H:%M:%S"),user['email'],seller['email'],user['email'],nft['token'],str(nft['id'])])
        return {
            "success": 1,
            "message": "NFT bought successfully"
        }
    def updateNFT(self,id,description,token):
        self.query("UPDATE nftinfo SET description = %s, token = %s WHERE id = %s",(description,token,id))

    def getAllRecords(self):
        return self.query("SELECT * FROM nftrecord")
#####################
# test
####################
            
    def nft_getAllUsers(self):
        return self.query("SELECT * FROM nftusers")
    def nft_getAllNFTs(self):
        return self.query("SELECT * FROM nftinfo")