"""Tests for Paged KV Block Fragment Profiler."""
import unittest
from paged_kv_block_fragment_profiler.core import PagedKVProfiler


class TestPagedKVProfiler(unittest.TestCase):
    def test_computes_waste_and_cow_savings(self):
        prof = PagedKVProfiler(total_physical_blocks=100)
        res = prof.profile([
            {"seq_len": 17, "block_ids": [10, 11]},
            {"seq_len": 18, "block_ids": [10, 12]},
        ], block_size=16)
        self.assertEqual(res["logical_blocks"], 4)
        self.assertEqual(res["physical_blocks_used"], 3)
        self.assertEqual(res["cow_saved_blocks"], 1)
        self.assertAlmostEqual(res["internal_waste_pct"], 45.31, places=1)
