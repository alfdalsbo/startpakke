#!/usr/bin/env python3
"""Kontroller struktur, eiere, ruter og budsjetter uten nettverk eller skriving."""
from pathlib import Path
import argparse,json,sys
from checks import check

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--ready',action='store_true');p.add_argument('--public',action='store_true');p.add_argument('--json',action='store_true');a=p.parse_args()
    result=check(a.root,a.ready,a.public);result['status']='blocked' if result['errors'] else 'ok'
    if a.json:print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        for w in result['warnings']:print('VARSEL:',w)
        for e in result['errors']:print('FEIL:',e)
        print('STRUKTURKONTROLL BESTÅTT' if not result['errors'] else 'IKKE BESTÅTT');print(result['claim'])
    return bool(result['errors'])
if __name__=='__main__':sys.exit(main())
