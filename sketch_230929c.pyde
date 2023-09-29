import csv
from process import normalize
from enviroment import DataRow, Vehicle

PATH = "./data.csv"
global DATA
global buffer
buffer = []
DATA = iter([])


def initDataset():
    global DATA
    with open(PATH, "r") as f:
        csv_reader = csv.reader(f,delimiter=',')
        next(csv_reader)
        
        DATA = iter([list(map(float, row))[1:] for row in csv_reader])
    pass

def getNextRow():
   return next(DATA)
    
    


def setup():
    initDataset()
    size(1280,720)
    pass
    
    
def draw():
    row = getNextRow()
    if not row:
        exit()
    normalized = normalize(row)
    dataRow = DataRow(normalized)
    objects = dataRow.get_objects()
    for i,o in enumerate(objects):
        if (o.x == 0 or o.y == 0) and len(buffer) > 0:
            
            objects[i].x = buffer[-1][i].x + buffer[-1][i].speed_x;
            objects[i].y = buffer[-1][i].y + buffer[-1][i].speed_y;
            
    buffer.append(objects)
    car = Vehicle(normalized[8], normalized[-2])
    print(objects)
    
    
    # transform
    translate(width/2, height/2)
    scale(1.5)

    
    # drawing
    
    background(30,35,42,130)
    
   

    
    # Make the car
    fill(61, 89, 4)
    rect(-20,-20,40,40)
    
    textSize(15);
    fill(255,255,255,100)
    text('Kocsika', -20,0)

    # car tolerance zone
    
    fill(45, 224, 87,30)
    ellipse(0,0,car.t, car.t)
    
    
    colors = [(0,0,255),(255,0,0),(0,255,255),(0,255,0)]
    for i,o in enumerate(objects):
        c = colors[i]
        c = [c[0],c[1],c[2], 100]
        fill(*c)
        stroke(255,0,0,100)
        #line(0,0,o.x, o.y)
        noStroke()
        ellipse(o.x, o.y, 20,20)
    
    
    delay(20)
    pass
