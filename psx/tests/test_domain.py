import unittest
from unittest.mock import patch

from psx.commands.domain import (
    check_web_service,
    normalize_domain,
    prompt_selection,
    resolve_domain,
    suggest_domains,
    validate_domain,
)


class TestDomainNormalization(unittest.TestCase):
    def test_plain_domain(self):
        self.assertEqual(normalize_domain("example.com"), "example.com")

    def test_url_normalization(self):
        self.assertEqual(normalize_domain("https://example.com/test?a=1#frag"), "example.com")
        self.assertEqual(normalize_domain("http://example.com/path"), "example.com")

    def test_trailing_dot_and_whitespace(self):
        self.assertEqual(normalize_domain("  https://example.com./test?x=1  "), "example.com")

    def test_invalid_domain_rejected(self):
        with self.assertRaises(ValueError):
            normalize_domain("not a domain")

        with self.assertRaises(ValueError):
            normalize_domain("https://bad_host!!/path")


class TestDomainValidation(unittest.TestCase):
    def test_valid_hosts(self):
        self.assertTrue(validate_domain("example.com"))
        self.assertTrue(validate_domain("sub.example.co.uk"))

    def test_invalid_hosts(self):
        self.assertFalse(validate_domain(""))
        self.assertFalse(validate_domain("localhost"))
        self.assertFalse(validate_domain("127.0.0.1"))
        self.assertFalse(validate_domain("2001:db8::1"))
        self.assertFalse(validate_domain("-bad-.com"))


class TestDomainLookup(unittest.TestCase):
    @patch("psx.commands.domain.socket.getaddrinfo")
    def test_resolve_domain(self, mock_getaddrinfo):
        mock_getaddrinfo.return_value = [
            (socket_family := 2, 1, 6, "", ("93.184.216.34", 0)),
            (socket_family, 1, 6, "", ("93.184.216.35", 0)),
        ]

        result = resolve_domain("example.com")
        self.assertEqual(result["domain"], "example.com")
        self.assertIn("93.184.216.34", result["addresses"])
        self.assertIn("93.184.216.35", result["addresses"])

    @patch("psx.commands.domain.socket.create_connection")
    def test_check_web_service(self, mock_create_connection):
        mock_create_connection.return_value.__enter__.return_value = object()
        result = check_web_service("example.com")
        self.assertIn(80, result)
        self.assertIn(443, result)
        self.assertEqual(result[80]["status"], "Open")

    def test_suggestion_list(self):
        self.assertIn("github.com", suggest_domains("githb.com"))

    @patch("builtins.input", side_effect=["2", "x", "3"])
    def test_prompt_selection(self, _mock_input):
        options = ["github.com", "gitlab.com", "github.io"]
        self.assertEqual(prompt_selection(options), "gitlab.com")


if __name__ == "__main__":
    unittest.main()
