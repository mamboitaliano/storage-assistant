from app.database import Base, SessionLocal, engine
from app.models import Floor, Room, Container, Item
from app.seed.floors import seed_floors
from app.seed.rooms import seed_rooms
from app.seed.containers import seed_containers
from app.seed.items import seed_items

def main():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # wipe it all
        db.query(Item).delete()
        db.query(Container).delete()
        db.query(Room).delete()
        db.query(Floor).delete()
        db.commit()

        floors = seed_floors(db)
        rooms = seed_rooms(db, floors)
        containers = seed_containers(db, rooms)
        seed_items(db, rooms, containers)

        db.commit()
        print("Seeding complete.")
    finally:
        db.close()

if __name__ == "__main__":
    main()