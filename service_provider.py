def login(username: str, password: str):
    # This is a dummy function, so it doesn't actually perform any authentication.
    # Instead, it just returns a static dictionary.
    return {
        "bearer": "dummy_bearer_token",
        "cookie": "dummy_cookie_token"
    }


def book_zone(auth_token: str, cookie_token, date: str):
    # This is a dummy function, so it doesn't actually perform any booking.
    # Instead, it just returns a static message.
    return "Booking successful"
