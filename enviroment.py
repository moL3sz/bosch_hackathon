import random


class Enviroment:
    def __init__(self,data):
        self.data = data
        pass
    
    
    def __repr__(self):
        return "Enviroment"
    
class DataRow:
    def __init__(self, rowData):
        self.rowData = rowData
        self.FirstObjectDistance_X = rowData[0]
        self.FirstObjectDistance_Y = rowData[1]
        self.SecondObjectDistance_X = rowData[2]
        self.SecondObjectDistance_Y = rowData[3]
        self.ThirdObjectDistance_X = rowData[4]
        self.ThirdObjectDistance_Y = rowData[5]
        self.FourthObjectDistance_X = rowData[6]
        self.FourthObjectDistance_Y = rowData[7]
        self.VehicleSpeed = rowData[8]
        self.FirstObjectSpeed_X = rowData[9]
        self.FirstObjectSpeed_Y = rowData[10]
        self.SecondObjectSpeed_X = rowData[11]
        self.SecondObjectSpeed_Y = rowData[12]
        self.ThirdObjectSpeed_X = rowData[13]
        self.ThirdObjectSpeed_Y = rowData[14]
        self.FourthObjectSpeed_X = rowData[15]
        self.FourthObjectSpeed_Y = rowData[16]
        self.YawRate = rowData[17]
        self.Timestamp = rowData[18]
        
    def get_objects(self):
        dists = self.rowData[:8]
        speeds = self.rowData[9:-2]
        objects = []
        for i in range(0,7,2):
            x,y = dists[i],dists[i+1]
            speed_x,speed_y = speeds[i],speeds[i+1]
            objects.append(Object(x,y,speed_x,speed_y))
        return objects
        
    
class Object:
    def __init__(self, x,y,speed_x, speed_y):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    
    def potential(self):
        self.color = (255,0,0)
    def __repr__(self):
        return '(x: {0}, y: {1}, speed_x: {2}, speed_y: {3})'.format(self.x, self.y, self.speed_x, self.speed_y)
        
class Vehicle:
    def __init__(self, speed, yawRate):
        self.speed = speed
        self.yawRate = yawRate
        self.w = 80
        self.h = 80
        self.t = 160 # tolerancia
   
        
