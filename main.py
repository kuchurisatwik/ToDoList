from fastapi import FastAPI
import routers.tasks as tasks,routers.users as users,routers.auth as auth



app  = FastAPI()

app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(auth.router)