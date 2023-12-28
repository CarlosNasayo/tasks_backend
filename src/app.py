from fastapi import FastAPI
from routes import tasks
from routes import places
from mongoengine import connect
app = FastAPI()
db_user = "carlosnasayov"
db_password = "OeiVjkgUG797tdLH"
db_name = "databd"  
cluster_url = "cluster0.uwrow0q.mongodb.net"
connect(db=db_name, host=f"mongodb+srv://{db_user}:{db_password}@{cluster_url}/datadb?retryWrites=true&w=majority")
print("Conexión exitosa")
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(places.router, prefix="/api/places",tags=["places"])
