"""Core virtual KV-cache page table fragmentation and CoW sharing profiler."""
import math
from typing import Any, Dict, List


class PagedKVProfiler:
    """Profiles internal fragmentation, CoW block reuse, and capacity pressure in paged KV caches."""

    def __init__(self, total_physical_blocks: int = 4096):
        self.total_physical_blocks = total_physical_blocks

    def profile(self, sequences: List[Dict[str, Any]], block_size: int = 16) -> Dict[str, Any]:
        if block_size < 1:
            raise ValueError("block_size must be >= 1")
        total_tokens = 0
        logical_blocks = 0
        unique_phys = set()

        for seq in sequences:
            slen = int(seq["seq_len"])
            total_tokens += slen
            needed = math.ceil(slen / block_size) if slen > 0 else 0
            logical_blocks += needed
            for bid in seq.get("block_ids", []):
                unique_phys.add(bid)

        allocated_slots = logical_blocks * block_size
        wasted_slots = max(0, allocated_slots - total_tokens)
        waste_pct = round((wasted_slots / max(1, allocated_slots)) * 100.0, 2)
        phys_used = len(unique_phys) if unique_phys else logical_blocks
        cow_saved = max(0, logical_blocks - phys_used)
        pressure = round(phys_used / max(1, self.total_physical_blocks), 4)

        return {
            "block_size": block_size,
            "sequences": len(sequences),
            "logical_blocks": logical_blocks,
            "physical_blocks_used": phys_used,
            "cow_saved_blocks": cow_saved,
            "internal_waste_pct": waste_pct,
            "hbm_pressure": pressure,
        }
