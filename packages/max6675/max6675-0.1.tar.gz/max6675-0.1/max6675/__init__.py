# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 09:53:54 2021

@author: franc
"""


import pyfirmata2 as pyfirmata
import time




#%% Fonctions nécessaires pour la lecture du thermocouple



class thermocouple:


    def __init__(self,board,miso,cs,sclk):

        self.board = board

        self.miso = self.board.get_pin("d:{}:i".format(miso))
        self.cs   = self.board.get_pin("d:{}:o".format(cs))
        self.sclk = self.board.get_pin("d:{}:o".format(sclk))
        
        time.sleep(1)
        cs.write(1)
        time.sleep(1)


    def read(self):

        self.cs.write(0)
        time.sleep(50/1000)
        
        bit_array = ""
        for i in range(16):
            self.sclk.write(0)
            time.sleep(50/1000)
            
            bit_array = bit_array + str( self.miso.read()*1 )
            
            self.sclk.write(1)
            time.sleep(50/1000)
        
        self.cs.write(1)
        time.sleep(50/1000)
        
        return int(bit_array[1:-3],2)/4


