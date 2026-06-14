from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, time
from typing import List, Tuple

from app.db.session import get_db
from app.schemas.room import RoomCreate
from app.models.room import Room
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.models.booking import Booking


router = APIRouter()



from typing import List, Tuple, Union
from datetime import time

def calculate_free_slots(
    bookings: List[Union[dict, object]], 
    work_start: time = time(9, 0), 
    work_end: time = time(18, 0)
) -> List[Tuple[time, time]]:
    
    free = [(work_start, work_end)]
    
    for booking in bookings:
        if isinstance(booking, dict):
            start = booking['start_time']
            end = booking['end_time']
        else:
            start = booking.start_time
            end = booking.end_time
        
        new_free = []
        for free_start, free_end in free:
            if start >= free_end or end <= free_start:
                new_free.append((free_start, free_end))
            else:
                if start > free_start:
                    new_free.append((free_start, start))
                if end < free_end:
                    new_free.append((end, free_end))
        free = new_free
    
    return free


@router.get('/')
def get_room_availability(
    room_id: int,
    date: date,
    start_time: time,
    end_time: time,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    unavailable = db.query(Booking).filter(
        Booking.room_id == room_id,
        Booking.date == date,
        Booking.start_time < end_time,
        Booking.end_time > start_time
    ).first()

    return {"available": not unavailable}


@router.post('/')
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    new_room = Room(name=room.name)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


@router.delete('/{room_id}')
def delete_room(
    room_id: int, 
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    
    room_obj = db.query(Room).filter(Room.id == room_id).first()

    if not room_obj:
        raise HTTPException(status_code=404, detail="Комната не найдена")
    
    db.delete(room_obj)
    db.commit()
    return {"message": "Комната удалена"}


@router.get('/{room_id}/availability')
def get_availability(
    room_id: int,
    date: date,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    WORK_START = time(9, 0)
    WORK_END = time(18, 0)
    
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")
    
    bookings = db.query(Booking).filter(
        Booking.room_id == room_id,
        Booking.date == date
    ).order_by(Booking.start_time).all()
    
    free = calculate_free_slots(bookings, WORK_START, WORK_END)

    return [
        {"start": str(start), "end": str(end)}
        for start, end in free
    ]