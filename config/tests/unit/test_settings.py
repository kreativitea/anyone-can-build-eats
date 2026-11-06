"""Settings are read once, when Python first imports them, so each test reads
them again in a new Python, with the environment variables it needs."""

import json
import os
import subprocess
import sys
import unittest

from django.conf import settings


def settings_with(**env):
    """Import config.settings in a fresh Python, with only these variables changed."""
    code = (
        "import json, config.settings as s; "
        "print(json.dumps({'hosts': s.ALLOWED_HOSTS, "
        "'origins': s.CSRF_TRUSTED_ORIGINS, "
        "'engine': s.DATABASES['default']['ENGINE']}))"
    )
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=settings.BASE_DIR,
        env={**os.environ, **env},
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


class DatabaseSettingsTests(unittest.TestCase):
    def test_empty_database_url_means_sqlite(self):
        self.assertEqual(
            settings_with(DATABASE_URL="")["engine"], "django.db.backends.sqlite3"
        )

    def test_database_url_picks_postgres(self):
        url = "postgresql://user:not-a-real-password@localhost:5432/example"
        self.assertEqual(
            settings_with(DATABASE_URL=url)["engine"],
            "django.db.backends.postgresql",
        )


class RenderSettingsTests(unittest.TestCase):
    def test_render_address_is_allowed(self):
        found = settings_with(RENDER_EXTERNAL_HOSTNAME="gaidai-eats.onrender.com")
        self.assertIn("gaidai-eats.onrender.com", found["hosts"])
        # Forms sent from that address (log-in, sign-up, reviews) are accepted.
        self.assertIn("https://gaidai-eats.onrender.com", found["origins"])
