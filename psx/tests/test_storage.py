import tempfile
import unittest
from pathlib import Path

from psx.commands.cleanup import cache_usage, clean_cache, format_size


class TestStorageCleanup(unittest.TestCase):
    def test_cache_usage_and_cleanup(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            cache_file = root / "browser" / "cache.bin"
            cache_file.parent.mkdir()
            cache_file.write_bytes(b"cache data")

            size, files = cache_usage(root)
            self.assertEqual(size, 10)
            self.assertEqual(files, 1)

            removed_size, removed_files = clean_cache(root)
            self.assertEqual(removed_size, 10)
            self.assertEqual(removed_files, 1)
            self.assertEqual(cache_usage(root), (0, 0))

    def test_format_size(self):
        self.assertEqual(format_size(1024), "1.0 KB")
        self.assertEqual(format_size(1024 ** 2), "1.0 MB")


if __name__ == "__main__":
    unittest.main()
