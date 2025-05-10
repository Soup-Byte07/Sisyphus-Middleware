from fastapi import APIRouter

router = APIRouter(prefix="/frontend", tags=["frontend"])

@router.get("/frontpage")
def get_all_page_data(): 
    return {
        "title": "Sisyphus Front Page",
        "page": "Front Page",
        "content": [
            {"type": "text", "content": "Welcome to the Sisyphus Middleware!"},
            {"type": "image", "content": "/static/images/sisyphus.png"},
            {"type": "text", "content": "This is a simple front page."},
        ],
    }
