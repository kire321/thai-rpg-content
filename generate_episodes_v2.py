#!/usr/bin/env python3
"""Compatibility entry point for the generalized act-format generator.

The implementation lives in :mod:`generate_episodes_v3`; this filename is
kept because earlier content batches and contributor notes invoke v2.
"""

from generate_episodes_v3 import main


if __name__ == "__main__":
    main()
