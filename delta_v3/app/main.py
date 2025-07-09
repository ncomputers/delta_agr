from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from passlib.context import CryptContext

from .database import create_user, get_user, save_api_keys, save_trade_rule, redis_client

app = FastAPI(title="Algo Trading Platform")
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/signup", response_class=HTMLResponse)
async def signup(username: str = Form(...), password: str = Form(...)):
    hashed = pwd_context.hash(password)
    user_id = create_user(username, hashed)
    if user_id is None:
        raise HTTPException(status_code=400, detail="Username already exists")
    return RedirectResponse(url=f"/dashboard?user_id={user_id}", status_code=303)

@app.post("/login", response_class=HTMLResponse)
async def login(username: str = Form(...), password: str = Form(...)):
    user = get_user(username)
    if not user or not pwd_context.verify(password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return RedirectResponse(url=f"/dashboard?user_id={user['id']}", status_code=303)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user_id: int):
    return templates.TemplateResponse("dashboard.html", {"request": request, "user_id": user_id})

@app.post("/api-keys/{user_id}")
async def add_api_keys(user_id: int, api_key: str = Form(...), api_secret: str = Form(...)):
    save_api_keys(user_id, api_key, api_secret)
    return RedirectResponse(url=f"/dashboard?user_id={user_id}", status_code=303)

@app.post("/rules/{user_id}")
async def add_rule(
    user_id: int,
    loss_threshold: float = Form(...),
    quantity: float = Form(...),
    profit_target: float = Form(...),
):
    save_trade_rule(user_id, loss_threshold, quantity, profit_target)
    return RedirectResponse(url=f"/dashboard?user_id={user_id}", status_code=303)

@app.get("/price")
async def get_latest_price():
    return redis_client.hgetall("latest_price")
