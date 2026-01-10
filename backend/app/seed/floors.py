from app.models import Floor

def seed_floors(db) -> list[Floor]:
    floors = [
        Floor(name="Basement", floor_number=-1),
        Floor(name="First Floor", floor_number=1),
        Floor(name="Second Floor", floor_number=2),
    ]

    db.add_all(floors)
    db.flush() #get IDs
    return floors