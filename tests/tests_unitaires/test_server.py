# from conftest import client
# from server import clubs
import server
import pytest


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


@pytest.mark.parametrize("club_place, competition_place", [(2, 10), (10, 2), (2, 2)])
def test_purchasePlaces_book_more_than_clubs_point_or_competition_places(
    client, mocker, club_place, competition_place
):
    mocker.patch.object(
        server,
        "clubs",
        [{"name": "test_club", "email": "test@gmail.com", "points": club_place}],
    )
    mocker.patch.object(
        server,
        "competitions",
        [
            {
                "name": "test_festival",
                "date": "2020-03-27 10:00:00",
                "numberOfPlaces": competition_place,
            }
        ],
    )
    response = client.post(
        "/purchasePlaces",
        data={"competition": "test_festival", "club": "test_club", "places": "8"},
    )
    data = response.data.decode()
    expected_data = "Error : Too much places booked"
    assert response.status_code == 403
    assert expected_data in data
