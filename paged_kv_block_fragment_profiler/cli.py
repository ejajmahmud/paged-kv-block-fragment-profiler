"""CLI for Paged KV Block Fragment Profiler."""
import argparse
import json
from .core import PagedKVProfiler


def main():
    parser = argparse.ArgumentParser(description="Paged KV Block Fragment Profiler CLI")
    parser.add_argument("--block-size", type=int, default=16, help="KV cache block size")
    args = parser.parse_args()

    prof = PagedKVProfiler(total_physical_blocks=512)
    seqs = [
        {"seq_len": 49, "block_ids": [1, 2, 3, 4]},
        {"seq_len": 35, "block_ids": [1, 2, 5]},
    ]
    print(json.dumps(prof.profile(seqs, block_size=args.block_size), indent=2))


if __name__ == "__main__":
    main()
