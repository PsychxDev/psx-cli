import unittest
from unittest.mock import patch

from psx.commands.track import collect_snapshot, format_bytes


class TestTrack(unittest.TestCase):
    @patch("psx.commands.track.temperature", return_value="42.0C")
    @patch("psutil.cpu_percent", return_value=24.0)
    @patch("psutil.net_io_counters")
    @patch("psutil.disk_usage")
    @patch("psutil.virtual_memory")
    def test_collect_snapshot(self, memory, disk, network, cpu, _temperature):
        memory.return_value.percent = 35
        disk.return_value.percent = 48
        network.return_value.bytes_sent = 1200
        network.return_value.bytes_recv = 3400

        snapshot = collect_snapshot((1000, 3000))

        self.assertEqual(snapshot["cpu"], 24.0)
        self.assertEqual(snapshot["memory"], 35)
        self.assertEqual(snapshot["disk"], 48)
        self.assertEqual(snapshot["sent"], 200)
        self.assertEqual(snapshot["received"], 400)
        self.assertEqual(snapshot["status"], "Healthy")

    def test_format_bytes(self):
        self.assertEqual(format_bytes(1024), "1.0 KB")
        self.assertEqual(format_bytes(1024 ** 2), "1.0 MB")


if __name__ == "__main__":
    unittest.main()
