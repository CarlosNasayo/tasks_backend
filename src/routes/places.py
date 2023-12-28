from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from mongoengine import Document, StringField, ListField,BooleanField
from typing import List

router = APIRouter()
class PlaceInput(BaseModel):
    name: str
    description: str 
class PlaceOutput(BaseModel):
    id:str
    name: str
    description: str
    completed: bool
class Place(Document):
    name = StringField(required=True)
    description = StringField(required=True)
    completed=BooleanField(required=True)


@router.get("/get_place", summary="Get all places", response_model=List[PlaceOutput])
async def get_places():
    try:
        places_to_return = Place.objects()
        result = [{'id': str(place.id), 'name': place.name, 'description': place.description, 'completed': place.completed} for place in places_to_return]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting places: {str(e)}")
@router.post("/create_places", summary="Create a new place", response_model=PlaceOutput)
async def create_place(place_input: PlaceInput):
    existing_place = Place.objects(name=place_input.name).first()
    if existing_place:
        raise HTTPException(status_code=400, detail="place already exists")

    try:
        new_place = Place(
            name=place_input.name,
            description=place_input.description,
            completed=False
        )
        new_place.save()

        return PlaceOutput(
            id=str(new_place.id),
            name=new_place.name,
            description=new_place.description,
            completed=new_place.completed
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create place: {str(e)}")


@router.put("/{place_id}", summary="Update a Place")
async def update_place(place_id: str, place_input: PlaceInput):
    try:
        place_to_update=Place.objects(id=str(place_id)).first()
        place_to_update.update(name=place_input.name,description=place_input.description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update a place: {str(e)}")

    
    return {'message': f'Place with ID {place_to_update.id} sucesfully updated'}



@router.delete("/{place_id}", summary="Delete a Place")
async def delete_place(place_id: str):
    try:

        place_to_delete=Place.objects(id=place_id).first()
        if place_to_delete:
            place_to_delete.delete()
        else:
            return  HTTPException(status_code=500, detail=f"the place doesn't exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete  place: {str(e)}")
    return {'message': f'Place with ID {place_to_delete.id} sucesfully deleted'}




@router.patch("/{place_id}", summary="Partial update of a place")
async def partial_update_place(place_id: str,status:bool):
    place_patch= Place.objects(id=place_id).first()
    if place_patch:
        place_patch.update(completed=status)
    else:
          raise HTTPException(status_code=404, detail=f"the place with  ID {place_id} doesn't exists")
    return {'message': f'Place with ID {place_patch.id} sucesfully updatedd', 'the current status is': status}
