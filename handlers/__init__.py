from .commands import router as commands_router
from .voice import router as voice_router

routers = [
    commands_router,
    voice_router
]