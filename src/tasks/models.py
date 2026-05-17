from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, ForeignKey
from core.database import Base
from sqlalchemy.orm import relationship

class TaskModel(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    title = Column(String(150), nullable=False)
    description = Column(String(500), nullable=False)
    is_completed = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("UserModel", back_populates="tasks", uselist=False)
