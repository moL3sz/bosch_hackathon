
from enviroment import DataRow




def process(rawData):
    
    return [DataRow(row) for row in rawData]

def normalize(rawDataRow):
    
        
    return list(map(lambda x: x , rawDataRow))



def filterObjects(data):
    pass
    


def calculate_zero_values(buffer, i):

    current_o = buffer[-1][i]
    x,y = current_o.x, current_o.y
    speed_x= current_o.speed_x
    speed_y= current_o.speed_y
        
    
