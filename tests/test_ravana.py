"""
tests/test_ravana.py
Basic smoke tests — verify every module instantiates and runs its
primary method without raising an exception.
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Ensure repo root is on the path when running from the tests/ directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestConfig(unittest.TestCase):
    def test_head_map_has_16_entries(self):
        import config
        self.assertEqual(len(config.HEAD_MAP), 16)

    def test_all_constants_present(self):
        import config
        required = [
            "BASELINE_HR", "COERCION_LIMIT", "CHAFF_SIZE",
            "WIREGUARD_ENDPOINTS", "AUTHORIZED_MACS", "BLOAT_SERVICES",
            "LOG_SCRUB_TARGETS", "CCTV_BUFFER_PATH",
        ]
        for attr in required:
            self.assertTrue(hasattr(config, attr), f"config.{attr} is missing")


class TestBait(unittest.TestCase):
    def test_deploy_bait_creates_directory(self):
        import tempfile
        import config
        original = config.BAIT_VAULT_PATH
        with tempfile.TemporaryDirectory() as tmp:
            config.BAIT_VAULT_PATH = os.path.join(tmp, "vault_bait")
            from ravana_bait import deploy_bait
            deploy_bait()
            self.assertTrue(os.path.isdir(config.BAIT_VAULT_PATH))
            config.BAIT_VAULT_PATH = original


class TestScrub(unittest.TestCase):
    @patch("os.system")
    def test_scrub_logs_runs(self, mock_sys):
        from ravana_scrub import scrub_logs
        scrub_logs()  # Should not raise


class TestStripper(unittest.TestCase):
    def test_identify_bloat_runs(self):
        from ravana_stripper import LogicStripper
        s = LogicStripper()
        s.identify_bloat()  # Should not raise

    @patch("os.system")
    def test_decimate_runs(self, mock_sys):
        from ravana_stripper import LogicStripper
        s = LogicStripper()
        s.decimate()  # Should not raise


class TestSanitizer(unittest.TestCase):
    @patch("subprocess.run", side_effect=FileNotFoundError)
    def test_scan_no_tools_installed(self, mock_run):
        from ravana_sanitizer import SignalSanitizer
        s = SignalSanitizer()
        result = s.scan_for_static()
        self.assertFalse(result)


class TestGhost(unittest.TestCase):
    @patch("requests.get")
    def test_broadcast_noise(self, mock_get):
        from ravana_ghost import PerceptualGhost
        ghost = PerceptualGhost()
        ghost.broadcast_noise()  # Should not raise
        self.assertTrue(mock_get.called)


class TestSentinel(unittest.TestCase):
    def test_process_stream_returns_value(self):
        from ravana_sentinel import PrivacySentinel
        s = PrivacySentinel()
        result = s.process_stream("Raw_CCTV_Feed")
        self.assertIsNotNone(result)


class TestVisualPurge(unittest.TestCase):
    @patch("os.system")
    def test_purge_buffer_no_dir(self, mock_sys):
        from ravana_visual_purge import purge_buffer
        purge_buffer()  # Should not raise even if dir doesn't exist


class TestObfuscator(unittest.TestCase):
    def test_fragment_and_pad_returns_string(self):
        from ravana_obfuscator import DPIObfuscator
        obf = DPIObfuscator()
        result = obf.fragment_and_pad("test_data")
        self.assertIsInstance(result, str)
        self.assertIn("test_data", result)


class TestMirage(unittest.TestCase):
    def test_generate_ghost_signals_populates_nodes(self):
        from ravana_mirage import MirageGenerator
        m = MirageGenerator()
        m.generate_ghost_signals()
        self.assertEqual(len(m.virtual_nodes), 5)


class TestBioSentry(unittest.TestCase):
    def test_no_threat_below_limit(self):
        from ravana_bio_sentry import BioSentry
        sentry = BioSentry()
        self.assertFalse(sentry.evaluate_threat(72))

    @patch("ravana_bio_sentry.BioSentry.trigger_ghost_purge")
    def test_threat_above_limit(self, mock_purge):
        from ravana_bio_sentry import BioSentry
        sentry = BioSentry()
        self.assertTrue(sentry.evaluate_threat(150))
        mock_purge.assert_called_once()


class TestBaitSwitch(unittest.TestCase):
    def test_engage_decoy_changes_mode(self):
        from ravana_bait_switch import BaitSwitch
        switch = BaitSwitch()
        switch.engage_decoy()
        self.assertEqual(switch.mode, "DECOY")


class TestUltimate(unittest.TestCase):
    def test_run_shield_cycle_standard(self):
        from ravana_ultimate import RavanaUltimate
        r = RavanaUltimate()
        r.run_shield_cycle(72)  # Should not raise

    def test_run_shield_cycle_high_intensity(self):
        from ravana_ultimate import RavanaUltimate
        r = RavanaUltimate()
        r.run_shield_cycle(110)  # Should not raise

    def test_somatic_sync_high(self):
        from ravana_ultimate import RavanaUltimate
        r = RavanaUltimate()
        self.assertEqual(r.head_10_somatic_sync(110), "HIGH_INTENSITY")

    def test_somatic_sync_standard(self):
        from ravana_ultimate import RavanaUltimate
        r = RavanaUltimate()
        self.assertEqual(r.head_10_somatic_sync(70), "STANDARD")


class TestBiometric(unittest.TestCase):
    def test_manual_source(self):
        import config
        original = config.HR_INPUT_SOURCE
        config.HR_INPUT_SOURCE = "manual"
        from ravana_biometric import read_heart_rate
        hr = read_heart_rate()
        self.assertEqual(hr, config.HR_MANUAL_DEFAULT)
        config.HR_INPUT_SOURCE = original

    def test_file_source_fallback(self):
        import config
        original_source = config.HR_INPUT_SOURCE
        original_file = config.HR_INPUT_FILE
        config.HR_INPUT_SOURCE = "file"
        config.HR_INPUT_FILE = "/tmp/nonexistent_ravana_hr_test.txt"
        from ravana_biometric import read_heart_rate
        hr = read_heart_rate()
        self.assertEqual(hr, config.HR_MANUAL_DEFAULT)
        config.HR_INPUT_SOURCE = original_source
        config.HR_INPUT_FILE = original_file

    def test_file_source_reads_value(self):
        import config
        import tempfile
        original_source = config.HR_INPUT_SOURCE
        original_file = config.HR_INPUT_FILE
        config.HR_INPUT_SOURCE = "file"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("88")
            config.HR_INPUT_FILE = f.name
        try:
            import importlib
            import ravana_biometric
            importlib.reload(ravana_biometric)
            hr = ravana_biometric.read_heart_rate()
            self.assertEqual(hr, 88)
        finally:
            os.unlink(config.HR_INPUT_FILE)
            config.HR_INPUT_SOURCE = original_source
            config.HR_INPUT_FILE = original_file


if __name__ == "__main__":
    unittest.main()
