# from conftest import client
# from server import clubs
import server
import pytest

from datetime import datetime, timedelta


def test_index_should_status_code_ok(client):
    response = client.get("/")
    assert response.status_code == 200


def test_clubs_list_status_code_ok(client):
    response = client.get("/clubs_list")
    assert response.status_code == 200


def test_clubs_list_content(client):
    response = client.get("/clubs_list")
    data = response.data.decode()
    expected_value = "<ul id='clubs_list'>"
    assert expected_value in data


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
                "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
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


def test_purchasePlaces_book_negative_place(client, mocker):
    mocker.patch.object(
        server,
        "clubs",
        [{"name": "test_club", "email": "test@gmail.com", "points": server.PRICE_PER_PLACE * 2}],
    )
    mocker.patch.object(
        server,
        "competitions",
        [
            {
                "name": "test_festival",
                "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
                "numberOfPlaces": 5,
            }
        ],
    )
    response = client.post(
        "/purchasePlaces",
        data={"competition": "test_festival", "club": "test_club", "places": "-1"},
    )
    data = response.data.decode()
    expected_value_club = f"Points available: {server.PRICE_PER_PLACE}"
    expected_value_competition = "Number of Places: 4"
    assert response.status_code == 200
    assert expected_value_club in data
    assert expected_value_competition in data


def test_purchasePlace_without_data(client, mocker):
    mocker.patch.object(
        server,
        "clubs",
        [{"name": "test_club", "email": "test@gmail.com", "points": 5}],
    )
    mocker.patch.object(
        server,
        "competitions",
        [
            {
                "name": "test_festival",
                "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
                "numberOfPlaces": 6,
            }
        ],
    )
    response = client.post(
        "/purchasePlaces",
        data={"competition": "test_festival", "club": "test_club", "places": ""},
    )
    data = response.data.decode()
    expected_value_club = "Points available: 5"
    expected_value_competition = "Number of Places: 6"
    expected_flash_message = "Bad request : number of place must be an integer !"
    assert response.status_code == 400
    assert expected_value_club in data
    assert expected_value_competition in data
    assert expected_flash_message in data


def test_purchase_more_than_max_place_per_competition(client, mocker):
    mocker.patch.object(
        server,
        "clubs",
        [{"name": "test_club", "email": "test@gmail.com", "points": 15}],
    )
    mocker.patch.object(
        server,
        "competitions",
        [
            {
                "name": "test_festival",
                "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
                "numberOfPlaces": 15,
            }
        ],
    )
    response = client.post(
        "/purchasePlaces",
        data={"competition": "test_festival", "club": "test_club", "places": server.MAX_PLACES + 2},
    )
    data = response.data.decode()
    expected_value_club = "Points available: 15"
    expected_value_competition = "Number of Places: 15"
    expected_flash_message = "Error : Too much places booked"
    assert response.status_code == 403
    assert expected_value_club in data
    assert expected_value_competition in data
    assert expected_flash_message in data


def test_purchase_past_competition(client, mocker):
    mocker.patch.object(
        server,
        "clubs",
        [{"name": "test_club", "email": "test@gmail.com", "points": 15}],
    )
    mocker.patch.object(
        server,
        "competitions",
        [
            {
                "name": "test_festival",
                "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
                "numberOfPlaces": 15,
            }
        ],
    )
    response = client.post(
        "/purchasePlaces",
        data={"competition": "test_festival", "club": "test_club", "places": "1"},
    )
    data = response.data.decode()
    expected_value_club = "Points available: 15"
    expected_value_competition = "Number of Places: 15"
    expected_flash_message = "Error : you cannot book a place in a past competition !"
    assert response.status_code == 403
    assert expected_value_club in data
    assert expected_value_competition in data
    assert expected_flash_message in data


# TODO : à déplacer dans les test fonctionnels
# SUREMEENT PAS UN TEST UNITAIRE => il y a deux actions du client
def test_purchase_more_than_max_place_per_competition_with_2_request(client, mocker):
    mocker.patch.object(
        server,
        "clubs",
        [{"name": "test_club", "email": "test@gmail.com", "points": server.MAX_PLACES * 3}],
    )
    mocker.patch.object(
        server,
        "competitions",
        [
            {
                "name": "test_festival",
                "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
                "numberOfPlaces": server.MAX_PLACES * 3,
            }
        ],
    )
    response = client.post(
        "/purchasePlaces",
        data={"competition": "test_festival", "club": "test_club", "places": server.MAX_PLACES},
    )

    # time.sleep(5)

    response2 = client.post(
        "/purchasePlaces",
        data={"competition": "test_festival", "club": "test_club", "places": server.MAX_PLACES},
    )
    data = response2.data.decode()
    expected_value_club = f"Points available: {(server.MAX_PLACES * 3)}"
    expected_value_competition = f"Number of Places: {(server.MAX_PLACES * 3)}"
    expected_flash_message = (
        f"Error : A club can&#39;t reserve more than {server.MAX_PLACES} places to the same competition"
    )

    assert response.status_code == 403
    assert expected_value_club in data
    assert expected_value_competition in data
    assert expected_flash_message in data
