from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, time as datetime_time

from app.db.session import get_db
from app.models.booking import Booking
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.models.room import Room
from app.schemas.booking import BookingCreate

router = APIRouter()


def parse_time(time_str: str) -> datetime_time:
    parts = time_str.split(':')
    return datetime_time(int(parts[0]), int(parts[1]), int(parts[2]) if len(parts) > 2 else 0)


@router.post('')
def create_booking(
    data: BookingCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    room = db.query(Room).filter(Room.id == data.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    start_time = data.start_time if isinstance(data.start_time, datetime_time) else parse_time(str(data.start_time))
    end_time = data.end_time if isinstance(data.end_time, datetime_time) else parse_time(str(data.end_time))

    if start_time >= end_time:
        raise HTTPException(status_code=400, detail="Некорректное время бронирования")

    existing = db.query(Booking).filter(
        Booking.room_id == data.room_id,
        Booking.date == data.date,
        Booking.start_time < end_time,
        Booking.end_time > start_time
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Это время уже забронировано")

    booking = Booking(
        user_id=user.id,
        room_id=data.room_id,
        date=data.date,
        start_time=start_time,
        end_time=end_time
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking


@router.get('')
def get_bookings(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return db.query(Booking).filter(Booking.user_id == user.id).all()


@router.delete('/{booking_id}')
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")

    from datetime import date as today_date
    if booking.date < today_date.today() and user.role != "admin":
        raise HTTPException(status_code=400, detail="Нельзя удалить прошедшее бронирование")

    if booking.user_id != user.id and user.role != "admin":
        raise HTTPException(status_code=403, detail="Нет прав на удаление этого бронирования")

    db.delete(booking)
    db.commit()
    return {"message": "Бронирование удалено"}