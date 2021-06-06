from typing import Any, List

from fastapi import APIRouter, HTTPException

from app import schemas

router = APIRouter()


def get_item(id: int, db: List[schemas.Item]):
    for item in db:
        if item.id == id:
            return item
    return None


item_db = [
    schemas.Item(**{
        'id': 1,
        'title': 'Title1',
        'description': 'Description1',
        'owner_id': 1
    })
]


@router.get("/", response_model=List[schemas.Item])
def read_items(
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve Items.

    - **skip**:  skips the number of domains returned in response.
    - **limit**: This parameter limits the number of domains returned in response.
    \f
    :param skip
    :param limit
    """
    return item_db[skip:skip + limit]


@router.post("/", response_model=schemas.Item)
def create_item(
        *,
        item_in: schemas.ItemCreate,
) -> Any:
    """
    Create a new Item.

    - **title**: Item Title
    - **description**: Item Description
    \f
    :param item_in User input

    """
    item = schemas.Item(**{
        'id': len(item_db) + 1,
        'title': item_in.title,
        'description': item_in.description,
        'owner_id': 1
    })
    item_db.append(item)
    return item


@router.put("/{id}", response_model=schemas.Item)
def update_item(
        *,
        id: int,
        item_in: schemas.ItemUpdate,
) -> Any:
    """
     Update an Item

     - **id**            : Item ID
     - **title**         : Item Title
     - **description**   : Item Description

     \f
     :param id item id
     :param item_in User input

     """
    item = get_item(id=id, db=item_db)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.title = item_in.title
    item.description = item_in.description
    return item


@router.get("/{id}", response_model=schemas.Item)
def read_item(
        *,
        id: int,
) -> Any:
    """
    Get Item by id.

    - **id** : Item ID
    \f
    :param id: Item ID

    """
    item = get_item(id=id, db=item_db)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{id}", response_model=schemas.Item)
def delete_item(
        *,
        id: int,
) -> Any:
    """
    Delete an item.
    """
    item = get_item(id=id, db=item_db)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item_db.remove(item)
    return item
