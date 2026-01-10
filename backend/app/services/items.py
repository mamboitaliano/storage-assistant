from sqlalchemy.orm import Session

from ..models import Item
from ..schemas.items import ItemUpdate, ItemResponse


def get_items(db: Session) -> list[Item]:
    items = db.query(Item).all()
    return items

def update_item(db: Session, item_id: int, data: ItemUpdate) -> ItemResponse | None:
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return None

    if data.name is not None:
        item.name = data.name
    if data.room_id is not None:
        item.room_id = data.room_id
    if data.container_id is not None:
        item.container_id = data.container_id
    if data.quantity is not None:
        item.quantity = data.quantity

    db.commit()
    db.refresh(item)

    return ItemResponse(
        id=item.id,
        name=item.name,
        room_id=item.room_id,
        container_id=item.container_id,
        quantity=item.quantity,
        created_at=item.created_at,
    )


def delete_item(db: Session, item_id: int, quantity: int | None = None) -> dict | None:
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return None

    if quantity and quantity < item.quantity:
        item.quantity -= quantity
        db.commit()
        return {"message": "Item quantity reduced", "id": item.id, "quantity": item.quantity}

    db.delete(item)
    db.commit()
    return {"message": "Item deleted", "id": item.id}
