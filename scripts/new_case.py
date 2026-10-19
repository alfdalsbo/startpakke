#!/usr/bin/env python3
"""Opprett et saksutkast og registerlenke. Nekter å overskrive en eksisterende sak."""
from pathlib import Path
from tempfile import NamedTemporaryFile
import argparse,os,re,stat,sys

def create(root,slug,title):
    root=Path(root).resolve();title=title.strip()
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug):raise ValueError('Bruk små a-z, tall og bindestrek i slug')
    if not title.strip() or any(c in title for c in '\n\r[]'):raise ValueError('Tittel må være én tekstlinje uten hakeparenteser')
    path=root/'saker'/(slug+'.md');registry=root/'saker/README.md'
    if path.exists():raise ValueError('Saken finnes allerede; bruk eksisterende eier')
    template=(root/'maler/sak.md').read_text(encoding='utf-8')
    if not template.startswith('# Navn på saken\n'):raise ValueError('Saksmalen mangler forventet tittel; ingen filer endres')
    content=template.replace('# Navn på saken','# '+title,1)
    lock=registry.parent/'.new-case.lock'
    try:
        with lock.open('x',encoding='utf-8') as f:f.write(str(os.getpid())+'\n')
    except FileExistsError:
        raise ValueError('En saksopprettelse er allerede i gang. Hvis den er avbrutt: kontroller prosessen før .new-case.lock fjernes.') from None
    created=False;temporary=None
    try:
        old=registry.read_text(encoding='utf-8')
        with path.open('x',encoding='utf-8') as f:
            created=True
            f.write(content)
        with NamedTemporaryFile(mode='w',encoding='utf-8',dir=registry.parent,prefix='.new-case-',suffix='.tmp',delete=False) as f:
            temporary=Path(f.name)
            f.write(old+f'\n- [{title}]({slug}.md) – utkast, fyll metadata og kildegrunnlag.\n')
        if registry.read_text(encoding='utf-8')!=old:raise ValueError('Registeret ble endret under opprettelsen. Prøv igjen med gjeldende register.')
        temporary.chmod(stat.S_IMODE(registry.stat().st_mode))
        temporary.replace(registry)
    except Exception:
        if created and path.exists():path.unlink()
        raise
    finally:
        if temporary is not None and temporary.exists():temporary.unlink()
        lock.unlink()
    return path

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('slug');p.add_argument('--title',required=True);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);a=p.parse_args()
    try:print(create(a.root,a.slug,a.title));return 0
    except (ValueError,OSError) as e:print('FEIL:',e);return 1
if __name__=='__main__':sys.exit(main())
