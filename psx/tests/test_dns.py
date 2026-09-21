import unittest
from unittest.mock import patch

from psx.commands.dns import lookup_dns


class TestDNSLookup(unittest.TestCase):
    @patch("psx.commands.dns.socket.getaddrinfo")
    def test_lookup_dns_success(self, mock_getaddrinfo):
        mock_getaddrinfo.side_effect = [
            [
                (2, 0, 0, "", ("93.184.216.34", 0)),
                (10, 0, 0, "", ("2606:4700:10::6814:179a", 0, 0, 0)),
            ],
            [
                (2, 0, 0, "", ("93.184.216.34", 0)),
            ],
        ]

        result = lookup_dns("example.com")
        self.assertEqual(result["domain"], "example.com")
        self.assertIn("93.184.216.34", result["a_records"])
        self.assertIn("2606:4700:10::6814:179a", result["aaaa_records"])

    @patch("psx.commands.dns.socket.getaddrinfo")
    def test_lookup_dns_failure(self, mock_getaddrinfo):
        mock_getaddrinfo.side_effect = OSError("boom")

        result = lookup_dns("invalid.invalid")
        self.assertFalse(result["reachable"])
        self.assertIn("error", result["status"])


if __name__ == "__main__":
    unittest.main()
