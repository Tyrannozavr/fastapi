from fastapi import APIRouter

router = APIRouter()

app.include_router(user.router)
app.include_router(test.router)
app.include_router(restrictions.router)
app.include_router(files.router)
app.include_router(dependencies.router)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(doc_example.database_router, prefix="/database", tags=["auth"])