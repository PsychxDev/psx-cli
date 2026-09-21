import unittest
import io
import contextlib

from psx.commands.health import run as health
from psx.commands.profile import collect_profile


class TestProfileData(unittest.TestCase):
    def test_collect_profile_returns_expected_keys(self):
        profile = collect_profile()
        self.assertIn("hostname", profile)
        self.assertIn("os", profile)
        self.assertIn("kernel", profile)
        self.assertIn("uptime", profile)
        self.assertIn("memory", profile)
        self.assertIn("disk", profile)
        self.assertIn("network", profile)

    def test_profile_network_has_interface_list(self):
        profile = collect_profile()
        self.assertTrue(isinstance(profile["network"], list))

    def test_health_summary_focuses_on_machine_health(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            health()

        text = output.getvalue()
        self.assertIn("Processor", text)
        self.assertIn("Memory", text)
        self.assertIn("Storage", text)
        self.assertIn("Summary", text)
        self.assertIn("Processor", text)
        self.assertIn("Memory", text)
        self.assertIn("Storage", text)
        self.assertNotIn("Host:", text)
        self.assertNotIn("Uptime:", text)


if __name__ == "__main__":
    unittest.main()
