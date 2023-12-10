import io
from project import User
from werkzeug.datastructures import FileStorage


def test_get_main_page(test_client):
    response = test_client.get("/")
    # print('fROM TEST')
    assert b"<title>Flask Auth Example</title>" in response.data


def test_sign_in(app, test_client):
    response = test_client.post(
        "/signin",
        data={
            "email": "docentcafedry@protonmail.com",
            "name": "Lesha",
            "password": "2913454alex",
        },
    )

    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().email == "docentcafedry@protonmail.com"


def test_login(test_client):
    test_client.post(
        "/signin",
        data={
            "email": "docentcafedry@protonmail.com",
            "name": "Lesha",
            "password": "2913454alex",
        },
    )
    response = test_client.post(
        "/login",
        data={"email": "docentcafedry@protonmail.com", "password": "2913454alex"},
    )

    assert response.status == "302 FOUND"


def test_load_file(test_client):
    test_client.post(
        "/signin",
        data={
            "email": "docentcafedry@protonmail.com",
            "name": "Lesha",
            "password": "2913454alex",
        },
    )
    test_client.post(
        "/login",
        data={"email": "docentcafedry@protonmail.com", "password": "2913454alex"},
    )

    file = FileStorage(
        stream=io.BytesIO(b"my text contet"),
        filename="Input.txt",
        content_type="multipart/form-data",
    )

    response = test_client.post(
        "/upload", data={"file": file}, content_type="multipart/form-data"
    )

    assert response.status == "302 FOUND"


def test_delete_file(test_client):
    test_client.post(
        "/signin",
        data={
            "email": "docentcafedry@protonmail.com",
            "name": "Lesha",
            "password": "2913454alex",
        },
    )
    test_client.post(
        "/login",
        data={"email": "docentcafedry@protonmail.com", "password": "2913454alex"},
    )

    file = FileStorage(
        stream=io.BytesIO(b"my text contet"),
        filename="Input.txt",
        content_type="multipart/form-data",
    )

    test_client.post("/upload", data={"file": file}, content_type="multipart/form-data")

    response = test_client.delete(f"/delete/{file.filename}")

    assert response.status == "302 FOUND"


def test_upload_file(test_client):
    test_client.post(
        "/signin",
        data={
            "email": "docentcafedry@protonmail.com",
            "name": "Lesha",
            "password": "2913454alex",
        },
    )
    test_client.post(
        "/login",
        data={"email": "docentcafedry@protonmail.com", "password": "2913454alex"},
    )

    file = FileStorage(
        stream=io.BytesIO(b"my text contet"),
        filename="Input.txt",
        content_type="multipart/form-data",
    )

    test_client.post("/upload", data={"file": file}, content_type="multipart/form-data")

    response = test_client.get(f"/uploads/{file.filename}", follow_redirects=True)
    print(len(response.history))
    assert response.status == "200 OK"
