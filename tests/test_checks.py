"""Regresjoner for kontrakten, med små isolerte og nettverksfrie testrepoer."""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock
import json
import shutil
import subprocess
import sys
import unittest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'scripts'))
from checks import REQUIRED, budget_table, budgets, check, load_policy, size
from new_case import create
from preflight import preflight

POLICY = json.loads((REPO / 'config/context-budgets.json').read_text(encoding='utf-8'))
HUB = '# Prøvesak\n\nStatus: aktiv\nEier: Testperson\nSist oppdatert: 2026-10-19\nKildestatus: kontrollert\n'
TASK = '\n## O001 Prøve\nEier: Testperson\nStatus: aktiv\nMål: Levere\nNeste handling: Lese\nFerdig når: Lest\nKilde: Test\nFrist: 2026-11-12\nArbeidsdato: ingen\nKontrolldato: ingen\n'


class RepoTest(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(prefix='startpakke-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in REQUIRED:
            self.write(name, '# Test\n')
        self.policy = deepcopy(POLICY)
        self.write_policy()
        self.cfg = {'schema_version': 1, 'phase': 'pilot', 'owner': 'IKKE_AVKLART',
                    'original_home': 'IKKE_AVKLART', 'delivery_home': 'IKKE_AVKLART',
                    'access_confirmed': False, 'task_owner': 'markdown',
                    'repository': '', 'automation_enabled': False}
        self.write_config()
        self.write('CHATGPT-PROSJEKTINSTRUKS.md', 'Les CHATGPT-START.md.\n')
        self.write('arbeid/OPPGAVER.md', '# Oppgaver\n\nKøstatus: aktiv\n')
        self.write('maler/sak.md', HUB.replace('# Prøvesak', '# Navn på saken').replace('Status: aktiv', 'Status: utkast'))

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return path

    def append(self, name, content):
        path = self.root / name
        return self.write(name, path.read_text(encoding='utf-8') + content)

    def write_config(self):
        self.write('config/system.json', json.dumps(self.cfg))

    def write_policy(self):
        self.write('config/context-budgets.json', json.dumps(self.policy))
        self.write('docs/KONTEKSTSKALERING.md', budget_table(self.policy) + '\n')

    def errors(self, **kwargs):
        return check(self.root, **kwargs)['errors']

    def assert_error(self, phrase, **kwargs):
        errors = self.errors(**kwargs)
        self.assertTrue(any(phrase in error for error in errors), errors)

    def add_case(self, slug='prove'):
        self.write('saker/' + slug + '.md', HUB)
        self.append('saker/README.md', '\n[Prøvesak](' + slug + '.md)\n')


class BudgetTests(RepoTest):
    def measurement(self, kind, name=None):
        rows = budgets(self.root)['measurements']
        return next(row for row in rows if row['kind'] == kind and (name is None or row['name'] == name))

    def test_utf8_byte_count_and_crlf_normalization(self):
        path = self.root / 'context/START.md'
        path.write_bytes('æøå\r\nA\r\n'.encode('utf-8'))
        self.assertEqual(size(path), 9)
        self.assertEqual(self.measurement('warm')['bytes'], 9)
        path.write_bytes('æøå\nA\n'.encode('utf-8'))
        self.assertEqual(size(path), 9)

    def test_warning_and_greater_equal_block_boundaries(self):
        lim = self.policy['limits']['warm']
        for amount, expected in [(lim['warning'] - 1, 'ok'), (lim['warning'], 'warning'),
                                 (lim['block'] - 1, 'warning'), (lim['block'], 'blocked')]:
            with self.subTest(amount=amount):
                self.write('context/START.md', 'a' * amount)
                self.assertEqual(self.measurement('warm')['status'], expected)

    def test_strict_greater_boundary(self):
        limit = self.policy['limits']['agents']['block']
        self.write('AGENTS.md', 'a' * limit)
        self.assertEqual(self.measurement('agents')['status'], 'ok')
        self.append('AGENTS.md', 'a')
        self.assertEqual(self.measurement('agents')['status'], 'blocked')

    def test_dashboard_sums_three_files(self):
        self.write('context/START.md', 'a' * 5000)
        self.write('context/CURRENT.md', 'b' * 8000)
        self.write('context/PRIORITERINGER.md', 'c' * 6000)
        row = self.measurement('dashboard')
        self.assertEqual(row['bytes'], 19000)
        self.assertEqual(row['status'], 'blocked')

    def test_automatic_and_explicit_routes(self):
        self.write('context/START.md', 'a' * 5000)
        self.write('areas/prove.md', 'b' * 16600)
        self.assertEqual(self.measurement('route', 'START + areas/prove.md')['status'], 'blocked')
        self.write('arbeid/UKA.md', 'c' * 8300)
        self.write('arbeid/OPPGAVER.md', 'd' * 8300)
        self.assertEqual(self.measurement('route', 'Dagsvalg')['bytes'], 21600)
        self.assertEqual(self.measurement('route', 'Dagsvalg')['status'], 'blocked')

    def test_every_recursive_depth_file_is_measured_even_if_historical(self):
        self.write('saker/dybde/prove/eldre/2020.md', 'Status: historisk\n' + 'x' * 20000)
        self.write('saker/register/eldre/INDEX.md', 'x' * 16000)
        rows = {row['name']: row for row in budgets(self.root)['measurements']}
        self.assertEqual(rows['saker/dybde/prove/eldre/2020.md']['status'], 'blocked')
        self.assertEqual(rows['saker/register/eldre/INDEX.md']['status'], 'blocked')

    def test_missing_route_file_blocks(self):
        (self.root / 'arbeid/UKA.md').unlink()
        self.assertTrue(any('mangler fil' in error for error in budgets(self.root)['errors']))

    def test_instruction_limit_counts_characters_not_utf8_bytes(self):
        prefix = 'Les CHATGPT-START.md.\n'
        limit = self.policy['instruction_max_characters']
        self.write('CHATGPT-PROSJEKTINSTRUKS.md', prefix + 'ø' * (limit - len(prefix)))
        self.assertEqual(self.errors(), [])
        self.append('CHATGPT-PROSJEKTINSTRUKS.md', 'ø')
        self.assert_error('tegngrensen')

    def test_document_table_must_match_policy(self):
        self.append('docs/KONTEKSTSKALERING.md', '\nForklaring.\n')
        self.assertEqual(self.errors(), [])
        path = self.root / 'docs/KONTEKSTSKALERING.md'
        self.write('docs/KONTEKSTSKALERING.md', path.read_text(encoding='utf-8').replace('5 400', '5 399'))
        self.assert_error('budsjetttabell avviker')

    def test_invalid_policies_report_instead_of_crashing(self):
        invalid = [[], {'limits': []}]
        changes = [('limits', None), ('measurement', 'tokens'), ('schema_version', True),
                   ('instruction_max_characters', 0), ('extra_routes', [{}])]
        for key, value in changes:
            policy = deepcopy(self.policy); policy[key] = value; invalid.append(policy)
        for value in [None, [], {'block': True, 'label': 'Test'},
                      {'block': 10, 'warning': 10, 'label': 'Test'},
                      {'block': 10, 'absolute': 9, 'label': 'Test'},
                      {'block': 10, 'comparison': '=', 'label': 'Test'}]:
            policy = deepcopy(self.policy); policy['limits']['warm'] = value; invalid.append(policy)
        for route_files in [['context/START.md', {}], ['context/START.md', '../outside.md'],
                            ['context/START.md', 'context/START.md'], ['README.md']]:
            policy = deepcopy(self.policy)
            policy['extra_routes'] = [{'name': 'Test', 'files': route_files}]
            invalid.append(policy)
        for policy in invalid:
            with self.subTest(policy=policy):
                self.write('config/context-budgets.json', json.dumps(policy))
                self.assertTrue(budgets(self.root)['errors'])
                self.assert_error('Budsjettkonfigurasjon')


class StructureTests(RepoTest):
    def test_unconfigured_template_passes_structure_and_public_but_not_ready(self):
        self.assertEqual(self.errors(), [])
        self.assertEqual(self.errors(public=True), [])
        self.assert_error('Ikke avklart', ready=True)

    def test_recursive_registers_and_depth_reachability(self):
        self.write('saker/README.md', '[Gruppe](register/INDEX.md)\n')
        self.write('saker/register/INDEX.md', '[Neste](under/INDEX.md)\n')
        self.write('saker/register/under/INDEX.md', '[Sak](../../prove.md)\n')
        self.write('saker/prove.md', HUB + '\n[Dybde](dybde/prove/INDEX.md)\n')
        self.write('saker/dybde/prove/INDEX.md', '[Tema](tema/INDEX.md)\n')
        self.write('saker/dybde/prove/tema/INDEX.md', '[Detalj](detalj.md)\n')
        self.write('saker/dybde/prove/tema/detalj.md', HUB + '\n[Tilbake](../INDEX.md)\n')
        self.assertEqual(self.errors(), [])
        self.write('saker/register/INDEX.md', '# Brutt leserute\n')
        self.assert_error('Ikke nåbar fra register: saker/prove.md')
        self.assert_error('Foreldreløst underregister')
        self.write('saker/register/INDEX.md', '[Neste](under/INDEX.md)\n')
        self.write('saker/dybde/prove/INDEX.md', '# Brutt detaljrute\n')
        self.assert_error('Foreldreløs saksdybde: saker/dybde/prove/tema/detalj.md')

    def test_unrelated_link_does_not_hide_orphan(self):
        self.add_case()
        self.write('saker/README.md', '[Omvei](../docs/README.md)\n')
        self.write('docs/README.md', '[Sak](../saker/prove.md)\n')
        self.assert_error('Ikke nåbar fra register: saker/prove.md')

    def test_depth_needs_hub_and_root_index_route(self):
        self.write('saker/dybde/prove/INDEX.md', '# Indeks\n')
        self.assert_error('Dybde uten sakshub')
        self.add_case()
        self.assert_error('Hub peker ikke til rot-INDEX')
        (self.root / 'saker/dybde/prove/INDEX.md').unlink()
        self.assert_error('Dybde uten INDEX')

    def test_recursive_history_is_reachable_only_through_own_index(self):
        for family in ['context/historikk', 'context/revisjon', 'areas/historikk']:
            with self.subTest(family=family):
                self.write(family + '/INDEX.md', '[År](2025/INDEX.md)\n')
                self.write(family + '/2025/INDEX.md', '[Detalj](notat.md)\n')
                self.write(family + '/2025/notat.md', '# Historisk notat\n')
                self.assertEqual(self.errors(), [])
                self.write(family + '/INDEX.md', '# Frakoblet\n')
                self.assert_error('Foreldreløs historikk/revisjon: ' + family + '/2025/notat.md')
                self.write(family + '/INDEX.md', '[År](2025/INDEX.md)\n')

    def test_metadata_required_and_active_case_needs_real_date_and_owner(self):
        self.add_case()
        for name in ['Status', 'Eier', 'Sist oppdatert', 'Kildestatus']:
            with self.subTest(name=name):
                self.write('saker/prove.md', '\n'.join(line for line in HUB.splitlines() if not line.startswith(name + ':')))
                self.assert_error('mangler metadata ' + name)
        self.write('saker/prove.md', HUB.replace('2026-10-19', '2026-02-30').replace('Testperson', 'IKKE_AVKLART'))
        self.assert_error('ugyldig oppdateringsdato')
        self.assert_error('aktiv/historisk sak mangler eier')

    def test_link_routes_encoded_paths_and_fenced_examples(self):
        self.write('docs/øving.md', '# Øving\n')
        self.append('README.md', '\n[Øving](docs/%C3%B8ving.md)\n```md\n[Eksempel](finnes-ikke.md)\n```\n')
        self.assertEqual(self.errors(), [])
        self.append('README.md', '\n[Feil](docs/mangler.md)\n[Utenfor](../utenfor.md)\n')
        self.assert_error('brutt lenke')
        self.assert_error('lenke utenfor repo')

    def test_github_queue_demands_retired_markdown_queue(self):
        self.cfg.update(task_owner='github_issues', repository='example/arbeid')
        self.write_config()
        self.append('arbeid/OPPGAVER.md', '\nDet er ikke nok å nevne Køstatus: historisk her.\n')
        self.assert_error('Tekstkøen må være historisk')
        self.write('arbeid/OPPGAVER.md', '# Oppgaver\nKøstatus: historisk\n')
        self.assertEqual(self.errors(), [])
        self.cfg['repository'] = ''; self.write_config()
        self.assert_error('GitHub-kø krever eget repository')

    def test_task_dates_duplicate_ids_and_required_fields(self):
        self.append('arbeid/OPPGAVER.md', TASK)
        self.assertEqual(self.errors(), [])
        self.append('arbeid/OPPGAVER.md', TASK.replace('2026-11-12', '2026-02-30').replace('Eier: Testperson', 'Eier:'))
        self.assert_error('Duplisert oppgave-ID')
        self.assert_error('ugyldig dato i Frist')
        self.assert_error('mangler Eier')

    def test_ready_requires_config_receipt_and_existing_pilot(self):
        self.cfg.update(owner='Testperson', original_home='Avklart kilde', delivery_home='Avklart mappe', access_confirmed=True)
        self.write_config()
        self.assert_error('Oppstartskvittering', ready=True)
        self.write('context/OPPSTART.md', 'Status: bestått\nDato: 2026-10-19\nPilotsak: saker/prove.md\n')
        self.assert_error('faktisk pilotsak', ready=True)
        self.add_case()
        self.assertEqual(self.errors(ready=True), [])
        self.assert_error('tilpasset konfigurasjon', public=True)

    def test_secret_patterns_and_sensitive_file_types(self):
        for secret in ['gh' + 'p_' + 'A' * 36, 'github_' + 'pat_' + 'x' * 50,
                       'AK' + 'IA' + 'Z' * 16, '-----BEGIN ' + 'PRIVATE KEY-----']:
            with self.subTest(pattern=secret[:6]):
                self.write('prove.txt', secret)
                self.assert_error('Mulig autentiseringshemmelighet')
        (self.root / 'prove.txt').unlink()
        self.write('.env.example', 'EXAMPLE=placeholder\n')
        self.assertEqual(self.errors(), [])
        self.write('.env.local', 'EXAMPLE=placeholder\n')
        self.assert_error('Mulig hemmelighetsfil')

    def test_symlink_is_rejected_without_reading_target(self):
        path = self.root / 'context/START.md'; path.unlink()
        path.symlink_to(self.root.parent / 'does-not-exist')
        self.assert_error('Symbolsk lenke')
        self.assertTrue(any('Symbolsk lenke' in e for e in budgets(self.root)['errors']))

    def test_invalid_system_config_yields_usable_report(self):
        for content in ['{', '[]', '{"phase": [], "task_owner": []}']:
            with self.subTest(content=content):
                self.write('config/system.json', content)
                report = check(self.root)
                self.assertTrue(report['errors'])
                self.assertIn('claim', report)


class NewCaseTests(RepoTest):
    def test_creates_valid_case_and_repeat_never_overwrites(self):
        path = create(self.root, 'prove', 'Ny prøvesak')
        self.assertTrue(path.read_text(encoding='utf-8').startswith('# Ny prøvesak\n'))
        self.assertEqual(self.errors(), [])
        before = path.read_bytes(), (self.root / 'saker/README.md').read_bytes()
        with self.assertRaises(ValueError):
            create(self.root, 'prove', 'Endret tittel')
        self.assertEqual(before, (path.read_bytes(), (self.root / 'saker/README.md').read_bytes()))

    def test_bad_slug_title_and_template_do_not_modify_registry(self):
        before = (self.root / 'saker/README.md').read_bytes()
        for slug, title in [('../escape', 'Tittel'), ('Stor-bokstav', 'Tittel'), ('prove', 'To\nlinjer'), ('prove', '[Lenke]')]:
            with self.subTest(slug=slug, title=title), self.assertRaises(ValueError):
                create(self.root, slug, title)
        self.write('maler/sak.md', '# Uventet mal\n')
        with self.assertRaises(ValueError):
            create(self.root, 'prove', 'Tittel')
        self.assertEqual((self.root / 'saker/README.md').read_bytes(), before)
        self.assertFalse((self.root / 'saker/prove.md').exists())

    def test_concurrent_existing_file_is_not_deleted(self):
        target = self.root / 'saker/prove.md'
        real_open = Path.open

        def racing_open(path, mode='r', *args, **kwargs):
            if path == target and mode == 'x':
                with real_open(target, 'w', encoding='utf-8') as other:
                    other.write('Annen prosess sin sak\n')
                raise FileExistsError('Opprettet samtidig')
            return real_open(path, mode, *args, **kwargs)

        with mock.patch.object(Path, 'open', racing_open), self.assertRaises(FileExistsError):
            create(self.root, 'prove', 'Tittel')
        self.assertEqual(target.read_text(encoding='utf-8'), 'Annen prosess sin sak\n')

    def test_failed_registry_replace_keeps_original_and_removes_own_draft(self):
        before = (self.root / 'saker/README.md').read_bytes()
        with mock.patch.object(Path, 'replace', side_effect=OSError('Simulert diskfeil')):
            with self.assertRaises(OSError):
                create(self.root, 'prove', 'Tittel')
        self.assertEqual((self.root / 'saker/README.md').read_bytes(), before)
        self.assertFalse((self.root / 'saker/prove.md').exists())
        self.assertEqual(list((self.root / 'saker').glob('.new-case*')), [])

    def test_parallel_creation_lock_does_not_touch_existing_state(self):
        lock = self.write('saker/.new-case.lock', 'Annen prosess\n')
        before = (self.root / 'saker/README.md').read_bytes()
        with self.assertRaisesRegex(ValueError, 'allerede i gang'):
            create(self.root, 'prove', 'Tittel')
        self.assertEqual((self.root / 'saker/README.md').read_bytes(), before)
        self.assertTrue(lock.exists())
        self.assertFalse((self.root / 'saker/prove.md').exists())


class CommandLineTests(RepoTest):
    def run_script(self, script, *args):
        return subprocess.run([sys.executable, str(REPO / 'scripts' / script), '--root', str(self.root), *args], capture_output=True, text=True)

    def test_invalid_policy_still_returns_machine_readable_json(self):
        self.write('config/context-budgets.json', '[]')
        for script in ['budget.py', 'verify.py']:
            with self.subTest(script=script):
                result = self.run_script(script, '--json')
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertTrue(json.loads(result.stdout)['errors'])

    def test_write_docs_and_json_use_one_report_even_with_table_at_end(self):
        self.write('docs/KONTEKSTSKALERING.md', '# Grenser\n\n' + budget_table(self.policy))
        self.policy['limits']['warm']['warning'] -= 1
        self.write('config/context-budgets.json', json.dumps(self.policy))
        result = self.run_script('budget.py', '--write-docs', '--json')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['updated'], 'docs/KONTEKSTSKALERING.md')
        self.assertEqual(self.errors(), [])

    def test_missing_system_config_returns_failed_report_not_traceback(self):
        (self.root / 'config/system.json').unlink()
        result = self.run_script('verify.py', '--json')
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(json.loads(result.stdout)['status'], 'blocked')
        self.assertNotIn('Traceback', result.stderr)


@unittest.skipUnless(shutil.which('git'), 'Git kreves for kontroll av staged kandidat')
class PreflightTests(RepoTest):
    def setUp(self):
        super().setUp()
        shutil.copytree(REPO / 'scripts', self.root / 'scripts', ignore=shutil.ignore_patterns('__pycache__'))
        self.git('init', '-q')
        self.git('config', 'user.name', 'Lokal test')
        self.git('config', 'user.email', 'test@example.invalid')
        self.git('add', '.')
        self.git('commit', '-qm', 'Gyldig start')
        self.head = self.git('rev-parse', 'HEAD').strip()

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], stderr=subprocess.PIPE, text=True)

    def test_reports_staged_tree_and_ignores_unstaged_error(self):
        self.append('README.md', '\n[Ustaged feil](mangler.md)\n')
        report = preflight(self.root, self.head)
        self.assertEqual(report['status'], 'ok')
        self.assertEqual(report['head'], self.head)
        self.assertEqual(report['tree'], self.git('write-tree').strip())

    def test_staged_error_not_hidden_by_unstaged_fix(self):
        self.append('README.md', '\n[Staged feil](mangler.md)\n')
        self.git('add', 'README.md')
        self.write('README.md', '# Ustaged rettelse\n')
        report = preflight(self.root, self.head)
        self.assertEqual(report['status'], 'blocked')
        self.assertTrue(any('brutt lenke' in e for e in report['errors']))

    def test_stale_head_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'HEAD er endret'):
            preflight(self.root, '0' * 40)

    def test_staged_symlink_is_rejected(self):
        (self.root / 'ekstern').symlink_to('../utenfor')
        self.git('add', 'ekstern')
        with self.assertRaisesRegex(ValueError, 'ustøttet arkivpost'):
            preflight(self.root, self.head)

    def test_contradictory_candidate_exit_status_is_rejected(self):
        self.write('scripts/verify.py', 'import json,sys\nprint(json.dumps({"status":"ok","errors":[],"warnings":[]}))\nsys.exit(1)\n')
        self.git('add', 'scripts/verify.py')
        with self.assertRaisesRegex(ValueError, 'motstridende'):
            preflight(self.root, self.head)

    def test_changed_index_during_check_is_rejected(self):
        import preflight as module
        original_git = module.git
        calls = 0

        def changing_tree(root, *args):
            nonlocal calls
            if args == ('write-tree',):
                calls += 1
                if calls == 2:
                    return b'changed-tree\n'
            return original_git(root, *args)

        with mock.patch.object(module, 'git', changing_tree):
            with self.assertRaisesRegex(ValueError, 'indeks endret seg'):
                preflight(self.root, self.head)


if __name__ == '__main__':
    unittest.main()
