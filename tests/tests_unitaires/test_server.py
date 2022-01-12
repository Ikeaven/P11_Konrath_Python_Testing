from tests.tests_unitaires.conftest import client

from server import clubs
import server


def test_index_should_status_code_ok(client):
    response = client.get("/")
    assert response.status_code == 200


def test_showSummary_valid_email(client, mocker):
    mocker.patch.object(
        server,
        "clubs",
        [{"name": "Simply Lift", "email": "test@gmail.com", "points": "13"}],
    )
    response = client.post("/showSummary", data={"email": "test@gmail.com"})
    assert response.status_code == 200


def test_showSummary_invalide_email(client, mocker):
    mocker.patch.object(
        server,
        "clubs",
        [{"name": "Simply Lift", "email": "test@gmail.com", "points": "13"}],
    )
    response = client.post("/showSummary", data={"email": "invalide@mail.com"})
    data = response.data.decode()
    expected_content = "<p>Error : Unknown Email</p>"
    assert expected_content in data
    assert response.status_code == 404
