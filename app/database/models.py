from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True)

    ose_building_id: Mapped[int] = mapped_column(Integer)
    data_year: Mapped[int] = mapped_column(Integer)

    property_name: Mapped[str | None] = mapped_column(String(255))
    year_built: Mapped[int | None] = mapped_column(Integer)

    raw_data: Mapped[dict] = mapped_column(JSONB, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "ose_building_id",
            "data_year",
            name="uq_building_year",
        ),
    )


class PredictionInput(Base):
    __tablename__ = "prediction_inputs"

    id: Mapped[int] = mapped_column(primary_key=True)

    building_id: Mapped[int | None] = mapped_column(
        ForeignKey("buildings.id"),
        nullable=True,
    )

    building_age: Mapped[int] = mapped_column(Integer)
    primary_property_type: Mapped[str] = mapped_column(String(255))
    number_of_buildings: Mapped[int] = mapped_column(Integer)
    property_gfa_total: Mapped[float] = mapped_column(Float)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    building: Mapped[Building | None] = relationship()


class PredictionOutput(Base):
    __tablename__ = "prediction_outputs"

    id: Mapped[int] = mapped_column(primary_key=True)

    prediction_input_id: Mapped[int] = mapped_column(
        ForeignKey("prediction_inputs.id"),
        unique=True,
    )

    predicted_energy_consumption: Mapped[float] = mapped_column(Float)

    model_version: Mapped[str] = mapped_column(
        String(50),
        default="1.0",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    prediction_input: Mapped[PredictionInput] = relationship()