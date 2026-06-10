import enum
from datetime import datetime, date
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class SourceSystem(str, enum.Enum):
    WMS = "WMS"
    WME = "WME"
    ERP = "ERP"
    MANUAL_UPLOAD = "MANUAL_UPLOAD"


class ImportType(str, enum.Enum):
    AUTOMATIC = "AUTOMATIC"
    MANUAL = "MANUAL"
    TEST = "TEST"


class ImportStatus(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"
    FAILED = "FAILED"


class RunStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    IN_PROGRESS = "IN_PROGRESS"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    COMPLETED = "COMPLETED"
    BLOCKED = "BLOCKED"
    REOPENED = "REOPENED"


class MatchType(str, enum.Enum):
    EXACT = "EXACT"
    NORMALIZED_DOCUMENT = "NORMALIZED_DOCUMENT"
    DATE_QUANTITY = "DATE_QUANTITY"
    PARTNER_DATE_QUANTITY = "PARTNER_DATE_QUANTITY"
    PRODUCTION_COMMAND = "PRODUCTION_COMMAND"
    NETTED = "NETTED"
    MANUAL = "MANUAL"


class Verdict(str, enum.Enum):
    MATCH = "MATCH"
    MATCH_AFTER_NETTING = "MATCH_AFTER_NETTING"
    REVIEW = "REVIEW"
    NOT_MATCH = "NOT_MATCH"


class EconomicSign(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"
    NEUTRAL = "NEUTRAL"
    UNKNOWN = "UNKNOWN"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    product_name: Mapped[str] = mapped_column(String(255))
    category: Mapped[str | None] = mapped_column(String(128), nullable=True)
    unit: Mapped[str | None] = mapped_column(String(32), nullable=True)
    is_finished_good: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_raw_material: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_packaging: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    lots: Mapped[list["Lot"]] = relationship(back_populates="product")


class Lot(Base):
    __tablename__ = "lots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    lot_code: Mapped[str] = mapped_column(String(128), index=True)
    supplier_lot: Mapped[str | None] = mapped_column(String(128), nullable=True)
    production_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    expiry_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    product: Mapped[Product] = relationship(back_populates="lots")


class ImportBatch(Base):
    __tablename__ = "import_batches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_system: Mapped[SourceSystem] = mapped_column(Enum(SourceSystem), index=True)
    import_type: Mapped[ImportType] = mapped_column(Enum(ImportType), index=True)
    period_from: Mapped[date | None] = mapped_column(Date, nullable=True)
    period_to: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[ImportStatus] = mapped_column(Enum(ImportStatus), default=ImportStatus.PENDING, index=True)
    records_imported: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    records_rejected: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_log: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class WmsEvent(Base):
    __tablename__ = "wms_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    import_batch_id: Mapped[int] = mapped_column(ForeignKey("import_batches.id"), index=True)
    product_code: Mapped[str] = mapped_column(String(64), index=True)
    product_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    lot_code: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    event_date: Mapped[date] = mapped_column(Date, index=True)
    raw_operation_type: Mapped[str] = mapped_column(String(128))
    canonical_bucket: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    document_no: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    normalized_document_no: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    inbound_document_no: Mapped[str | None] = mapped_column(String(128), nullable=True)
    order_no: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    partner: Mapped[str | None] = mapped_column(String(255), nullable=True)
    location_from: Mapped[str | None] = mapped_column(String(64), nullable=True)
    location_to: Mapped[str | None] = mapped_column(String(64), nullable=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    economic_sign: Mapped[EconomicSign] = mapped_column(Enum(EconomicSign), default=EconomicSign.UNKNOWN)
    reason_code: Mapped[str | None] = mapped_column(String(128), nullable=True)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_file: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_row: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class WmeEvent(Base):
    __tablename__ = "wme_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    import_batch_id: Mapped[int] = mapped_column(ForeignKey("import_batches.id"), index=True)
    product_code: Mapped[str] = mapped_column(String(64), index=True)
    product_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    lot_code: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    event_date: Mapped[date] = mapped_column(Date, index=True)
    document_type: Mapped[str] = mapped_column(String(64), index=True)
    document_no: Mapped[str] = mapped_column(String(128), index=True)
    normalized_document_no: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    warehouse: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    partner: Mapped[str | None] = mapped_column(String(255), nullable=True)
    quantity_in: Mapped[Decimal] = mapped_column(Numeric(18, 6), default=0)
    quantity_out: Mapped[Decimal] = mapped_column(Numeric(18, 6), default=0)
    quantity_signed: Mapped[Decimal] = mapped_column(Numeric(18, 6), default=0)
    stock_after: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    canonical_bucket: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    economic_sign: Mapped[EconomicSign] = mapped_column(Enum(EconomicSign), default=EconomicSign.UNKNOWN)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_file: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_row: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ReconciliationRun(Base):
    __tablename__ = "reconciliation_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_code: Mapped[str] = mapped_column(String(64), index=True)
    lot_code: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    date_from: Mapped[date] = mapped_column(Date)
    date_to: Mapped[date] = mapped_column(Date)
    run_status: Mapped[RunStatus] = mapped_column(Enum(RunStatus), default=RunStatus.DRAFT, index=True)
    import_batch_wms_id: Mapped[int | None] = mapped_column(ForeignKey("import_batches.id"), nullable=True)
    import_batch_wme_id: Mapped[int | None] = mapped_column(ForeignKey("import_batches.id"), nullable=True)
    created_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    conclusion: Mapped[str | None] = mapped_column(Text, nullable=True)

    matches: Mapped[list["ReconciliationMatch"]] = relationship(back_populates="run")


class ReconciliationMatch(Base):
    __tablename__ = "reconciliation_matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reconciliation_run_id: Mapped[int] = mapped_column(ForeignKey("reconciliation_runs.id"), index=True)
    wms_event_id: Mapped[int | None] = mapped_column(ForeignKey("wms_events.id"), nullable=True, index=True)
    wme_event_id: Mapped[int | None] = mapped_column(ForeignKey("wme_events.id"), nullable=True, index=True)
    match_type: Mapped[MatchType | None] = mapped_column(Enum(MatchType), nullable=True, index=True)
    verdict: Mapped[Verdict] = mapped_column(Enum(Verdict), index=True)
    confidence_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    rule_applied: Mapped[str] = mapped_column(String(255))
    quantity_difference: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    date_difference_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewed_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    run: Mapped[ReconciliationRun] = relationship(back_populates="matches")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entity_type: Mapped[str] = mapped_column(String(64), index=True)
    entity_id: Mapped[int] = mapped_column(Integer, index=True)
    action: Mapped[str] = mapped_column(String(64), index=True)
    old_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    new_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    user_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
