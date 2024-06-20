from pathlib import Path

from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from service_provider import login as provider_login, book_zone as provider_book_zone
from auth import get_user_tokens, generate_token, get_token
from fastapi.param_functions import Form
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'static/templates')))

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    tokens = provider_login(username=form_data.username, password=form_data.password)
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Replace generate_token with your actual function to generate a token
    token = generate_token(tokens, username=form_data.username)
    response = RedirectResponse(url='/bookings', status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie("token", token, httponly=True)
    return response


@router.get("/bookings")
def booking_page(request: Request, token: str = Depends(get_token)):
    response = templates.TemplateResponse("booking.html", {"request": request})
    response.set_cookie("token", token, httponly=True)
    return response


class BookingForm:
    def __init__(self, date: str):
        self.date = datetime.fromisoformat(date)


@router.post("/booking")
def make_booking(date: str = Form(...), token: str = Depends(get_token)):
    form = BookingForm(date)

    try:
        tokens = get_user_tokens(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

    try:
        provider_book_zone(
            auth_token=tokens["bearer"],
            cookie_token=tokens["cookie"],
            date=form.date.isoformat()
        )
        return {"message": "Booking successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/",)
def home():
    return RedirectResponse(url='/login', status_code=status.HTTP_303_SEE_OTHER)
