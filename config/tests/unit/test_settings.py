"""Settings are read once, when Python first imports them, so each test reads
them again in a new Python, with the environment variables it needs."""

import os
import subprocess
import sys
import unittest

from django.conf import settings


def engine_with(**env):
    """The database engine config.settings picks, with only these variables changed."""
    code = "import config.settings as s; print(s.DATABASES['default']['ENGINE'])"
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=settings.BASE_DIR,
        env={**os.environ, **env},
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


class DatabaseSettingsTests(unittest.TestCase):
    def test_empty_database_url_means_sqlite(self):
        self.assertEqual(engine_with(DATABASE_URL=""), "django.db.backends.sqlite3")

    def test_database_url_picks_postgres(self):
        url = "postgresql://user:not-a-real-password@localhost:5432/example"
        self.assertEqual(engine_with(DATABASE_URL=url), "django.db.backends.postgresql")
