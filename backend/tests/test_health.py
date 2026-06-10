def health_check() -> dict[str, str]:
    return {"status": "ok", "mode": "read-only"}


def test_health_check() -> None:
    assert health_check() == {"status": "ok", "mode": "read-only"}
