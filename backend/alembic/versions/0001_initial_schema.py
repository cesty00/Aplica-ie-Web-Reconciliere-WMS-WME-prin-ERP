"""initial schema

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-06-10
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "0001_initial_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    source_system = sa.Enum("WMS", "WME", "ERP", "MANUAL_UPLOAD", name="sourcesystem")
    import_type = sa.Enum("AUTOMATIC", "MANUAL", "TEST", name="importtype")
    import_status = sa.Enum("PENDING", "RUNNING", "SUCCESS", "PARTIAL_SUCCESS", "FAILED", name="importstatus")
    economic_sign = sa.Enum("IN", "OUT", "NEUTRAL", "UNKNOWN", name="economicsign")
    run_status = sa.Enum("DRAFT", "IN_PROGRESS", "NEEDS_REVIEW", "COMPLETED", "BLOCKED", "REOPENED", name="runstatus")
    match_type = sa.Enum(
        "EXACT",
        "NORMALIZED_DOCUMENT",
        "DATE_QUANTITY",
        "PARTNER_DATE_QUANTITY",
        "PRODUCTION_COMMAND",
        "NETTED",
        "MANUAL",
        name="matchtype",
    )
    verdict = sa.Enum("MATCH", "MATCH_AFTER_NETTING", "REVIEW", "NOT_MATCH", name="verdict")

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("product_code", sa.String(length=64), nullable=False),
        sa.Column("product_name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=128), nullable=True),
        sa.Column("unit", sa.String(length=32), nullable=True),
        sa.Column("is_finished_good", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("is_raw_material", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("is_packaging", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("product_code"),
    )
    op.create_index("ix_products_product_code", "products", ["product_code"])

    op.create_table(
        "lots",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("lot_code", sa.String(length=128), nullable=False),
        sa.Column("supplier_lot", sa.String(length=128), nullable=True),
        sa.Column("production_date", sa.Date(), nullable=True),
        sa.Column("expiry_date", sa.Date(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="ACTIVE"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_lots_product_id", "lots", ["product_id"])
    op.create_index("ix_lots_lot_code", "lots", ["lot_code"])

    op.create_table(
        "import_batches",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source_system", source_system, nullable=False),
        sa.Column("import_type", import_type, nullable=False),
        sa.Column("period_from", sa.Date(), nullable=True),
        sa.Column("period_to", sa.Date(), nullable=True),
        sa.Column("status", import_status, nullable=False, server_default="PENDING"),
        sa.Column("records_imported", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("records_rejected", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_log", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_import_batches_source_system", "import_batches", ["source_system"])
    op.create_index("ix_import_batches_import_type", "import_batches", ["import_type"])
    op.create_index("ix_import_batches_status", "import_batches", ["status"])

    op.create_table(
        "wms_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("import_batch_id", sa.Integer(), sa.ForeignKey("import_batches.id"), nullable=False),
        sa.Column("product_code", sa.String(length=64), nullable=False),
        sa.Column("product_name", sa.String(length=255), nullable=True),
        sa.Column("lot_code", sa.String(length=128), nullable=True),
        sa.Column("event_date", sa.Date(), nullable=False),
        sa.Column("raw_operation_type", sa.String(length=128), nullable=False),
        sa.Column("canonical_bucket", sa.String(length=64), nullable=True),
        sa.Column("document_no", sa.String(length=128), nullable=True),
        sa.Column("normalized_document_no", sa.String(length=128), nullable=True),
        sa.Column("inbound_document_no", sa.String(length=128), nullable=True),
        sa.Column("order_no", sa.String(length=128), nullable=True),
        sa.Column("partner", sa.String(length=255), nullable=True),
        sa.Column("location_from", sa.String(length=64), nullable=True),
        sa.Column("location_to", sa.String(length=64), nullable=True),
        sa.Column("quantity", sa.Numeric(18, 6), nullable=False),
        sa.Column("economic_sign", economic_sign, nullable=False, server_default="UNKNOWN"),
        sa.Column("reason_code", sa.String(length=128), nullable=True),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("source_file", sa.String(length=255), nullable=True),
        sa.Column("source_row", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    for col in ["import_batch_id", "product_code", "lot_code", "event_date", "canonical_bucket", "document_no", "normalized_document_no", "order_no"]:
        op.create_index(f"ix_wms_events_{col}", "wms_events", [col])

    op.create_table(
        "wme_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("import_batch_id", sa.Integer(), sa.ForeignKey("import_batches.id"), nullable=False),
        sa.Column("product_code", sa.String(length=64), nullable=False),
        sa.Column("product_name", sa.String(length=255), nullable=True),
        sa.Column("lot_code", sa.String(length=128), nullable=True),
        sa.Column("event_date", sa.Date(), nullable=False),
        sa.Column("document_type", sa.String(length=64), nullable=False),
        sa.Column("document_no", sa.String(length=128), nullable=False),
        sa.Column("normalized_document_no", sa.String(length=128), nullable=True),
        sa.Column("warehouse", sa.String(length=64), nullable=True),
        sa.Column("partner", sa.String(length=255), nullable=True),
        sa.Column("quantity_in", sa.Numeric(18, 6), nullable=False, server_default="0"),
        sa.Column("quantity_out", sa.Numeric(18, 6), nullable=False, server_default="0"),
        sa.Column("quantity_signed", sa.Numeric(18, 6), nullable=False, server_default="0"),
        sa.Column("stock_after", sa.Numeric(18, 6), nullable=True),
        sa.Column("canonical_bucket", sa.String(length=64), nullable=True),
        sa.Column("economic_sign", economic_sign, nullable=False, server_default="UNKNOWN"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("source_file", sa.String(length=255), nullable=True),
        sa.Column("source_row", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    for col in ["import_batch_id", "product_code", "lot_code", "event_date", "document_type", "document_no", "normalized_document_no", "warehouse", "canonical_bucket"]:
        op.create_index(f"ix_wme_events_{col}", "wme_events", [col])

    op.create_table(
        "reconciliation_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("product_code", sa.String(length=64), nullable=False),
        sa.Column("lot_code", sa.String(length=128), nullable=True),
        sa.Column("date_from", sa.Date(), nullable=False),
        sa.Column("date_to", sa.Date(), nullable=False),
        sa.Column("run_status", run_status, nullable=False, server_default="DRAFT"),
        sa.Column("import_batch_wms_id", sa.Integer(), sa.ForeignKey("import_batches.id"), nullable=True),
        sa.Column("import_batch_wme_id", sa.Integer(), sa.ForeignKey("import_batches.id"), nullable=True),
        sa.Column("created_by", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("conclusion", sa.Text(), nullable=True),
    )
    op.create_index("ix_reconciliation_runs_product_code", "reconciliation_runs", ["product_code"])
    op.create_index("ix_reconciliation_runs_lot_code", "reconciliation_runs", ["lot_code"])
    op.create_index("ix_reconciliation_runs_run_status", "reconciliation_runs", ["run_status"])

    op.create_table(
        "reconciliation_matches",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("reconciliation_run_id", sa.Integer(), sa.ForeignKey("reconciliation_runs.id"), nullable=False),
        sa.Column("wms_event_id", sa.Integer(), sa.ForeignKey("wms_events.id"), nullable=True),
        sa.Column("wme_event_id", sa.Integer(), sa.ForeignKey("wme_events.id"), nullable=True),
        sa.Column("match_type", match_type, nullable=True),
        sa.Column("verdict", verdict, nullable=False),
        sa.Column("confidence_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("rule_applied", sa.String(length=255), nullable=False),
        sa.Column("quantity_difference", sa.Numeric(18, 6), nullable=True),
        sa.Column("date_difference_days", sa.Integer(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("reviewed_by", sa.String(length=128), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    for col in ["reconciliation_run_id", "wms_event_id", "wme_event_id", "match_type", "verdict"]:
        op.create_index(f"ix_reconciliation_matches_{col}", "reconciliation_matches", [col])

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.Column("action", sa.String(length=64), nullable=False),
        sa.Column("old_value", sa.Text(), nullable=True),
        sa.Column("new_value", sa.Text(), nullable=True),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("user_id", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_audit_logs_entity_type", "audit_logs", ["entity_type"])
    op.create_index("ix_audit_logs_entity_id", "audit_logs", ["entity_id"])
    op.create_index("ix_audit_logs_action", "audit_logs", ["action"])


def downgrade() -> None:
    op.drop_index("ix_audit_logs_action", table_name="audit_logs")
    op.drop_index("ix_audit_logs_entity_id", table_name="audit_logs")
    op.drop_index("ix_audit_logs_entity_type", table_name="audit_logs")
    op.drop_table("audit_logs")

    for col in ["reconciliation_run_id", "wms_event_id", "wme_event_id", "match_type", "verdict"]:
        op.drop_index(f"ix_reconciliation_matches_{col}", table_name="reconciliation_matches")
    op.drop_table("reconciliation_matches")

    op.drop_index("ix_reconciliation_runs_run_status", table_name="reconciliation_runs")
    op.drop_index("ix_reconciliation_runs_lot_code", table_name="reconciliation_runs")
    op.drop_index("ix_reconciliation_runs_product_code", table_name="reconciliation_runs")
    op.drop_table("reconciliation_runs")

    for col in ["import_batch_id", "product_code", "lot_code", "event_date", "document_type", "document_no", "normalized_document_no", "warehouse", "canonical_bucket"]:
        op.drop_index(f"ix_wme_events_{col}", table_name="wme_events")
    op.drop_table("wme_events")

    for col in ["import_batch_id", "product_code", "lot_code", "event_date", "canonical_bucket", "document_no", "normalized_document_no", "order_no"]:
        op.drop_index(f"ix_wms_events_{col}", table_name="wms_events")
    op.drop_table("wms_events")

    op.drop_index("ix_import_batches_status", table_name="import_batches")
    op.drop_index("ix_import_batches_import_type", table_name="import_batches")
    op.drop_index("ix_import_batches_source_system", table_name="import_batches")
    op.drop_table("import_batches")

    op.drop_index("ix_lots_lot_code", table_name="lots")
    op.drop_index("ix_lots_product_id", table_name="lots")
    op.drop_table("lots")

    op.drop_index("ix_products_product_code", table_name="products")
    op.drop_table("products")

    sa.Enum(name="verdict").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="matchtype").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="runstatus").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="economicsign").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="importstatus").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="importtype").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="sourcesystem").drop(op.get_bind(), checkfirst=True)
