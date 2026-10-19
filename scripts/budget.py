#!/usr/bin/env python3
"""Mål UTF-8-byte og vedlikehold dokumenttabellen fra samme konfigurasjon."""
from pathlib import Path
import argparse,json,sys,re
from checks import budgets,load_policy,budget_table,text

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--json',action='store_true');p.add_argument('--write-docs',action='store_true');a=p.parse_args();root=a.root.resolve()
    try:
        policy=load_policy(root)
        if a.write_docs:
            f=root/'docs/KONTEKSTSKALERING.md';s=text(f);table=budget_table(policy)
            if '<!-- BUDGET_TABLE -->' in s:s=s.replace('<!-- BUDGET_TABLE -->',table)
            else:s,_=re.subn(r'\| Klasse \| Varsel \|.*?(?=\n\n|\Z)',lambda _:table,s,count=1,flags=re.S)
            if table not in s:raise ValueError('Fant ikke tabellplassering')
            f.write_text(s,encoding='utf-8')
    except (OSError,ValueError,TypeError,KeyError) as e:
        r={'errors':[str(e)],'warnings':[],'measurements':[]}
        print(json.dumps(r,ensure_ascii=False,indent=2) if a.json else 'FEIL: '+str(e));return 1
    r=budgets(root,policy)
    if a.write_docs:r['updated']='docs/KONTEKSTSKALERING.md'
    if a.json:print(json.dumps(r,ensure_ascii=False,indent=2))
    else:
        if a.write_docs:print('Oppdatert docs/KONTEKSTSKALERING.md')
        for m in r['measurements']:print(f"{m['bytes']:>6} byte  {m['status']:<7} {m['name']}")
        for e in r['errors']:print('FEIL:',e)
    return bool(r['errors'])
if __name__=='__main__':sys.exit(main())
