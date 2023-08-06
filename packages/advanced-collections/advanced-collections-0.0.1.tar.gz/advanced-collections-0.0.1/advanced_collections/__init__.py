__version__ = "0.0.1"

import advanced_collections.sorted as sorted
from ._memlist import MemList
from ._seglist import SegList

__all__ = ["MemList", "SegList", "sorted"]
