from contextlib import contextmanager
from typing import Optional, Iterator

from tqdm import tqdm

from terality._terality.errorreporting import is_ipython


@contextmanager
def data_transfer_progress_bar(total_size: int, desc: str) -> Iterator[Optional[tqdm]]:
    # Disable progress bar for non-interactive
    if is_ipython():
        yield tqdm(total=total_size, unit="B", unit_scale=True, desc=desc)
    else:
        yield None
