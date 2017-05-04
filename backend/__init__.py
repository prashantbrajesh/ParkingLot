__version__= '0.1'
from bottle import Bottle, TEMPLATE_PATH
app = Bottle()
TEMPLATE_PATH.append("./backend/views/")
TEMPLATE_PATH.remove("./views/")
from backend.routes import ConfigRoutes, ParkingRoutes, StaticRoutes
