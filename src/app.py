from fastapi import FastAPI
from routes import tasks
from routes import places
from mongoengine import connect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Conexión a la base de datos MongoDB
db_user = "carlosnasayov"
db_password = "OeiVjkgUG797tdLH"
db_name = "databd"  
cluster_url = "cluster0.uwrow0q.mongodb.net"
connect(db=db_name, host=f"mongodb+srv://{db_user}:{db_password}@{cluster_url}/datadb?retryWrites=true&w=majority")
print("Conexión exitosa")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(places.router, prefix="/api/places", tags=["places"])
