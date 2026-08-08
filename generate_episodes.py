#!/usr/bin/env python3
"""Legacy entry point for episode generation.

Older notes used ``EPISODE_COUNT`` with this filename.  Delegate to the
OpenRouter-aware generalized generator while retaining that environment-based
interface and never storing credentials in source control.
"""

from __future__ import annotations

import os
import sys

from generate_episodes_v3 import main


if __name__ == "__main__":
    if "EPISODE_COUNT" in os.environ and "--count" not in sys.argv:
        sys.argv.extend(["--count", os.environ["EPISODE_COUNT"]])
    main()
