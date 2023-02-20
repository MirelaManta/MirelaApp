from website.models import User, Note


def test_login(client):
    """
    It tests the "/login" URL response to HTTP "GET" request

    """
    response = client.get("/login")
    assert b"<title>Login</title>" in response.data
    assert b"Email Address" in response.data
    assert b"Password" in response.data
    assert response.status_code == 200


def test_sign_up(client, app):
    """
    Given valid registration data, the success of the "POST" request creation is tested.
    More precisely, correct uploading of data on the sign-up page and the creation of a new account in the database.
    """

    user_data = {"email": "mirela@test.com", "firstName": "Mirela",
                 "password1": "passtest", "password2": "passtest"}
    response = client.post("/sign-up", data=user_data)
    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().first_name == "Mirela"
        assert User.query.first().email == "mirela@test.com"
        assert b"Welcome to Mirela's website!" in response.data
        assert b'<button type = "submit" class="btn btn-primary">Submit</button>' in response.data


def test_notes_page(client, app):
    """
    Given valid login details, the page should be redirected to home/secret notes.
    It also tests the correct addition of a note to the current user.
    """
    data_user = {"email": "mirela@test.com", "password": "passtest"}
    user_note = {"note": "This is a test"}
    client.post("/login", data=data_user)

    response = client.post("/", data=user_note)
    print(response.data)
    with app.app_context():
        assert b"Home" in response.data
        assert b"Now you can look like this little one." in response.data
        assert b"Secret Notes" in response.data
        assert Note.query.first().data == "This is a test"
        assert Note.query.first().user_id == User.query.first().id


def test_invalid_login(client, app):
    """
    Given an email and a password, without prior registration, the page should reload and flash an error message.
    The home page "/" should not be accessible.
    """

    data_user = {"email": "tibi@test.com", "password": "strongpass"}
    client.post("/login", data=data_user)
    response = client.get("/")
    # will redirect the URL to login page(refresh)
    assert response.status_code == 302
    assert b"Email does not exist, please sign up."



