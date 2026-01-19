from faker import Faker
from app.models import Container

fake = Faker()

def seed_containers(db, rooms) -> list[Container]:
    containers: list[Container] = []
    for room in rooms:
        for _ in range(fake.random_int(min=30, max=100)):
            containers.append(
                Container(
                    name=f"{fake.word().title()} Bin",
                    room_id=room.id,
                )
            )

    db.add_all(containers)
    db.flush()
    return containers
