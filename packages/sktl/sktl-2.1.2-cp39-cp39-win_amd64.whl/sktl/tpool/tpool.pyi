from concurrent.futures import Future, ThreadPoolExecutor
from typing import List

class tPool(ThreadPoolExecutor):
    def watch(self, tasks: List[Future], name: str = ..., block: bool = ...): ...
