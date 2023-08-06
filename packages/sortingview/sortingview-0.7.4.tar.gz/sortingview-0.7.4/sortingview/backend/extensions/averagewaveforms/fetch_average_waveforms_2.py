from typing import Dict, List, Union

import hither2 as hi
from hither2.dockerimage import RemoteDockerImage
import kachery_client as kc
import numpy as np
from sortingview.serialize_wrapper import serialize_wrapper
# from labbox import LabboxContext
from sortingview.config import job_cache, job_handler
from sortingview.helpers import prepare_snippets_h5, get_unit_waveforms_from_snippets_h5

@hi.function(
    'fetch_average_waveform_2', '0.2.14',
    image=RemoteDockerImage('docker://magland/labbox-ephys-processing:0.3.19'),
    modules=['sortingview']
)
@serialize_wrapper
def fetch_average_waveform_2(snippets_h5, unit_id):
    import h5py
    h5_path = kc.load_file(snippets_h5)
    assert h5_path is not None
    unit_waveforms, unit_waveforms_channel_ids, channel_locations0, sampling_frequency, unit_spike_train = get_unit_waveforms_from_snippets_h5(h5_path, unit_id)
    
    average_waveform = np.mean(unit_waveforms, axis=0)

    return dict(
        average_waveform=average_waveform.astype(np.float32),
        channel_ids=unit_waveforms_channel_ids.astype(np.int32),
        channel_locations=channel_locations0.astype(np.float32),
        sampling_frequency=sampling_frequency
    )

@kc.taskfunction('fetch_average_waveform.2', type='pure-calculation')
def task_fetch_average_waveform(recording_object, sorting_object, unit_id, snippet_len=(50, 80)):
    with hi.Config(job_handler=job_handler.waveforms, job_cache=job_cache):
        with hi.Config(job_handler=job_handler.extract_snippets):
            snippets_h5 = prepare_snippets_h5.run(recording_object=recording_object, sorting_object=sorting_object, snippet_len=snippet_len)
        return fetch_average_waveform_2.run(
            snippets_h5=snippets_h5,
            unit_id=unit_id
        )

@hi.function('test_delay', '0.1.0')
def test_delay(delay_sec):
    import time
    time.sleep(delay_sec)
    return f'delayed: {delay_sec} sec'

@kc.taskfunction('test_delay.1', type='pure-calculation')
def task_test_delay(delay_sec, cachebust):
    with hi.Config(job_handler=job_handler.waveforms, job_cache=None):
        return test_delay.run(
            delay_sec=delay_sec
        )