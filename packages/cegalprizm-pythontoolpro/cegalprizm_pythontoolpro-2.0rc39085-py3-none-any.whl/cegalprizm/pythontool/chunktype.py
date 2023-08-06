# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



class ChunkType(object):
    # fake enum
    chunk = -1
    none = 0  # 3d
    i = 1  # 2d islice
    j = 2
    k = 3  # 2d layer
    ij = 4  # 1d column
    jk = 5
    ik = 6
    ijk = 7  # single value

    names = {
        chunk: "chunk",
        none: "none",
        i: "i",
        j: "j",
        k: "k",
        ij: "ij",
        jk: "jk",
        ik: "ik",
        ijk: "ijk"
    }

    @classmethod
    def make(cls, i, j, k):
        if type(i) is tuple or type(j) is tuple or type(k) is tuple:
            return ChunkType.chunk
        if i is None and j is None and k is None:
            return ChunkType.chunk
        if i is not None and j is None and k is None:
            return ChunkType.i
        if i is None and j is not None and k is None:
            return ChunkType.j
        if i is None and j is None and k is not None:
            return ChunkType.k
        if i is not None and j is not None and k is None:
            return ChunkType.ij
        if i is None and j is not None and k is not None:
            return ChunkType.jk
        if i is not None and j is None and k is not None:
            return ChunkType.ik
        if i is not None and j is not None and k is not None:
            return ChunkType.ijk
