from __future__ import absolute_import
from celery import shared_task
from django.conf import settings
from server.utils import build_structure

import requests
import datetime


@shared_task
def run_code(pipeline_id, run_id):
    headers = {'Authorization': f'Token {settings.API_KEY}'}
    r = requests.get(f'https://{settings.PARSAGON_HOST}/api/pipelines/{pipeline_id}/code/', headers=headers)
    code = r.json()['code']
    start_time = datetime.datetime.now()
    requests.patch(f'https://{settings.PARSAGON_HOST}/api/pipelines/runs/{run_id}/', headers=headers, json={'status': 'RUNNING'})
    loc = dict(locals(), **globals())
    try:
        exec(code, loc, loc)
    except Exception as e:
        #requests.post(f'https://{settings.PARSAGON_HOST}/api/pipelines/', headers=headers, json={'message': e, 'state': var_state})
        if 'driver' in loc:
            loc['driver'].quit()
        if 'display' in loc:
            loc['display'].stop()
        requests.patch(f'https://{settings.PARSAGON_HOST}/api/pipelines/runs/{run_id}/', headers=headers, json={'status': 'ERROR'})
        return
    requests.patch(f'https://{settings.PARSAGON_HOST}/api/pipelines/runs/{run_id}/', headers=headers, json={'status': 'FINISHED'})
