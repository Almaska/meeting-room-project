from fastapi import FastAPI

from app.api import rooms
from app.db.session import engine
from app.db.base import Base
from app.routers import auth, booking
from app.models.room import Room
from app.models.user import User
from app.models.booking import Booking


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(rooms.router, prefix="/rooms")
app.include_router(auth.router, prefix="/auth")
app.include_router(booking.router, prefix="/bookings")


@app.get("/")
def root ():
    return {"message": "API работает"}

