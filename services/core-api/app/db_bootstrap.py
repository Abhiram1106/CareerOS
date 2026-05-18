from pathlib import Path

from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory

from .config import AUTO_CREATE_TABLES
from .database import Base, engine


class DatabaseNotReadyError(RuntimeError):
    pass


def _alembic_config() -> Config:
    project_root = Path(__file__).resolve().parents[1]
    config = Config(str(project_root / "alembic.ini"))
    config.set_main_option("script_location", str(project_root / "migrations"))
    return config


def _current_head_revision() -> str:
    script = ScriptDirectory.from_config(_alembic_config())
    return script.get_current_head()


def _current_db_revision() -> str | None:
    with engine.connect() as connection:
        context = MigrationContext.configure(connection)
        return context.get_current_revision()


def bootstrap_database() -> None:
    if AUTO_CREATE_TABLES:
        Base.metadata.create_all(bind=engine)
        return

    db_revision = _current_db_revision()
    head_revision = _current_head_revision()
    if db_revision != head_revision:
        raise DatabaseNotReadyError(
            "Database schema is not at Alembic head. "
            "Run `alembic upgrade head` before starting Core API. "
            f"(current={db_revision}, head={head_revision})"
        )
