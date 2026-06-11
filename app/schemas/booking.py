from pydantic import BaseModel
from datetime import date, time

class BookingCreate(BaseModel):
    room_id: int
    date: date
    start_time: time
    end_time: time
    