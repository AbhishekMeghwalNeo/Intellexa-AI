from fastapi import APIRouter

router = APIRouter()

@router.post("/upload")
def upload_document():
    return {
        "message": "Upload endpoint working"
    }
