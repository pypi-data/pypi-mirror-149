# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



# vertex definitions

"""Vertex indices

A call to :func:`cegalprizm.pythontool.Grid.vertices` returns a set of vertex positions indexed by these constants.

For ease of use, ``import`` the ``vertices`` module before using the constants defined.

**Example**:

.. code-block:: Python

  from cegalprizm.pythontool import vertices

  verts = my_grid.vertices(10, 15, 22)
  print(len(verts))   # outputs 8
  top_sw = verts[vertices.TopSouthWest]

"""
BaseSouthWest: int = 0
"""The base south-west vertex index"""
BaseNorthWest: int = 1
"""The base north-west vertex index"""
BaseNorthEast: int = 2
"""The base north-east vertex index"""
BaseSouthEast: int = 3
"""The base south-east vertex index"""
TopSouthWest: int = 4
"""The top south-east vertex index"""
TopNorthWest: int = 5
"""The top north-west vertex index"""
TopNorthEast: int = 6
"""The top north-east vertex index"""
TopSouthEast: int = 7
"""The top south-east vertex index"""
