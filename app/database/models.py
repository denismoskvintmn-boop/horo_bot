from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    Time,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=True)
    name = Column(String(255), nullable=False)
    gender = Column(String(10), nullable=False)
    birth_date = Column(Date, nullable=False)
    birth_time = Column(Time, nullable=True)
    birth_city = Column(String(255), nullable=False)
    timezone = Column(String(50), default="UTC")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    horoscopes = relationship("Horoscope", back_populates="user", cascade="all, delete-orphan")
    subscriptions = relationship(
        "Subscription", back_populates="user", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("gender IN ('male', 'female')", name="valid_gender"),
        Index("idx_user_birth_date", "birth_date"),
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, name={self.name})>"


class Horoscope(Base):
    __tablename__ = "horoscopes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    astronomy_json = Column(Text, nullable=False)
    text = Column(Text, nullable=False)
    status = Column(String(20), default="pending")
    sent_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="horoscopes")

    __table_args__ = (
        UniqueConstraint("user_id", "date", name="unique_user_date"),
        CheckConstraint("status IN ('pending', 'sent', 'failed')", name="valid_status"),
        Index("idx_horoscope_date_status", "date", "status"),
    )


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plan = Column(String(50), nullable=False)
    status = Column(String(20), default="active")
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="subscriptions")

    __table_args__ = (
        CheckConstraint("plan IN ('free', 'premium')", name="valid_plan"),
        CheckConstraint(
            "status IN ('active', 'cancelled', 'expired')",
            name="valid_subscription_status",
        ),
    )
