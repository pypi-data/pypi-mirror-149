import os
from typing import List
import kachery_cloud as kcl
import numpy as np
import figurl as fig
from figurl.core.serialize_wrapper import _serialize

def create_volume_view(v: np.ndarray, *, component_names: List[str]):
    assert v.ndim == 4, 'Array must be 4-dimensional (first dimension is components)'
    num_components = v.shape[0]
    nx = v.shape[1]
    ny = v.shape[2]
    nz = v.shape[3]
    assert num_components == len(component_names)
    assert nx * ny * nz <= 1e7
    assert v.dtype in [np.float32, np.int16, np.int32], f'Unsupported data type: {v.dtype}'
    volume_uri = kcl.store_json(_serialize(v))
    data = {
        'type': 'volume',
        'dataUri': volume_uri,
        'dataShape': v.shape,
        'componentNames': component_names
    }
    F = fig.Figure(view_url='gs://figurl/volumeview-3', data=data)
    return F
