from app.db.base import Base
from app.db import models  # noqa: F401


def test_mvp_01_tables_are_registered() -> None:
    expected_tables = {
        "products",
        "lots",
        "import_batches",
        "wms_events",
        "wme_events",
        "reconciliation_runs",
        "reconciliation_matches",
        "audit_logs",
    }

    assert expected_tables.issubset(set(Base.metadata.tables.keys()))
