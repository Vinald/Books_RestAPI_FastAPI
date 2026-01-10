from sqlmodel import SQLModel, Field, Column
import uuid
from datetime import datetime
import sqlalchemy.dialects.postgresql as postgresql


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID | None = Field(
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            nullable=False,
        )
    )
    username: str = Field(nullable=False, unique=True)
    email: str = Field(nullable=False, unique=True)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    is_active: bool = Field(nullable=False, default=False)
    created_at: datetime = Field (
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )
    updated_at: datetime = Field (
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, email={self.email})"
