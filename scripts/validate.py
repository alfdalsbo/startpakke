#!/usr/bin/env python3
"""Kompatibel inngang fra startpakke 1.0; bruker nå full verifikasjon."""
from pathlib import Path
from checks import check as full_check
from verify import main

def check(root,ready=False):
    r=full_check(Path(root),ready);return r['errors'],r['warnings']
if __name__=='__main__':raise SystemExit(main())
