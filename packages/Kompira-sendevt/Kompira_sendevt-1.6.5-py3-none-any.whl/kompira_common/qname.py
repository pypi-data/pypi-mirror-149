# -*- coding: utf-8 -*-
RPCQ_NAME = 'rpc_queue'              # kompirad -> jobmngrd
RETQ_NAME = 'ret_queue'              # jobmngrd -> kompirad
HBQ_NAME = 'hb_queue'                # jobmngrd -> kompirad
IOQ_NAME = 'io_queue'                # sendevt -> kompirad
CANCEL_EXCHANGE_NAME = 'cancel_xchg' # kompirad -> jobmngrd(ブロードキャスト)
JOBQ_NAME = 'job_queue'              # kompirad -> jobmngrd(ジョブマネージャ毎)
