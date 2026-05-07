from fastapi import APIRouter

router = APIRouter()

@router.post("/query")
def query_document():
    return {
        "message": "Query endpoint working"
    }