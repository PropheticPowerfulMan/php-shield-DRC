"""Initial identity and organization schema. Auth flows are not active yet."""
from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlalchemy import DateTime, ForeignKey, MetaData, String, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

NAMING_CONVENTION = {"ix": "ix_%(column_0_label)s", "uq": "uq_%(table_name)s_%(column_0_name)s", "ck": "ck_%(table_name)s_%(constraint_name)s", "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s", "pk": "pk_%(table_name)s"}
class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)

user_roles = Table("user_roles", Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True))

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

class User(TimestampMixin, Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    roles: Mapped[list["Role"]] = relationship(secondary=user_roles, back_populates="users")

class Role(TimestampMixin, Base):
    __tablename__ = "roles"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    users: Mapped[list[User]] = relationship(secondary=user_roles, back_populates="roles")

class Institution(TimestampMixin, Base):
    __tablename__ = "institutions"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)

class Department(TimestampMixin, Base):
    __tablename__ = "departments"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    institution_id: Mapped[UUID] = mapped_column(ForeignKey("institutions.id", ondelete="RESTRICT"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
