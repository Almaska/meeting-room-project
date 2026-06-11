import pytest
from datetime import time
from app.api.rooms import calculate_free_slots


def test_calculate_free_slots_empty():
    bookings = []
    free = calculate_free_slots(bookings)
    assert free == [(time(9, 0), time(18, 0))]


def test_calculate_free_slots_with_booking_in_middle():
    bookings = [
        {'start_time': time(12, 0), 'end_time': time(14, 0)}
    ]
    free = calculate_free_slots(bookings)
    assert (time(9, 0), time(12, 0)) in free
    assert (time(14, 0), time(18, 0)) in free
    assert len(free) == 2


def test_calculate_free_slots_with_booking_at_start():
    bookings = [
        {'start_time': time(9, 0), 'end_time': time(11, 0)}
    ]
    free = calculate_free_slots(bookings)
    assert (time(9, 0), time(11, 0)) not in free
    assert (time(11, 0), time(18, 0)) in free
    assert len(free) == 1


def test_calculate_free_slots_full_day():
    bookings = [
        {'start_time': time(9, 0), 'end_time': time(12, 0)},
        {'start_time': time(12, 0), 'end_time': time(15, 0)},
        {'start_time': time(15, 0), 'end_time': time(18, 0)},
    ]
    free = calculate_free_slots(bookings)
    assert free == []