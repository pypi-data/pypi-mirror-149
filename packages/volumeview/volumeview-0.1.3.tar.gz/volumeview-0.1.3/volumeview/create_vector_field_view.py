import os
import kachery_cloud as kcl
import numpy as np
import figurl as fig
from figurl.core.serialize_wrapper import _serialize

def create_vector_field_view(v: np.ndarray):
    assert v.ndim == 4, 'Array must be 4-dimensional (first dimension must be size 3)'
    num_components = v.shape[0]
    nx = v.shape[1]
    ny = v.shape[2]
    nz = v.shape[3]
    assert num_components == 3
    assert nx * ny * nz <= 1e7
    assert v.dtype in [np.float32, np.int16, np.int32], f'Unsupported data type: {v.dtype}'
    data_uri = kcl.store_json(_serialize(v))
    data = {
        'type': 'vector_field',
        'dataUri': data_uri,
        'dataShape': v.shape
    }
    F = fig.Figure(view_url='gs://figurl/volumeview-3', data=data)
    return F
