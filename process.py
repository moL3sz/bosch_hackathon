
from enviroment import DataRow



def avg(l):
    return sum(l) / len(l)

def estimate_coef(x, y):
    
    n = len(x)
 
    # mean of x and y vector
    m_x = avg(x)
    m_y = avg(y)
 
    # calculating cross-deviation and deviation about x
    SS_xy = sum(y*x) - n*m_y*m_x
    SS_xx = sum(x*x) - n*m_x*m_x
 
    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1*m_x
 
    return (b_0, b_1)

def process(rawData):
    
    
    
    return [DataRow(row) for row in rawData]


def normalize(rawDataRow):
    
        
    return list(map(lambda x: x / 30, rawDataRow))



def filterObjects(data):
    pass
    


def calculate_zero_values(buffer, i):

    current_o = buffer[-1][i]
    x,y = current_o.x, current_o.y
    speed_x= current_o.speed_x
    speed_y= current_o.speed_y
        
    
