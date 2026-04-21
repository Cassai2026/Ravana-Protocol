"""
tests/test_ravana.py
Basic smoke tests — verify every module instantiates and runs its
primary method without raising an exception.
"""
import os
import subprocess
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
            "DECOY_PORT", "AUDIT_LOG_FILE", "AUDIT_KEY_FILE",
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


class TestBaitSwitchDecoy(unittest.TestCase):
    def test_engage_decoy_changes_mode(self):
        from ravana_bait_switch import BaitSwitch
        switch = BaitSwitch()
        switch.engage_decoy()
        self.assertEqual(switch.mode, "DECOY")

    @patch("ravana_bait_switch.socketserver.TCPServer")
    def test_decoy_server_starts(self, mock_server_cls):
        """engage_decoy should start the background TCP server thread."""
        mock_srv = MagicMock()
        mock_server_cls.return_value = mock_srv
        from ravana_bait_switch import BaitSwitch
        switch = BaitSwitch()
        switch.engage_decoy()
        mock_server_cls.assert_called_once()
        mock_srv.serve_forever.assert_called_once()

    @patch("ravana_bait_switch.socketserver.TCPServer", side_effect=OSError("port in use"))
    def test_decoy_server_gracefully_handles_error(self, _mock):
        """engage_decoy must not raise even if the port is unavailable."""
        from ravana_bait_switch import BaitSwitch
        switch = BaitSwitch()
        switch.engage_decoy()          # Should not raise
        self.assertEqual(switch.mode, "DECOY")

    @patch("ravana_bait_switch.socketserver.TCPServer")
    def test_stop_decoy_resets_mode(self, mock_server_cls):
        mock_srv = MagicMock()
        mock_server_cls.return_value = mock_srv
        from ravana_bait_switch import BaitSwitch
        switch = BaitSwitch()
        switch.engage_decoy()
        switch.stop_decoy()
        self.assertEqual(switch.mode, "SOVEREIGN")
        mock_srv.shutdown.assert_called_once()


class TestTunnel(unittest.TestCase):
    @patch("subprocess.run")
    def test_rotate_tunnel_calls_wg_quick(self, mock_run):
        """rotate_tunnel should call wg-quick down and then up."""
        import config
        original = config.WIREGUARD_ENDPOINTS
        config.WIREGUARD_ENDPOINTS = ["ep_a", "ep_b"]
        from ravana_tunnel import SilentTunnel
        tunnel = SilentTunnel()
        tunnel.rotate_tunnel()
        self.assertEqual(mock_run.call_count, 2)
        config.WIREGUARD_ENDPOINTS = original

    @patch("subprocess.run")
    def test_single_endpoint_skips_rotation(self, mock_run):
        """When only one endpoint exists, rotation should be skipped silently."""
        import config
        original = config.WIREGUARD_ENDPOINTS
        config.WIREGUARD_ENDPOINTS = ["only_ep"]
        from ravana_tunnel import SilentTunnel
        tunnel = SilentTunnel()
        tunnel.current_endpoint = "only_ep"
        tunnel.rotate_tunnel()
        mock_run.assert_not_called()
        config.WIREGUARD_ENDPOINTS = original

    @patch("subprocess.run", side_effect=FileNotFoundError)
    def test_rotate_handles_missing_wg_quick(self, _mock):
        """Missing wg-quick binary must not raise."""
        import config
        original = config.WIREGUARD_ENDPOINTS
        config.WIREGUARD_ENDPOINTS = ["ep_a", "ep_b"]
        from ravana_tunnel import SilentTunnel
        tunnel = SilentTunnel()
        tunnel.rotate_tunnel()   # Should not raise
        config.WIREGUARD_ENDPOINTS = original

    @patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "wg-quick"))
    def test_rotate_handles_command_error(self, _mock):
        """A CalledProcessError from wg-quick must not propagate."""
        import config
        original = config.WIREGUARD_ENDPOINTS
        config.WIREGUARD_ENDPOINTS = ["ep_a", "ep_b"]
        from ravana_tunnel import SilentTunnel
        tunnel = SilentTunnel()
        tunnel.rotate_tunnel()   # Should not raise
        config.WIREGUARD_ENDPOINTS = original


class TestIgnite(unittest.TestCase):
    @patch("ravana_supreme.ravana_master_watch")
    def test_ignite_calls_master_watch(self, mock_watch):
        """Running ravana_ignite as __main__ delegates to ravana_master_watch."""
        import runpy
        runpy.run_module("ravana_ignite", run_name="__main__", alter_sys=True)
        mock_watch.assert_called_once()


