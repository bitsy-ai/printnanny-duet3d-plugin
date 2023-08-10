from typing import Any


def parse_job(data: dict[str, Any]) -> dict[str, Any] | None:
    job = data.get("job")
    if job is not None:
        pass
