#!/usr/bin/env python3
"""Kontroller hele Git-indeksen isolert og bind resultatet til HEAD og tre-ID."""
from pathlib import Path,PurePosixPath
from tempfile import TemporaryDirectory
import argparse,io,json,subprocess,sys,tarfile

def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.PIPE)
def preflight(root,expected):
    root=Path(root).resolve();head=git(root,'rev-parse','HEAD').decode().strip()
    if expected and head!=expected:raise ValueError('HEAD er endret siden lesing; les og avstem før ny kontroll')
    if git(root,'ls-files','-u').strip():raise ValueError('Indeksen har uløste konflikter')
    tree=git(root,'write-tree').decode().strip();archive=git(root,'archive','--format=tar',tree)
    with TemporaryDirectory(prefix='startpakke-preflight-') as tmp:
        temp=Path(tmp)
        with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
            for member in tar.getmembers():
                rel=PurePosixPath(member.name)
                if rel.is_absolute() or '..' in rel.parts or not (member.isfile() or member.isdir()):raise ValueError('Kandidaten inneholder en utrygg eller ustøttet arkivpost')
                target=temp.joinpath(*rel.parts)
                if member.isdir():target.mkdir(parents=True,exist_ok=True)
                else:
                    target.parent.mkdir(parents=True,exist_ok=True)
                    with tar.extractfile(member) as source:target.write_bytes(source.read())
        script=temp/'scripts/verify.py'
        if not script.is_file():raise ValueError('Kandidaten mangler scripts/verify.py')
        result=subprocess.run([sys.executable,str(script),'--root',str(temp),'--json'],capture_output=True,text=True)
        if result.returncode not in [0,1]:raise ValueError('Kandidatkontrollen feilet teknisk: '+result.stderr[-1500:])
        report=json.loads(result.stdout)
        if not isinstance(report,dict) or report.get('status') not in ('ok','blocked') or not isinstance(report.get('errors'),list) or not isinstance(report.get('warnings'),list):raise ValueError('Kandidatkontrollen returnerte en ugyldig rapport')
        expected_status='blocked' if result.returncode or report['errors'] else 'ok'
        if report['status']!=expected_status:raise ValueError('Kandidatkontrollens avslutningskode, feil og status er motstridende')
    if git(root,'rev-parse','HEAD').decode().strip()!=head or git(root,'write-tree').decode().strip()!=tree:raise ValueError('HEAD eller indeks endret seg under kontrollen; kjør på nytt')
    return {'status':report['status'],'head':head,'tree':tree,'errors':report['errors'],'warnings':report['warnings'],'claim':'Hele staged kandidaten, ikke ustaged filer, eksterne originaler eller semantisk fullføring.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--expect-head');p.add_argument('--json',action='store_true');a=p.parse_args()
    try:r=preflight(a.root,a.expect_head)
    except (ValueError,OSError,subprocess.CalledProcessError) as e:r={'status':'blocked','errors':[str(e)],'warnings':[]}
    if a.json:print(json.dumps(r,ensure_ascii=False,indent=2))
    else:
        print(r['status'].upper(),r.get('tree',''))
        for e in r['errors']:print('FEIL:',e)
        for w in r['warnings']:print('VARSEL:',w)
        print(r.get('claim','Ingen godkjent kandidat'))
    return r['status']!='ok'
if __name__=='__main__':sys.exit(main())
