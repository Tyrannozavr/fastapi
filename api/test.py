from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def main():
    return {"message": "Hello, world"}

@router.get("/second")
async def second():
    return "helloworld"