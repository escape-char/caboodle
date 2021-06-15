from backend.endpoints.auth import router as auth_router
from backend.endpoints.mybookmarks import router as my_bookmarks_router

routers = [
    auth_router,
    my_bookmarks_router
]
