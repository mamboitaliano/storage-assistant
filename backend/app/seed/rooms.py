from faker import Faker
from app.models import Room

fake = Faker()

def seed_rooms(db, floors) -> list[Room]:
    rooms: list[Room] = []

    for floor in floors:
        for _ in range(2):
            rooms.append(
                Room(
                    name=f"{fake.word().title()} Room",
                    floor_id=floor.id,
                )
            )

    db.add_all(rooms)
    db.flush() # again, get the ids
    return rooms