'''
Created on Dec 12, 2020

@author: Harvey.Imama
'''


import pandas as pd
import cherrypy
from services  import testService
from persistence  import conn
from messenger  import sms
from messenger  import email
import logging
import threading


class MyWebService(object):
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def process(self):
        data = cherrypy.request.json
        df = pd.DataFrame(data)
        outcome = testService.Tester().predictOutcome(df) 
        if outcome == True:
            x = threading.Thread(target=self.__sendMessage__, args=(df,)) 
            x.start()
        df = self. __saveOutcome_(df,outcome)
    
        return df.to_json()
            
    def __saveOutcome_(self,data,outcome):
        data.isflagged = outcome
        conn.Connect().save(self.TRANSACTION,data)
        return data
        
    def __sendMessage__(self,data):
        email.emailMessenger().send(data)
        sms.SMSMessenger().send(data)

  