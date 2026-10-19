#!/usr/bin/env python3
"""Regresjon for oppgaveeierskap, lenker, datoer og klarhetskontroll."""
from pathlib import Path
from tempfile import TemporaryDirectory
import shutil,unittest,json
from validate import check

ROOT=Path(__file__).resolve().parents[1]
class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp=TemporaryDirectory();self.root=Path(self.temp.name)/'system'
        shutil.copytree(ROOT,self.root,ignore=shutil.ignore_patterns('__pycache__','.git','node_modules'))
    def tearDown(self):self.temp.cleanup()
    def test_initial_pilot_is_structurally_valid_but_not_ready(self):
        self.assertEqual(check(self.root)[0],[])
        self.assertGreater(len(check(self.root,True)[0]),0)
    def test_second_queue_owner_is_rejected(self):
        path=self.root/'config/system.json';c=json.loads(path.read_text());c['task_owner']='github_issues';c['repository']='owner/test';path.write_text(json.dumps(c))
        self.assertTrue(any('historisk' in x for x in check(self.root)[0]))
    def test_broken_route_is_rejected(self):
        path=self.root/'saker/README.md';path.write_text(path.read_text()+'\n[Feil](finnes-ikke.md)\n')
        self.assertTrue(any('brutt lenke' in x for x in check(self.root)[0]))
    def test_invalid_deadline_and_duplicate_are_rejected(self):
        task='\n## O001 Prøve\nEier: Tester\nStatus: aktiv\nMål: Levere\nNeste handling: Lese\nFerdig når: Lest\nKilde: Test\nFrist: 2026-02-30\nArbeidsdato: ingen\nKontrolldato: ingen\n'
        path=self.root/'arbeid/OPPGAVER.md';path.write_text(path.read_text()+task+task)
        errors=check(self.root)[0]
        self.assertTrue(any('ugyldig dato' in x for x in errors));self.assertTrue(any('Duplisert' in x for x in errors))
if __name__=='__main__':unittest.main()