class TestIronClad(unittest.TestCase):
    @patch("ravana_tunnel.SilentTunnel.rotate_tunnel")
    @patch("ravana_mirage.MirageGenerator.generate_ghost_signals")
    @patch("ravana_obfuscator.DPIObfuscator.fragment_and_pad", return_value="ok")
    @patch("ravana_ultimate.RavanaUltimate.run_shield_cycle")
    def test_engage_iron_clad_runs(self, mock_cycle, mock_pad, mock_mirage, mock_tunnel):
        from ravana_iron_clad import engage_iron_clad
        engage_iron_clad(hr_input=72)
        mock_cycle.assert_called_once_with(72)
        mock_pad.assert_called_once()
        mock_mirage.assert_called_once()
        mock_tunnel.assert_called_once()


class TestAuditLog(unittest.TestCase):
    def _tmp_config(self, tmp_dir):
        """Monkey-patch config paths to temp dir and return originals."""
        import config
        orig_key = config.AUDIT_KEY_FILE
        orig_log = config.AUDIT_LOG_FILE
        config.AUDIT_KEY_FILE = os.path.join(tmp_dir, "audit.key")
        config.AUDIT_LOG_FILE = os.path.join(tmp_dir, "audit.log")
        return orig_key, orig_log

    def _restore_config(self, orig_key, orig_log):
        import config
        config.AUDIT_KEY_FILE = orig_key
        config.AUDIT_LOG_FILE = orig_log

    def test_log_and_read_round_trip(self):
        import tempfile
        import importlib
        import ravana_audit
        with tempfile.TemporaryDirectory() as tmp:
            orig_key, orig_log = self._tmp_config(tmp)
            importlib.reload(ravana_audit)
            try:
                ravana_audit.log_event("TEST_EVENT", "hello")
                entries = ravana_audit.read_audit_log()
                self.assertEqual(len(entries), 1)
                self.assertEqual(entries[0]["event"], "TEST_EVENT")
                self.assertEqual(entries[0]["detail"], "hello")
            finally:
                self._restore_config(orig_key, orig_log)
                importlib.reload(ravana_audit)

    def test_log_multiple_events(self):
        import tempfile
        import importlib
        import ravana_audit
        with tempfile.TemporaryDirectory() as tmp:
            orig_key, orig_log = self._tmp_config(tmp)
            importlib.reload(ravana_audit)
            try:
                ravana_audit.log_event("EVENT_A")
                ravana_audit.log_event("EVENT_B", "detail_b")
                entries = ravana_audit.read_audit_log()
                self.assertEqual(len(entries), 2)
                self.assertEqual(entries[0]["event"], "EVENT_A")
                self.assertEqual(entries[1]["event"], "EVENT_B")
            finally:
                self._restore_config(orig_key, orig_log)
                importlib.reload(ravana_audit)

    def test_read_empty_log_returns_empty_list(self):
        import tempfile
        import importlib
        import ravana_audit
        with tempfile.TemporaryDirectory() as tmp:
            orig_key, orig_log = self._tmp_config(tmp)
            importlib.reload(ravana_audit)
            try:
                entries = ravana_audit.read_audit_log()
                self.assertEqual(entries, [])
            finally:
                self._restore_config(orig_key, orig_log)
                importlib.reload(ravana_audit)


class TestIntegration(unittest.TestCase):
    """End-to-end smoke test for ravana_master_watch()."""

    @patch("ravana_tunnel.SilentTunnel.rotate_tunnel")
    @patch("ravana_mirage.MirageGenerator.generate_ghost_signals")
    @patch("ravana_obfuscator.DPIObfuscator.fragment_and_pad", return_value="ok")
    @patch("ravana_ultimate.RavanaUltimate.run_shield_cycle")
    @patch("ravana_sanitizer.SignalSanitizer.scan_for_static", return_value=False)
    @patch("requests.get")
    @patch("os.system")
    @patch("subprocess.run")
    @patch("ravana_biometric.read_heart_rate", return_value=72)
    @patch("ravana_audit.log_event")
    def test_master_watch_completes(
        self, mock_log, mock_hr, mock_sub, mock_sys,
        mock_get, mock_scan, mock_cycle, mock_pad,
        mock_mirage, mock_tunnel,
    ):
        import importlib
        import ravana_supreme
        importlib.reload(ravana_supreme)
        ravana_supreme.ravana_master_watch()
        # Audit log should have been called at least for boot and status
        self.assertGreater(mock_log.call_count, 0)


if __name__ == "__main__":
    unittest.main()

