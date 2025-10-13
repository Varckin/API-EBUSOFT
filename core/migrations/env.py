from sqlalchemy import create_engine
from alembic import context

from core.base.base import Base

from core.auth.models import Token
from gen_totp.db_models import TotpTable


config = context.config
target_metadata = Base.metadata

def run_migrations_offline():
    """Run in offline mode."""
    section = config.get_section("sqlalchemy")
    url = section.get("url")
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run in online mode."""
    section = config.get_section("sqlalchemy")
    url = section.get("url")
    connectable = create_engine(url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
