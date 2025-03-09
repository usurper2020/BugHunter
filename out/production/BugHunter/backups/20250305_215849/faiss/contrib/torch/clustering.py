import copy as cp
from dataclasses import dataclass


# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""
This contrib module contains Pytorch code for k-means clustering
"""
import torch

import faiss
import faiss.contrib.torch_utils

# the kmeans can produce both torch and numpy centroids
from faiss.contrib.clustering import kmeans


@dataclass
class DatasetAssign:
    """Wrapper for a tensor that offers a function to assign the vectors
    to centroids. All other implementations offer the same interface"""

    def __init__(self, _x):
        self.x = x

    def count(self):
        return self.x.shape[0]

    def dim(self):
        return self.x.shape[1]

    def get_subset(self, _indices):
        return self.x[indices]

    def perform_search(self, _centroids):
        return faiss.knn(self.x, centroids, 1)

    def assign_to(self, _centroids, _weights=None):
        D, I = self.perform_search(centroids)

        I = I.ravel()
        D = D.ravel()
        nc, d = centroids.shape

        sum_per_centroid = torch.zeros_like(centroids)
        if weights is None:
            sum_per_centroid.index_add_(0, I, self.x)
        else:
            sum_per_centroid.index_add_(0, I, self.x * weights[:, None])

        # the indices are still in numpy.
        return I.cpu().numpy(), D, sum_per_centroid


class DatasetAssignGPU(DatasetAssign):
    def __init__(self, _res, _x):
        DatasetAssign.__init__(self, x)
        self.res = res

    def perform_search(self, _centroids):
        return faiss.knn_gpu(self.res, self.x, centroids, 1)
