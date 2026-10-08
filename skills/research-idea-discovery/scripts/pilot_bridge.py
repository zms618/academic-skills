#!/usr/bin/env python3
"""Explicitly authorized *local* pilot command runner. Never runs without --execute."""
import argparse
import datetime as dt
import hashlib
import json
import subprocess
import sys
from pathlib import Path

def run(command,workdir,outdir,timeout=120,execute=False):
    if not command:raise ValueError('command required')
    folder=Path(workdir).resolve();dest=Path(outdir).resolve();dest.mkdir(parents=True,exist_ok=True)
    if not folder.is_dir():raise ValueError('workdir must already exist')
    log={'command':command,'workdir':str(folder),'started_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
         'authorized_execute':bool(execute),'status':'DRY_RUN','returncode':None}
    if execute:
        try:
            p=subprocess.run(command,cwd=folder,capture_output=True,text=True,timeout=timeout,check=False,shell=False)
            log['returncode']=p.returncode;log['status']='RUN_COMPLETE' if p.returncode==0 else 'RUN_FAILED'
            stdout_bytes=p.stdout[:100000].encode('utf-8')
            stderr_bytes=p.stderr[:100000].encode('utf-8')
            (dest/'stdout.txt').write_bytes(stdout_bytes)
            (dest/'stderr.txt').write_bytes(stderr_bytes)
            log['stdout_sha256']=hashlib.sha256(stdout_bytes).hexdigest()
        except subprocess.TimeoutExpired:
            log['status']='TIMEOUT';log['returncode']=None
        except OSError as e:log['status']='EXEC_ERROR';log['error']=str(e)
    (dest/'pilot_run.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
    return log

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--workdir',required=True);ap.add_argument('--outdir',required=True)
    ap.add_argument('--timeout',type=int,default=120);ap.add_argument('--execute',action='store_true');ap.add_argument('command',nargs=argparse.REMAINDER)
    a=ap.parse_args(argv);cmd=a.command[1:] if a.command and a.command[0]=='--' else a.command
    report=run(cmd,a.workdir,a.outdir,a.timeout,a.execute)
    print(report['status']);return 0 if report['status'] in ('DRY_RUN','RUN_COMPLETE') else 2
if __name__=='__main__':sys.exit(main())
