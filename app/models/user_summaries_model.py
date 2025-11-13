from app.models.base_model import Base
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class UserSummary(Base):
    __tablename__ = "user_summaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    username: Mapped[str] = mapped_column(String(100))
    sessions: Mapped[int] = mapped_column(Integer)
    shots: Mapped[int] = mapped_column(Integer)
    average_score: Mapped[float] = mapped_column(Float)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # связь с User
    user: Mapped["User"] = relationship("User", back_populates="summaries")

    # связь с TrainingSession
    training_sessions: Mapped[list["TrainingSession"]] = relationship("TrainingSession", back_populates="summary")
