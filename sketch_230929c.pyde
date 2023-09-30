import csv
from process import normalize
from enviroment import DataRow, Vehicle

PATH = "./data.csv"
global DATA
global buffer
buffer = []
DATA = iter([])
global TIME
TIME =55
def initDataset():
    global DATA
    global TIME
    with open(PATH, "r") as f:
        csv_reader = csv.reader(f,delimiter=',')
        next(csv_reader)
        
        DATA = iter(filter(lambda x: x[-1] > TIME, [list(map(float, row))[1:] for row in csv_reader]))
    pass

def getNextRow():
   return next(DATA)
    
def yawF(x):
    return 3*(1-x)**2*x * 0.04 + 3*(1-x)*x**2*0.57 + x**3*0.95


    
    
def MM(A,B):    
    if len(A[0]) == len(B):
        result = [] 
        for i in range(0,len(A)): 
            temp = []
            for j in range(0,len(B[0])): 
                total = 0 
                l = 0 
                for k in range(0,len(A[0])):
                    total += A[i][k]*B[l][j]
                    l = l+1
                temp.append(total)
            result.append(temp)                
        return result
    else:
        return

def generate_possible_future(car, iteration=20):
    points = []
    pos_b = 5 # lépte szabályzó
    pos, rotation = 0,0
    prev = 1
    for k in range(iteration):
        R_M = [[cos(rotation), -sin(rotation)],
                [sin(rotation), cos(rotation)]]

        P_M = [[pos], [0]]
        pos += car.speed / pos_b
        rotation += car.yawRate
        rotation = sqrt(1 + (rotation*4*k)/60) - 1
        
        
        t_r = 20
        b_r = 20
        
        t_px = t_r * cos(rotation)
        t_py = t_r * sin(rotation)
        
        newPOS = list(MM(R_M, P_M))
        newPOS.append(rotation)

        points.append(newPOS)
    return points
    

def brake_radius(car):
    t = 1
    return (0.278 * t * (car.speed / 256)*3.6) + ((car.speed / 256)*3.6)*2 / (254 * (0.7 + 0))


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
            objects[i ].y = buffer[-1][i].y + buffer[-1][i].speed_y;
    buffer.append(objects)
    car = Vehicle(normalized[8], normalized[-2])
    future_path = generate_possible_future(car)
    
    

    
    
    # transform
    translate(300, height/2)
    scale(0.1)


    
    # drawing 
    
    background(30,35,42,130)
   
    
    if True:
        
    
        
        # Make the car
        push()
        rotate(car.yawRate)
        
        br = brake_radius(car)*256
        ellipse(0,0,br,br)

        line(0,0,car.speed, 0)
        for x,y,r in future_path:
            push()
            fill(255,0,0)
            translate(x[0],y[0])
            rotate(r)
            stroke(255)
            line(0,-100,0,100)
            ellipse(x[0],y[0],100,100)
            pop()
        fill(61, 89, 4)
        scale(4)
        rect(-100,-50,160,80)
        
        
        #line(-100,-200, 100,-200)
        #line(-100,200, 100,200)
        
        pop()
        textSize(15);
        fill(255,255,255,100)
        text('Kocsika', -20,0)
        textSize(300)
        text("Speed: " + str(car.speed / 256) + "m/s",200, -2000)
        text("Time: " + str(normalized[-1]), 200, -2600)
        text("Yaw: " + str(car.yawRate * 360 / PI),200, -2300)
        
    
    
        # car tolerance zone
        
        fill(45, 224, 87,30)
        ellipse(0,0,car.t, car.t)
        
        
        colors = [(0,0,255),(255,0,0),(0,255,255),(0,255,0)]
        for i,o in enumerate(objects):
            c = colors[i]
            c = [c[0],c[1],c[2], 100]
            fill(*c)
            strokeWeight(10)

            stroke(255,0,0)
            
            
            # line(0,0,o.x, o.y)
            textSize(200)
            text("Dist: " + str(round(sqrt((o.x / 128 )**2 + (o.y / 128)**2),3)) + "m", o.x, o.y)
            
    
            
            # line(o.x, o.y, o.x + o.speed_x, o.y + o.speed_y)
    
            noStroke()
            ellipse(o.x, o.y, 100,100)
            
            stroke(255,255,0) 
            if i == 0:
                stroke(255,0,0)
                push()
                translate(o.x,o.y)
                scale(4)

                rotate(PI/2 - car.yawRate)
                #line(-100,-200, 100,-200)
                #line(-100,200, 100,200)
                pop()
           
          
    
    
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
