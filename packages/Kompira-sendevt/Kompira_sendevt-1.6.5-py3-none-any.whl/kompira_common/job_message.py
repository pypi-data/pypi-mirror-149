import pickle

CONTENT_TYPE_JOB_RESULT = 'application/x-kompira-job-result'
CONTENT_TYPE_JOB_STREAM = 'application/x-kompira-job-stream'

def encode_body(contents):
    return pickle.dumps(contents)

def decode_body(body):
    assert isinstance(body, bytes)
    return pickle.loads(body)
