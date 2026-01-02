from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uvicorn
import os

from config import settings
from database.database import init_db, get_session
from database.models import User, Video, Deposit, Withdrawal, Setting, TariffPlan
from api.routes import users, videos, deposits, withdrawals, settings as settings_route, statistics, tariff_plans
from api.auth import create_access_token, require_admin


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
app.include_router(tariff_plans.router, prefix="/api")


@app.get("/", response_class=RedirectResponse)
async def root():
    """Redirect to admin dashboard"""
    return RedirectResponse(url="/admin")


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, error: str = None):
    """Login page"""
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": error}
    )


@app.post("/login")
async def login(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...)
):
    """Login endpoint"""
    if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
        # Create access token
        token = create_access_token(data={"sub": username})
        
        # Set cookie and redirect
        redirect_response = RedirectResponse(url="/admin", status_code=302)
        redirect_response.set_cookie(
            key="admin_token",
            value=token,
            httponly=True,
            max_age=60 * 60 * 24,  # 24 hours
            samesite="lax"
        )
        return redirect_response
    else:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid username or password"}
        )


@app.get("/logout")
async def logout():
    """Logout endpoint"""
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("admin_token")
    return response
@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request, 
    session: AsyncSession = Depends(get_session),
    username: str = Depends(require_admin)
):
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
async def admin_users(
    request: Request, 
    session: AsyncSession = Depends(get_session),
    username: str = Depends(require_admin)
):
    """Users management page"""
    from sqlalchemy.orm import selectinload
    result = await session.execute(
        select(User).options(selectinload(User.tariff_plan)).limit(100)
    )
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
async def admin_videos(
    request: Request, 
    session: AsyncSession = Depends(get_session),
    username: str = Depends(require_admin)
):
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


@app.get("/admin/tariff-plans", response_class=HTMLResponse)
async def admin_tariff_plans(
    request: Request, 
    session: AsyncSession = Depends(get_session),
    username: str = Depends(require_admin)
):
    """Tariff plans management page"""
    result = await session.execute(select(TariffPlan).limit(100))
    tariff_plans_list = result.scalars().all()
    
    return templates.TemplateResponse(
        "tariff_plans.html",
        {
            "request": request,
            "active_page": "tariff_plans",
            "tariff_plans": tariff_plans_list
        }
    )


@app.get("/admin/deposits", response_class=HTMLResponse)
async def admin_deposits(
    request: Request, 
    session: AsyncSession = Depends(get_session),
    username: str = Depends(require_admin)
):
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
async def admin_withdrawals(
    request: Request, 
    session: AsyncSession = Depends(get_session),
    username: str = Depends(require_admin)
):
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
async def admin_settings(
    request: Request, 
    session: AsyncSession = Depends(get_session),
    username: str = Depends(require_admin)
):
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
