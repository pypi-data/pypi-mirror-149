import hither2 as hi
from sortingview.config import job_cache, job_handler
from sortingview.helpers._prepare_snippets_h5 import prepare_snippets_h5
import kachery_client as kc

@kc.taskfunction('preload_extract_snippets.2', type='pure-calculation')
def task_preload_extract_snippets(recording_object, sorting_object, snippet_len=(50, 80)):
    with hi.Config(job_handler=job_handler.extract_snippets, job_cache=job_cache):
        snippets_h5 = hi.Job(prepare_snippets_h5, dict(recording_object=recording_object, sorting_object=sorting_object, snippet_len=snippet_len))
    return snippets_h5