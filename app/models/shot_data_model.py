from app.models.base_model import Base
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import datetime


class ShotData(Base):
    __tablename__ = "shot_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("training_sessions.id"), nullable=False)
    date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    time_stamp: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True),unique=True, nullable=False)
    stability_score: Mapped[Optional[float]] = mapped_column(Float)
    split: Mapped[Optional[float]] = mapped_column(Float)
    setup_upward_blue: Mapped[Optional[float]] = mapped_column(Float)
    setup_downward_green: Mapped[Optional[float]] = mapped_column(Float)
    targeting_yellow: Mapped[Optional[float]] = mapped_column(Float)
    hold_orange: Mapped[Optional[float]] = mapped_column(Float)
    cant: Mapped[Optional[float]] = mapped_column(Float)
    pitch: Mapped[Optional[float]] = mapped_column(Float)
    clicker: Mapped[Optional[str]] = mapped_column(String)
    target_x: Mapped[Optional[float]] = mapped_column(Float)
    target_y: Mapped[Optional[float]] = mapped_column(Float)
    target_score: Mapped[Optional[float]] = mapped_column(Float)
    problem_direction: Mapped[Optional[str]] = mapped_column(String)
    archery_target_index: Mapped[Optional[int]] = mapped_column(Integer)
    archery_hold_index: Mapped[Optional[int]] = mapped_column(Integer)
    archery_release_index: Mapped[Optional[int]] = mapped_column(Integer)
    archery_arrow_index: Mapped[Optional[int]] = mapped_column(Integer)
    archery_setup_time_raw: Mapped[Optional[float]] = mapped_column(Float)
    archery_draw_time_raw: Mapped[Optional[float]] = mapped_column(Float)
    archery_target_time_raw: Mapped[Optional[float]] = mapped_column(Float)
    archery_hold_time_raw: Mapped[Optional[float]] = mapped_column(Float)
    problem_degrees: Mapped[Optional[float]] = mapped_column(Float)
    problem_distance: Mapped[Optional[float]] = mapped_column(Float)

    # связь с TrainingSession
    session: Mapped["TrainingSession"] = relationship("TrainingSession", back_populates="shots")
