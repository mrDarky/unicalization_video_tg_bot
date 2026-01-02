from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    language = Column(String, default="en", nullable=False)  # Language preference: en, ru
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    balance = Column(Float, default=0.0)
    tariff_plan_id = Column(Integer, ForeignKey("tariff_plans.id"), nullable=True)
    
    videos = relationship("Video", back_populates="user")
    deposits = relationship("Deposit", back_populates="user")
    withdrawals = relationship("Withdrawal", back_populates="user")
    referrals = relationship("User", backref="referrer", remote_side=[id])
    tariff_plan = relationship("TariffPlan", back_populates="users")
    daily_usages = relationship("DailyVideoUsage", back_populates="user")


class Video(Base):
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_id = Column(String, nullable=False)
    original_filename = Column(String, nullable=True)
    processed_filename = Column(String, nullable=True)
    mode = Column(Integer, nullable=False)  # 1 or 2
    status = Column(String, default="pending")  # pending, processing, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    file_size = Column(Integer, nullable=True)
    duration = Column(Float, nullable=True)
    modifications = Column(Text, nullable=True)  # JSON string of applied modifications
    
    user = relationship("User", back_populates="videos")


class Deposit(Base):
    __tablename__ = "deposits"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending, completed, failed
    payment_method = Column(String, nullable=True)
    transaction_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="deposits")


class Withdrawal(Base):
    __tablename__ = "withdrawals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending, completed, failed
    payment_method = Column(String, nullable=True)
    wallet_address = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="withdrawals")


class Setting(Base):
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False, index=True)
    value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Statistic(Base):
    __tablename__ = "statistics"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    total_users = Column(Integer, default=0)
    active_users = Column(Integer, default=0)
    total_videos = Column(Integer, default=0)
    processed_videos = Column(Integer, default=0)
    total_deposits = Column(Float, default=0.0)
    total_withdrawals = Column(Float, default=0.0)
    new_users = Column(Integer, default=0)
    new_videos = Column(Integer, default=0)


class TariffPlan(Base):
    __tablename__ = "tariff_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    videos_per_day = Column(Integer, nullable=False, default=10)  # Daily limit
    videos_per_order = Column(Integer, nullable=False, default=5)  # Per order/batch limit
    price = Column(Float, nullable=True, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    users = relationship("User", back_populates="tariff_plan")


class DailyVideoUsage(Base):
    __tablename__ = "daily_video_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    video_count = Column(Integer, default=0)
    
    user = relationship("User", back_populates="daily_usages")
