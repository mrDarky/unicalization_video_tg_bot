from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uvicorn
import os

from config import settings
from database.database import init_db, get_session
from database.models import User, Video, Deposit, Withdrawal, Setting
from api.routes import users, videos, deposits, withdrawals, settings as settings_route, statistics


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup: Initialize database
    await init_db()
    yield
    # Shutdown: Add cleanup code here if needed


# Create FastAPI app
app = FastAPI(title="Video Bot Admin Panel", version="1.0.0", lifespan=lifespan)

# Mount static files only if the directory exists
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="api/templates")

# Include API routes
app.include_router(users.router, prefix="/api")
app.include_router(videos.router, prefix="/api")
app.include_router(deposits.router, prefix="/api")
app.include_router(withdrawals.router, prefix="/api")
app.include_router(settings_route.router, prefix="/api")
app.include_router(statistics.router, prefix="/api")


@app.get("/", response_class=RedirectResponse)
async def root():
    """Redirect to admin dashboard"""
    return RedirectResponse(url="/admin")


@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, session: AsyncSession = Depends(get_session)):
    """Admin dashboard page"""
    # Get statistics
    from api.routes.statistics import get_statistics
    stats = await get_statistics(session)
    
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "active_page": "dashboard",
            "stats": stats
        }
    )


@app.get("/admin/users", response_class=HTMLResponse)
async def admin_users(request: Request, session: AsyncSession = Depends(get_session)):
    """Users management page"""
    result = await session.execute(select(User).limit(100))
    users_list = result.scalars().all()
    
    return templates.TemplateResponse(
        "users.html",
        {
            "request": request,
            "active_page": "users",
            "users": users_list
        }
    )


@app.get("/admin/videos", response_class=HTMLResponse)
async def admin_videos(request: Request, session: AsyncSession = Depends(get_session)):
    """Videos management page"""
    result = await session.execute(select(Video).limit(100))
    videos_list = result.scalars().all()
    
    return templates.TemplateResponse(
        "videos.html",
        {
            "request": request,
            "active_page": "videos",
            "videos": videos_list
        }
    )


@app.get("/admin/deposits", response_class=HTMLResponse)
async def admin_deposits(request: Request, session: AsyncSession = Depends(get_session)):
    """Deposits management page"""
    result = await session.execute(select(Deposit).limit(100))
    deposits_list = result.scalars().all()
    
    return templates.TemplateResponse(
        "deposits.html",
        {
            "request": request,
            "active_page": "deposits",
            "deposits": deposits_list
        }
    )


@app.get("/admin/withdrawals", response_class=HTMLResponse)
async def admin_withdrawals(request: Request, session: AsyncSession = Depends(get_session)):
    """Withdrawals management page"""
    result = await session.execute(select(Withdrawal).limit(100))
    withdrawals_list = result.scalars().all()
    
    return templates.TemplateResponse(
        "withdrawals.html",
        {
            "request": request,
            "active_page": "withdrawals",
            "withdrawals": withdrawals_list
        }
    )


@app.get("/admin/settings", response_class=HTMLResponse)
async def admin_settings(request: Request, session: AsyncSession = Depends(get_session)):
    """Settings management page"""
    result = await session.execute(select(Setting))
    settings_list = result.scalars().all()
    
    return templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "active_page": "settings",
            "settings": settings_list
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "api_main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )
