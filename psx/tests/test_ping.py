import subprocess
import unittest
from unittest.mock import patch

from psx.commands.ping import ping_host


class TestPingHost(unittest.TestCase):
    @patch("subprocess.run")
    def test_ping_host_success(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["ping", "-c", "1", "example.com"],
            returncode=0,
            stdout="64 bytes from example.com (93.184.216.34): icmp_seq=1 ttl=57 time=10.2 ms\n",
            stderr="",
        )

        result = ping_host("example.com")
        self.assertEqual(result["host"], "example.com")
        self.assertTrue(result["reachable"])
        self.assertIn("10.2", result["latency"])

    @patch("subprocess.run")
    def test_ping_host_failure(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["ping", "-c", "1", "nonexistent.invalid"],
            returncode=1,
            stdout="",
            stderr="",
        )

        result = ping_host("nonexistent.invalid")
        self.assertEqual(result["host"], "nonexistent.invalid")
        self.assertFalse(result["reachable"])


if __name__ == "__main__":
    unittest.main()
