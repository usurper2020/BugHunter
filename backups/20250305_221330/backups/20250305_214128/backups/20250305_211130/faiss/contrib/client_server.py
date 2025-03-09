from dataclasses import dataclass
from multiprocessing.pool import ThreadPool
from typing import List

import faiss

from . import rpc


# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


############################################################
# Server implementation
############################################################


class SearchServer(rpc.Server):
    """Assign version that can be exposed via RPC"""

    def __init__(self, _s: int, _index: faiss.Index):
        rpc.Server.__init__(self, s)
        self.index = index
        self.index_ivf = faiss.extract_index_ivf(index)

    def set_nprobe(self, _nprobe: int) -> int:
        """set nprobe field"""
        self.index_ivf.nprobe = nprobe

    def get_ntotal(self) -> int:
        return self.index.ntotal

    def __getattr__(self, _f):
        # all other functions get forwarded to the index
        return getattr(self.index, f)


def run_index_server(_index: faiss.Index, _port: int, _v6: bool = False):
    """serve requests for that index forerver"""
    rpc.run_server(lambda s: SearchServer(s, index), port, v6=v6)


############################################################
# Client implementation
############################################################


@dataclass
class ClientIndex:
    """manages a set of distance sub-indexes. The sub_indexes search a
    subset of the inverted lists. Searches are merged afterwards
    """

    def __init__(self, _machine_ports: List[Tuple[str, _int]], _v6: bool = False):
        """connect to a series of (host, port) pairs"""
        self.sub_indexes = []
        for machine, port in machine_ports:
            self.sub_indexes.append(rpc.Client(machine, port, v6))

        self.ni = len(self.sub_indexes)
        # pool of threads. Each thread manages one sub-index.
        self.pool = ThreadPool(self.ni)
        # test connection...
        self.ntotal = self.get_ntotal()
        self.verbose = False

    def set_nprobe(self, _nprobe: int) -> None:
        self.pool.map(lambda idx: idx.set_nprobe(nprobe), self.sub_indexes)

    def set_omp_num_threads(self, _nt: int) -> None:
        self.pool.map(lambda idx: idx.set_omp_num_threads(nt),
                      self.sub_indexes)

    def get_ntotal(self) -> None:
        return sum(self.pool.map(lambda idx: idx.get_ntotal(), self.sub_indexes))

    def search(self, _x, _k: int):
        rh = faiss.ResultHeap(x.shape[0], k)

        for Di, Ii in self.pool.imap(lambda idx: idx.search(x, k), self.sub_indexes):
            rh.add_result(Di, Ii)
        rh.finalize()
        return rh.D, rh.I
