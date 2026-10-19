"""Pure checks shared by verify, budget and staged preflight. Python 3.10+."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import datetime as dt
import json
import re

IGNORED={'.git','.venv','node_modules','__pycache__'}
REQUIRED=['README.md','KOM-I-GANG.md','START-HER-KI.md','PROJECT.md','AGENTS.md','CHATGPT-PROSJEKTINSTRUKS.md','CHATGPT-START.md','context/START.md','context/README.md','context/PROFIL.md','context/KILDER.md','context/TILGANGER.md','context/CURRENT.md','context/PRIORITERINGER.md','context/SYSTEMSTATUS.md','context/OPPSTART.md','context/historikk/INDEX.md','context/revisjon/INDEX.md','areas/historikk/INDEX.md','saker/dybde/INDEX.md','saker/README.md','areas/README.md','arbeid/OPPGAVER.md','arbeid/UKA.md','config/system.json','config/context-budgets.json','docs/KONTEKSTSKALERING.md','docs/KONTEKSTFLYT.md','docs/KONTEKSTEIERSKAP.md','docs/SAKSSYSTEM.md','LICENSE']
TASK_STATUS={'avklaring','aktiv','planlagt','venter','parkert','fullført'}
LIMIT_KEYS={'warm','dashboard','route','registry','case_hub','depth','agents','chat_bootstrap','current','priorities'}
CLAIM='Lokal struktur og registrerte opplysninger; ikke originalkontroll, semantisk kompletthet eller prøvd ekstern tilgang.'

def text(path):return Path(path).read_text(encoding='utf-8').replace('\r\n','\n')
def size(path):return len(text(path).encode('utf-8'))
def field(content,name):
    m=re.search(r'^\s*(?:\*\*)?'+re.escape(name)+r':(?:\*\*)?[^\S\n]*([^\n]*)$',content,re.M|re.I)
    return m.group(1).strip() if m else ''
def valid_date(s):
    try:return bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}',s)) and bool(dt.date.fromisoformat(s))
    except ValueError:return False

def files(root):
    return sorted(p for p in root.rglob('*') if (p.is_file() or p.is_symlink()) and not any(x in IGNORED for x in p.relative_to(root).parts))
def inside(root,path):return path.resolve().is_relative_to(root.resolve())
def strip_code(s):return re.sub(r'```.*?```|~~~.*?~~~','',s,flags=re.S)
def local_links(root,p,content):
    result=[]
    for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',strip_code(content)):
        target=target.strip().split(' "',1)[0].strip('<>')
        parts=urlsplit(target)
        if parts.scheme or target.startswith('//'):continue
        result.append((p.parent/unquote(parts.path) if parts.path else p,unquote(parts.fragment),target))
    return result

def graph_target(p):
    if p.is_dir():
        for n in ['README.md','INDEX.md']:
            if (p/n).is_file():return (p/n).resolve()
    return p.resolve()
def reachable(graph,start,allowed):
    seen=set();todo=[start.resolve()]
    while todo:
        p=todo.pop()
        if p in seen or not allowed(p):continue
        seen.add(p);todo.extend(graph.get(p,set())-seen)
    return seen

def load_policy(root):
    policy=json.loads(text(root/'config/context-budgets.json'))
    if not isinstance(policy,dict):raise ValueError('Budsjettkonfigurasjon må være et objekt')
    if type(policy.get('schema_version')) is not int or policy['schema_version']!=1 or policy.get('measurement')!='utf8_lf':raise ValueError('Ukjent budsjettformat')
    limits=policy.get('limits',{})
    if not isinstance(limits,dict) or set(limits)!=LIMIT_KEYS:raise ValueError('Ufullstendig eller ukjent sett med budsjettklasser')
    for name,lim in limits.items():
        if not isinstance(lim,dict) or not isinstance(lim.get('label'),str) or not lim['label'].strip():raise ValueError('Ugyldig budsjettklasse: '+name)
        for k in ['warning','block','absolute']:
            if k in lim and (type(lim[k]) is not int or lim[k]<=0):raise ValueError('Ugyldig terskel: '+name+'/'+k)
        if 'block' not in lim:raise ValueError('Mangler blokkgrense: '+name)
        if lim.get('warning',0)>=lim['block'] or lim.get('absolute',lim['block']+1)<=lim['block']:raise ValueError('Feil terskelrekkefølge: '+name)
        if lim.get('comparison','>=') not in {'>=','>'}:raise ValueError('Ugyldig sammenligningsoperator')
    if type(policy.get('instruction_max_characters')) is not int or policy['instruction_max_characters']<=0:raise ValueError('Ugyldig instruksjonsgrense')
    if not isinstance(policy.get('extra_routes'),list):raise ValueError('extra_routes må være en liste')
    for route in policy['extra_routes']:
        if not isinstance(route,dict) or not route.get('name') or not route.get('files') or not isinstance(route['files'],list):raise ValueError('Ugyldig ekstra rute')
        if not isinstance(route['name'],str) or any(not isinstance(item,str) or not item.strip() for item in route['files']):raise ValueError('Rutenavn og filruter må være tekst')
        if len(route['files'])!=len(set(route['files'])):raise ValueError('Duplisert fil i ekstra rute')
        if 'context/START.md' not in route['files']:raise ValueError('Normalrute må inkludere START')
        for item in route['files']:
            if not isinstance(item,str) or not inside(root,root/item):raise ValueError('Rute utenfor repo')
    return policy

def budget_table(policy):
    rows=['| Klasse | Varsel | Blokkering | Absolutt | Regel |','| --- | ---: | ---: | ---: | --- |']
    fmt=lambda v:f'{v:,}'.replace(',',' ') if v is not None else '–'
    for lim in policy['limits'].values():
        rows.append(f"| {lim['label']} | {fmt(lim.get('warning'))} | {fmt(lim['block'])} | {fmt(lim.get('absolute'))} | {lim.get('comparison','>=')} byte |")
    rows.append(f"| Fast prosjektinstruks | – | {fmt(policy['instruction_max_characters'])} | – | > tegn |")
    return '\n'.join(rows)

def budgets(root,policy=None):
    root=Path(root).resolve();errors=[];warnings=[];measurements=[]
    symlinks=[p for p in files(root) if p.is_symlink()]
    if symlinks:return {'errors':['Symbolsk lenke krever egen håndtering: '+p.relative_to(root).as_posix() for p in symlinks],'warnings':[],'measurements':[]}
    try:policy=policy or load_policy(root)
    except (OSError,ValueError,TypeError,KeyError) as e:return {'errors':['Budsjettkonfigurasjon: '+str(e)],'warnings':[],'measurements':[]}
    def measure(kind,label,names):
        missing=[n for n in names if not (root/n).is_file()]
        if missing:errors.append('Budsjettrute mangler fil: '+', '.join(missing));return
        try:amount=sum(size(root/n) for n in names)
        except (OSError,UnicodeError) as e:errors.append('Uleselig budsjettrute '+label+': '+str(e));return
        lim=policy['limits'][kind]
        fail=amount>lim['block'] if lim.get('comparison','>=')=='>' else amount>=lim['block']
        status='blocked' if fail else 'warning' if amount>=lim.get('warning',float('inf')) else 'ok'
        measurements.append({'kind':kind,'name':label,'files':names,'bytes':amount,'status':status})
        if fail:errors.append(f"{label}: {amount} byte, blokkgrense {lim['block']} ({lim.get('comparison','>=')})")
        elif status=='warning':warnings.append(f"{label}: {amount} byte, varsel ved {lim['warning']}")
    for kind,name in [('warm','context/START.md'),('agents','AGENTS.md'),('chat_bootstrap','CHATGPT-START.md'),('current','context/CURRENT.md'),('priorities','context/PRIORITERINGER.md')]:measure(kind,name,[name])
    measure('dashboard','Arbeidsoversikt',['context/START.md','context/CURRENT.md','context/PRIORITERINGER.md'])
    for base in ['context','areas','saker']:
        for p in sorted((root/base).glob('*.md')):
            rel=p.relative_to(root).as_posix()
            if p.name in {'README.md','START.md','CURRENT.md','PRIORITERINGER.md'}:continue
            measure('route','START + '+rel,['context/START.md',rel])
            if base=='saker':measure('case_hub',rel,[rel])
    for p in files(root):
        rel=p.relative_to(root).as_posix()
        if p.suffix!='.md':continue
        if rel in ['saker/README.md','areas/README.md'] or rel.startswith(('saker/register/','areas/register/')):measure('registry',rel,[rel])
        elif rel.startswith(('saker/dybde/','areas/historikk/','context/historikk/','context/revisjon/','context/start/')):measure('depth',rel,[rel])
    for route in policy['extra_routes']:measure('route',route['name'],route['files'])
    return {'errors':errors,'warnings':warnings,'measurements':measurements}

def check(root,ready=False,public=False):
    root=Path(root).resolve();errors=[];warnings=[]
    symlinks=[p for p in files(root) if p.is_symlink()]
    if symlinks:return {'errors':['Symbolsk lenke krever egen håndtering: '+p.relative_to(root).as_posix() for p in symlinks],'warnings':[],'measurements':[],'claim':CLAIM}
    for name in REQUIRED:
        if not (root/name).is_file():errors.append('Mangler '+name)
    try:cfg=json.loads(text(root/'config/system.json'))
    except (OSError,ValueError) as e:return {'errors':errors+['Uleselig systemkonfigurasjon: '+str(e)],'warnings':warnings,'measurements':[],'claim':CLAIM}
    if not isinstance(cfg,dict):return {'errors':errors+['Systemkonfigurasjon må være et objekt'],'warnings':warnings,'measurements':[],'claim':CLAIM}
    if type(cfg.get('schema_version')) is not int or cfg['schema_version']!=1:errors.append('Ukjent system schema_version')
    if cfg.get('phase') not in ('pilot','active'):errors.append('phase må være pilot eller active')
    if cfg.get('task_owner') not in ('markdown','github_issues'):errors.append('Velg én gyldig task_owner')
    if cfg.get('automation_enabled') is not False:errors.append('Automatisering er ikke implementert i startmalen')
    if type(cfg.get('access_confirmed')) is not bool:errors.append('access_confirmed må være boolsk')
    for name in ['owner','original_home','delivery_home']:
        if not isinstance(cfg.get(name),str) or not cfg[name].strip() or cfg[name].strip()=='IKKE_AVKLART':(errors if ready else warnings).append('Ikke avklart: '+name)
    if cfg.get('access_confirmed') is not True:(errors if ready else warnings).append('Faktisk tilgang er ikke bekreftet')
    tasks=text(root/'arbeid/OPPGAVER.md') if (root/'arbeid/OPPGAVER.md').exists() else ''
    if cfg.get('task_owner')=='github_issues':
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',str(cfg.get('repository',''))):errors.append('GitHub-kø krever eget repository')
        if field(tasks,'Køstatus')!='historisk':errors.append('Tekstkøen må være historisk når Issues eier oppgavene')
    elif field(tasks,'Køstatus')!='aktiv':errors.append('Tekstkøen må være aktiv når markdown eier oppgavene')
    seen=set()
    for m in re.finditer(r'^## (O\d+) ([^\n]+)\n(.*?)(?=^## |\Z)',tasks,re.M|re.S):
        tid,_,body=m.groups()
        if tid in seen:errors.append('Duplisert oppgave-ID '+tid)
        seen.add(tid);status=field(body,'Status')
        if status not in TASK_STATUS:errors.append(tid+': ugyldig status')
        for name in ['Eier','Mål','Neste handling','Ferdig når','Kilde']:
            val=field(body,name)
            if not val or val=='IKKE_AVKLART' and status not in {'avklaring','parkert'}:errors.append(tid+': mangler '+name)
        for name in ['Frist','Arbeidsdato','Kontrolldato']:
            val=field(body,name)
            if val!='ingen' and not valid_date(val):errors.append(tid+': ugyldig dato i '+name)
    graph={};allfiles=files(root)
    for p in allfiles:
        rel=p.relative_to(root).as_posix()
        if p.is_symlink():errors.append('Symbolsk lenke krever egen håndtering: '+rel);continue
        if p.name=='.env' or p.name.startswith('.env.') and p.name!='.env.example' or p.suffix in {'.pem','.key'}:errors.append('Mulig hemmelighetsfil: '+rel)
        if p.suffix not in {'.md','.json','.py','.yml','.yaml','.txt','.html','.svg'} and p.name!='LICENSE':continue
        try:content=text(p)
        except (OSError,UnicodeError):errors.append('Uleselig tekstfil: '+rel);continue
        secret_patterns=[r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'gh[pousr]_[A-Za-z0-9]{30,}',r'github_pat_[A-Za-z0-9_]{40,}',r'AKIA[0-9A-Z]{16}']
        if any(re.search(pattern,content) for pattern in secret_patterns):errors.append('Mulig autentiseringshemmelighet: '+rel)
        if p.suffix!='.md':continue
        edges=set()
        for target,anchor,raw in local_links(root,p,content):
            if not inside(root,target):errors.append(rel+': lenke utenfor repo '+raw);continue
            if not target.exists():errors.append(rel+': brutt lenke '+raw);continue
            edges.add(graph_target(target))
        graph[p.resolve()]=edges
        parts=p.relative_to(root).parts
        is_hub=len(parts)==2 and parts[0] in {'saker','areas'} and p.name not in {'README.md','INDEX.md'}
        is_depth=rel.startswith('saker/dybde/') and p.name not in {'README.md','INDEX.md'}
        if is_hub or is_depth:
            for name in ['Status','Eier','Sist oppdatert','Kildestatus']:
                if not field(content,name):errors.append(rel+': mangler metadata '+name)
            if field(content,'Status') not in {'utkast','mal'}:
                if not valid_date(field(content,'Sist oppdatert')):errors.append(rel+': ugyldig oppdateringsdato')
                if field(content,'Eier')=='IKKE_AVKLART':errors.append(rel+': aktiv/historisk sak mangler eier')
    # Reachability remains inside each register family; an unrelated back-link cannot hide an orphan.
    for base in ['saker','areas']:
        start=root/base/'README.md'
        allowed=lambda p,b=base:inside(root/b,p) and (p.parent==root/b or 'register' in p.relative_to(root/b).parts)
        seenroutes=reachable(graph,start,allowed)
        for p in (root/base).glob('*.md'):
            if p.name not in {'README.md','INDEX.md'} and p.resolve() not in seenroutes:errors.append('Ikke nåbar fra register: '+p.relative_to(root).as_posix())
        for p in (root/base/'register').rglob('*.md'):
            if p.resolve() not in seenroutes:errors.append('Foreldreløst underregister: '+p.relative_to(root).as_posix())
    depthroot=root/'saker/dybde'
    if depthroot.exists():
        for folder in depthroot.iterdir():
            if not folder.is_dir():continue
            hub=root/'saker'/(folder.name+'.md');index=folder/'INDEX.md'
            if not hub.is_file():errors.append('Dybde uten sakshub: '+folder.name)
            if not index.is_file():errors.append('Dybde uten INDEX: '+folder.name)
            if index.resolve() not in graph.get(hub.resolve(),set()):errors.append('Hub peker ikke til rot-INDEX: '+folder.name)
            reached=reachable(graph,index,lambda p,f=folder:inside(f,p))
            for p in folder.rglob('*.md'):
                if p.resolve() not in reached:errors.append('Foreldreløs saksdybde: '+p.relative_to(root).as_posix())
        for p in depthroot.glob('*.md'):
            if p.name not in {'INDEX.md','README.md'}:errors.append('Saksdybde må ha egen saksmappe: '+p.name)
    for foldername in ['context/historikk','context/revisjon','areas/historikk']:
        folder=root/foldername;index=folder/'INDEX.md';reached=reachable(graph,index,lambda p,f=folder:inside(f,p))
        for p in folder.rglob('*.md'):
            if p.resolve() not in reached:errors.append('Foreldreløs historikk/revisjon: '+p.relative_to(root).as_posix())
    try:
        policy=load_policy(root);b=budgets(root,policy);errors.extend(b['errors']);warnings.extend(b['warnings'])
        documentation=text(root/'docs/KONTEKSTSKALERING.md')
        if budget_table(policy) not in documentation:errors.append('Dokumentert budsjetttabell avviker fra konfigurasjonen')
        instr=text(root/'CHATGPT-PROSJEKTINSTRUKS.md')
        if len(instr)>policy['instruction_max_characters']:errors.append('Prosjektinstruks overskrider tegngrensen')
        routes=re.findall(r'\b[A-Z][A-Z0-9-]*\.md\b',instr)
        if set(routes)!={'CHATGPT-START.md'}:errors.append('Prosjektinstruks skal bare peke til CHATGPT-START.md')
    except (OSError,ValueError,TypeError,KeyError) as e:errors.append('Budsjettkonfigurasjon: '+str(e));b={'measurements':[]}
    if ready:
        content=text(root/'context/OPPSTART.md') if (root/'context/OPPSTART.md').is_file() else ''
        if field(content,'Status')!='bestått' or not valid_date(field(content,'Dato')):errors.append('Oppstartskvittering er ikke bestått med gyldig dato')
        pilot=field(content,'Pilotsak')
        if not re.fullmatch(r'saker/[a-z0-9-]+\.md',pilot) or not (root/pilot).is_file():errors.append('Oppstartskvittering mangler faktisk pilotsak')
    if public:
        if cfg.get('phase')!='pilot' or any(cfg.get(k)!='IKKE_AVKLART' for k in ['owner','original_home','delivery_home']) or cfg.get('access_confirmed') is not False or cfg.get('repository')!='':errors.append('Distribusjonsmalen inneholder tilpasset konfigurasjon')
        if seen:errors.append('Distribusjonsmalen inneholder aktive personlige oppgaver')
        if any(p.name!='README.md' for p in (root/'saker').glob('*.md')):errors.append('Distribusjonsmalen inneholder egne saker')
    return {'errors':errors,'warnings':warnings,'measurements':b['measurements'],'claim':CLAIM}
