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
    size(1920,1080)
    pass
    
    
global PAUSED
PAUSED = False
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

    
    
    # transform
    translate(100, height/2)
    scale(0.1)

    
    # drawing
    
    background(30,35,42,130)
    
   

    
    # Make the car
    push()
    rotate(car.yawRate*-1)
    fill(61, 89, 4)
    scale(4)
    rect(-100,-50,160,80)
    
    pop()
    textSize(15);
    fill(255,255,255,100)
    text('Kocsika', -20,0)
    textSize(300)
    text("Speed: " + str(car.speed),200, -height/2 + 100)
    text("Yaw: " + str(car.yawRate * 360 / PI),200, -height/2 -200)


    # car tolerance zone
    
    fill(45, 224, 87,30)
    ellipse(0,0,car.t, car.t)
    
    
    colors = [(0,0,255),(255,0,0),(0,255,255),(0,255,0)]
    for i,o in enumerate(objects):
        c = colors[i]
        c = [c[0],c[1],c[2], 100]
        fill(*c)
        stroke(255,0,0)
        line(0,0,o.x, o.y)
        noStroke()
        ellipse(o.x, o.y, 100,100)
        
        stroke(255,255,0)
        line(objects[0].x,objects[0].y,objects[3].x, objects[3].y)
        line(objects[2].x,objects[2].y,objects[3].x, objects[3].y)
        for j,o_ in enumerate([objects[0], objects[2], objects[3]]):
            if i == 1:
                continue
            strokeWeight(10)
          
    
    
    delay(40)
    pass
    
def keyPressed(e):
    global PAUSED
    print(PAUSED)
    if(e.getKeyCode() == 32):
        
        PAUSED = False if PAUSED else True
        if PAUSED:
            noLoop()
        else:
            loop()
