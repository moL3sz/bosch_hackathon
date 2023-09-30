import csv
from process import normalize
from enviroment import DataRow, Vehicle

global DATA
global buffer
global TIME



buffer = []
DATA = iter([])

# Time when the simulation will start
TIME =55

# init the dataset
def initDataset():
    global DATA
    global TIME
    
    PATH = "./data.csv"


    with open(PATH, "r") as f:
        csv_reader = csv.reader(f,delimiter=',')
        next(csv_reader)
        DATA = iter(filter(lambda x: x[-1] > TIME, [list(map(float, row))[1:] for row in csv_reader]))
    pass

def getNextRow():
   return next(DATA)
    


    
# Matrix multiplication
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




# Generate the future path from the current time based on the current vehicle information
def generate_possible_future(car, iteration=20):
    points = []
    pos_b = iteration/3 # lépte szabályzó
    pos, rotation = 0,0
    prev = 1
    W_tolerance = 400 # a future path, Width of the area
     
    
    for t in range(1,iteration):
        
        R_M = [[cos(rotation), -sin(rotation)],
                [sin(rotation), cos(rotation)]]


        P_M_t= [[pos], [W_tolerance]]
        P_M_c = [[pos], [0]]
        P_M_b = [[pos], [-W_tolerance]]

        pos += car.speed / pos_b
        rotation += car.yawRate / pos_b


    
        newPOS_t = list(MM(R_M, P_M_t))
        newPOS_c = list(MM(R_M, P_M_c))
        newPOS_b = list(MM(R_M, P_M_b))


        points.append(newPOS_t)
        # points.append(newPOS_c)
        points.append(newPOS_b)
    return points
    
# Calculate the brake radius
def brake_radius(car):
    t = 1
    return (0.278 * t * (car.speed / 256)*3.6) + ((car.speed / 256)*3.6)*2 / (254 * (0.7 + 0))


def setup():
    initDataset()
    size(1920,1080)
    pass
    
    
global PAUSED
global prev_speed
global g_potential

PAUSED = False
prev_speed = 0
g_potential = False


def draw():
    global prev_speed
    global g_potential
   
    row = getNextRow()
    if not row:
        exit()
    normalized = normalize(row)
    dataRow = DataRow(normalized)
    # get all objects from
    objects = dataRow.get_objects()
    for i,o in enumerate(objects):
        if (o.x == 0 or o.y == 0) and len(buffer) > 0:
            
            objects[i].x = buffer[-1][i].x + buffer[-1][i].speed_x;
            objects[i].y = buffer[-1][i].y + buffer[-1][i].speed_y;
            
    buffer.append(objects)
    car = Vehicle(normalized[8] if not g_potential else prev_speed, normalized[-2])
    future_path = generate_possible_future(car,50)
    
    
    # translate the scene
    translate(300, height/2)
    scale(0.1)

    # drawing     
    background(30,35,42,130)
    # Make the car
    # Future path visulazation
    for x,y in future_path:
        fill(255,0,0)
        ellipse(x[0],y[0],50,50)
    
    
    push()
    rotate(car.yawRate)
    
    br = brake_radius(car)*512 
    brake_tolerance = 0.3
    br_t = br*(1+brake_tolerance) # toleranciált féktáv
    
    # Create the tolerance visualization
    fill(238, 255, 0,10)
    ellipse(0,0,br_t,br_t)
    fill(0,255,0,10)
    ellipse(0,0,br,br)
    
    # car rect
    noStroke()        
    fill(61, 89, 4)
    scale(4)
    rect(-100,-50,160,80)
    
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
    
    # define colors for each objects
    colors = [(0,0,255),(255,0,0),(0,255,255),(0,255,0)]
    
    
    for i,o in enumerate(objects):
        global potential
        c = colors[i]
        c = [c[0],c[1],c[2], 255]
        
        stroke(255,255,0,10) 
        push()
        avg_d = 0
        potential = False
        # pair the future path points together(top and bottom)
        for p1,p2 in zip(future_path[0::2], future_path[1::2]):
            
            p1x,p1y  = p1[0][0], p1[1][0]
            p2x,p2y  = p2[0][0], p2[1][0]
            
            # Calculate if any 2 boundary points (bottom and top) distance from the objects is less than a threshold, means, the objects is on the path of the vehicle
            d1 = sqrt((p1x-o.x)**2 + (p1y-o.y)**2)
            d2 = sqrt((p2x-o.x)**2 + (p2y-o.y)**2)
            d_car = sqrt(o.x**2 + o.y**2)
            # if so, and the object in the breaking zone then make it potential target
            if (d1+d2)/2 < 600 and d_car < br_t:
                potential = True
                stroke(255,0,0,10)

            # Debug lines
            line(o.x, o.y, p1x,p1y)
            line(o.x, o.y, p2x,p2y)

        pop()
        noStroke()
        fill(*c)
        strokeWeight(10)
        
        
        # line(0,0,o.x, o.y)
        textSize(200)
        text("Dist: " + str(round(sqrt((o.x / 128 )**2 + (o.y / 128)**2),3)) + "m", o.x, o.y)
        text("Speed: " + str(round(sqrt((o.speed_x / 256 )**2 + (o.speed_y / 256)**2),3)) + "m/s", o.x, o.y-150)

        
        # Check if any objects is potetntal then make the car brake
        if potential:
            fill(255,0,0)
            g_potential = potential
            prev_speed = max(0,car.speed * 0.91 )
            text("POTENTIAL TARGET", o.x, o.y-350)
        
    
        ellipse(o.x, o.y, 100,100)
        
    
    delay(20)

    
def keyPressed(e):
    global PAUSED
    print(PAUSED)
    if(e.getKeyCode() == 32):
        
        PAUSED = False if PAUSED else True
        if PAUSED:
            noLoop()
        else:
            loop()
