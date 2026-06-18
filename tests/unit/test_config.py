import importlib
import os

def test_settings_uses_default_database_url(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    import arkana.config
    importlib.reload(arkana.config)

    assert (
        arkana.config.settings.database_url
        == "postgresql+psycopg://arkana:arkana@localhost:5432/arkana"
    )

def test_settings_reads_database_url_from_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://test:test@localhost:5432/testdb")
    import arkana.config
    importlib.reload(arkana.config)

    assert arkana.config.settings.database_url == "postgresql+psycopg://test:test@localhost:5432/testdb"