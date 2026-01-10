from faker import Faker
from app.models import Item

fake = Faker()

def seed_items(db, rooms, containers) -> list[Item]:
    items: list[Item] = []

    # items in actual containers
    for container in containers:
        for _ in range(fake.random_int(min=2, max=4)):
            items.append(
                Item(
                    name=fake.word().title(),
                    room_id=container.room_id,
                    container_id=container.id,
                    quantity=fake.random_int(min=1, max=10),
                )
            )
    
    # loose items in rooms
    for room in rooms:
        for _ in range(fake.random_int(min=1, max=8)):
            items.append(
                Item(
                    name=fake.word().title(),
                    room_id=room.id,
                    container_id=None,
                    quantity=fake.random_int(min=1, max=6),
                )
            )
    
    db.add_all(items)
    db.flush()
    return items