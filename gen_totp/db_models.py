from sqlalchemy import Column, String, DateTime
from datetime import datetime, timezone
import secrets
from gen_totp.database import Base


class TotpTable(Base):
    __tablename__ = "totp"

    id = Column(String(64), primary_key=True, index=True,
                unique=True, default=lambda: secrets.token_urlsafe(32))
    service_name = Column(String(50), nullable=False)
    secret_key = Column(String(255), nullable=False)
    last_used_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    def touch(self):
        self.last_used_at = datetime.now(timezone.utc)
