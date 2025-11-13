from app.models.base_model import Base
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import datetime


class TrainingSession(Base):
    __tablename__ = "training_sessions"


    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_summary_id: Mapped[int] = mapped_column(ForeignKey("user_summaries.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    score: Mapped[float] = mapped_column(Float)
    bow_type: Mapped[Optional[str]] = mapped_column(String(50))
    shot_count: Mapped[int] = mapped_column(Integer)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    handedness: Mapped[Optional[str]] = mapped_column(String(20))
    total_score: Mapped[Optional[float]] = mapped_column(Float)
    total_arrows: Mapped[Optional[int]] = mapped_column(Integer)
    total_x: Mapped[Optional[int]] = mapped_column(Integer)
    target_type: Mapped[Optional[str]] = mapped_column(String(50))
    target_size: Mapped[Optional[float]] = mapped_column(Float)
    distance: Mapped[Optional[float]] = mapped_column(Float)
    cant: Mapped[Optional[float]] = mapped_column(Float)
    pitch: Mapped[Optional[float]] = mapped_column(Float)
    bow_name: Mapped[Optional[str]] = mapped_column(String(100))
    bow_make: Mapped[Optional[str]] = mapped_column(String(100))
    bow_model: Mapped[Optional[str]] = mapped_column(String(100))
    d_loop: Mapped[Optional[float]] = mapped_column(Float)
    holding_weight: Mapped[Optional[float]] = mapped_column(Float)
    peep_height: Mapped[Optional[float]] = mapped_column(Float)
    draw_length: Mapped[Optional[float]] = mapped_column(Float)
    draw_weight: Mapped[Optional[float]] = mapped_column(Float)
    front_stabilizer_weight: Mapped[Optional[float]] = mapped_column(Float)
    front_stabilizer_length: Mapped[Optional[float]] = mapped_column(Float)
    rear_left_stabilizer_weight: Mapped[Optional[float]] = mapped_column(Float)
    rear_left_stabilizer_length: Mapped[Optional[float]] = mapped_column(Float)
    rear_right_stabilizer_weight: Mapped[Optional[float]] = mapped_column(Float)
    rear_right_stabilizer_length: Mapped[Optional[float]] = mapped_column(Float)

    # связь с UserSummary
    summary: Mapped["UserSummary"] = relationship("UserSummary", back_populates="training_sessions")

    shots: Mapped[list["ShotData"]] = relationship("ShotData", back_populates="session")
