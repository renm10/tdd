from flask import Flask
from src import status

app = Flask(__name__)

COUNTERS = {}

# We will use the app decorator and create a route called slash counters.
# specify the variable in route <name>
# let Flask know that the only methods that is allowed to called
# on this function is "POST".
@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a counter"""
    app.logger.info(f"Request to create counter: {name}")
    global COUNTERS
    if name in COUNTERS:
        return {"Message":f"Counter {name} already exists"}, status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return {name: COUNTERS[name]}, status.HTTP_201_CREATED

@app.route('/counters/<name>', methods=['PUT']) #Creates the route with method PUT
def update_counter(name): #Function to implement route
    """Updates the counter"""
    app.logger.info(f"Request to update the given counter: {name}")
    global COUNTERS
    
    if name in COUNTERS:
        COUNTERS[name] += 1 #Increment counter by 1
        return {name: COUNTERS[name]}, status.HTTP_200_OK  #Return new counter and 200_OK return code
    
@app.route('/counters/<name>', methods=['GET']) #Creates the route with method GET
def read_counter(name): #Function to implement route
    """Read value from the counter"""
    app.logger.info(f"Request to read value from the given counter: {name}")
    
    if name in COUNTERS:
        return str(COUNTERS[name]), status.HTTP_200_OK  #Return new counter and 200_OK return code
    
