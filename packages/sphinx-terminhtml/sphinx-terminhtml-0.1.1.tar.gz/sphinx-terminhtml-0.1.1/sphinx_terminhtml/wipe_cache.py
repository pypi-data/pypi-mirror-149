import shutil
from pathlib import Path

from sphinx_terminhtml.cache import TERMINAL_CACHE_DIR
from sphinx_terminhtml.logger import log


def wipe_cache_contents(cache_dir: Path = TERMINAL_CACHE_DIR):
    shutil.rmtree(cache_dir)


if __name__ == "__main__":
    wipe_cache_contents()
    log.info(f"Cache at {TERMINAL_CACHE_DIR} wiped.")