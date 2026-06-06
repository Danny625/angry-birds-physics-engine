from __future__ import annotations

from angrybirds.scores import get_high_score, save_high_score


def test_high_score_only_updates_when_score_improves(tmp_path) -> None:
    database_path = tmp_path / "scores.db"

    assert get_high_score("level1", database_path) == 0
    assert save_high_score("level1", 1200, database_path) is True
    assert get_high_score("level1", database_path) == 1200

    assert save_high_score("level1", 800, database_path) is False
    assert get_high_score("level1", database_path) == 1200

    assert save_high_score("level1", 1600, database_path) is True
    assert get_high_score("level1", database_path) == 1600
