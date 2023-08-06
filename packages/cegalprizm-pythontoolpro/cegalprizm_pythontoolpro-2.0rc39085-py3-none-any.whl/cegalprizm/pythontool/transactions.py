# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import contextlib

@contextlib.contextmanager
def tx(petrellink, obj, *objs):
    tx = petrellink._create_tx_provider()
    try:
        tx.Add(obj._petrel_object_link.PetrelObject)
        if objs is not None:
            for o in objs:
                tx.Add(o._petrel_object_link.PetrelObject)
        tx.StartTxs()
        yield
    finally:
        tx.CommitTxs()
