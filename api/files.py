import json
from enum import Enum
from typing import Annotated

from fastapi import HTTPException, Query, Depends

from fastapi import APIRouter
from fastapi import File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from api.exceptions import MyExcellentException

router =  APIRouter()

class Tags(Enum):
    errors: str = "errors"
    different: str = "different"
    dependency: str = "dependency"

@router.post("/files/")
async def create_file(file: bytes = File()):
    print(type(file))
    print(file)
    return {"file_size": len(file)}


class Params(BaseModel):
    name: str | None = None
    age: int | None = None
@router.get("/test", response_description="just to be sure jsonable works correct")
def helloworld(params: Annotated[Params, Query()]):
    jsonable_params = jsonable_encoder(params)
    json_params = json.dumps(jsonable_params)
    print(type(jsonable_params), jsonable_params)
    print(type(json_params), jsonable_params)
    return params

@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    content = await file.read()
    # content_two = file.file.read()
    if not content:
        raise HTTPException(status_code=400, detail="File is empty")
    return {"filename": file.filename}


@router.get("/fiels/form/", tags=[Tags.errors, Tags.different], deprecated=True)
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


@router.get("/error", tags=[Tags.errors], summary="markdown test",
            response_description="this is response description")
async def error(func_error: Annotated[str | None, Query(deprecated=True)] = None):
    """
    Just check if the markdown works correct:

    - **helloworld**: blablabla
    """
    if func_error == "my_error":
        raise MyExcellentException(name=func_error)
    raise HTTPException(status_code=404, detail="Item not found and you have requested the wrong page, body")


@router.put("/error/{item_id}", tags=[Tags.errors], summary="complete data update")
def update_handler(item_id: int):
    """This method is used to complete data update"""
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}

@router.patch("/error/{item_id}", tags=[Tags.errors], summary="partial data update")
def update_item(item_id: int):
    """This method is used to partial data update"""
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}


class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@router.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    """exclude_unset creates an instance of model without default values"""
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.model_dump(exclude_unset=True)
    updated_item = stored_item_model.model_copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item


def get_db():
    return "connection to db"

@router.get("/users/", tags=[Tags.dependency])
async def get_connection(db: Annotated[str, Depends(get_db)], one_more_db: Annotated[str, Depends(get_db)]):
    return db