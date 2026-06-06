from __future__ import annotations

from fastapi.testclient import TestClient

from angrybirds.levels import level_to_dict, load_level
from api.app import create_app


def build_client(tmp_path) -> TestClient:
    app = create_app(tmp_path / "physics_game_test.db")
    return TestClient(app)


def test_health_endpoint_returns_ok(tmp_path) -> None:
    with build_client(tmp_path) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_level(tmp_path) -> None:
    level_payload = level_to_dict(load_level("level1"))

    with build_client(tmp_path) as client:
        create_response = client.post(
            "/levels",
            json={
                "name": "Starter Level",
                "author": "Danny",
                "level_json": level_payload,
            },
        )
        level_id = create_response.json()["id"]
        fetch_response = client.get(f"/levels/{level_id}")

    assert create_response.status_code == 201
    assert fetch_response.status_code == 200
    assert fetch_response.json()["name"] == "Starter Level"
    assert fetch_response.json()["level_json"]["id"] == "level1"


def test_list_levels_returns_created_records(tmp_path) -> None:
    level_payload = level_to_dict(load_level("level2"))

    with build_client(tmp_path) as client:
        client.post(
            "/levels",
            json={
                "name": "List Level",
                "author": "Danny",
                "level_json": level_payload,
            },
        )
        list_response = client.get("/levels")

    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert list_response.json()[0]["author"] == "Danny"


def test_scores_and_leaderboard_are_sorted_descending(tmp_path) -> None:
    level_payload = level_to_dict(load_level("level3"))

    with build_client(tmp_path) as client:
        level_response = client.post(
            "/levels",
            json={
                "name": "Leaderboard Level",
                "author": "Danny",
                "level_json": level_payload,
            },
        )
        level_id = level_response.json()["id"]

        low_score = client.post(
            "/scores",
            json={"level_id": level_id, "player": "Alex", "score": 1200},
        )
        high_score = client.post(
            "/scores",
            json={"level_id": level_id, "player": "Blair", "score": 2200},
        )
        leaderboard = client.get(f"/leaderboard/{level_id}")

    assert low_score.status_code == 201
    assert high_score.status_code == 201
    assert leaderboard.status_code == 200
    leaderboard_rows = leaderboard.json()
    assert [row["player"] for row in leaderboard_rows] == ["Blair", "Alex"]
    assert [row["score"] for row in leaderboard_rows] == [2200, 1200]
