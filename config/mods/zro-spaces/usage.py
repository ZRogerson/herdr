"""Read local usage metrics only; never return conversation text or credentials."""
import json, math, sqlite3, sys
from pathlib import Path
from datetime import datetime, timezone

def pct(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and 0 <= value <= 100 else None

def select_thread(rows, agent):
    title = agent.get('title') or ''
    cwd = agent.get('cwd')
    matches = [r for r in rows if r['cwd'] == cwd and any(n and (title == n or title.endswith(' '+n) or (' '+n+' | ') in (' '+title+' ')) for n in [r['name'], r['title']])]
    if len(matches) == 1: return matches[0]
    # Resumed or duplicated sessions can retain the same title and folder.
    # Prefer the uniquely most recently updated match; never break a tie arbitrarily.
    if not matches: return None
    latest = max(r['updated_at'] for r in matches)
    newest = [r for r in matches if r['updated_at'] == latest]
    return newest[0] if len(newest) == 1 else None

def codex_usage(path):
    with open(path, 'rb') as f:
        size=f.seek(0,2); f.seek(max(0,size-1024*1024))
        lines=f.read().splitlines()
    for line in reversed(lines):
        try: event=json.loads(line)
        except (ValueError, UnicodeDecodeError): continue
        payload=event.get('payload') or {}
        if event.get('type') != 'event_msg' or payload.get('type') != 'token_count': continue
        info=payload.get('info') or {}
        window=info.get('model_context_window')
        used=(info.get('last_token_usage') or {}).get('total_tokens')
        hp=pct(max(0,100*(1-used/window))) if isinstance(window,(int,float)) and window>0 and isinstance(used,(int,float)) and used>=0 else None
        rate=(payload.get('rate_limits') or {}).get('primary') or {}
        used_pct=pct(rate.get('used_percent'))
        reset=rate.get('resets_at')
        mp=100-used_pct if used_pct is not None and (not reset or reset>datetime.now(timezone.utc).timestamp()) else None
        minutes=rate.get('window_minutes')
        return {'hp': hp, 'mp':mp, 'updatedAt':datetime.fromisoformat(event['timestamp'].replace('Z','+00:00')).timestamp(), 'mpLabel':f'{minutes:g}-minute usage allowance remaining' if isinstance(minutes,(int,float)) else 'Usage allowance remaining (not reported by this account)'}
    return None

def claude_usage(agent, root):
    pid = agent.get('pid')
    if not isinstance(pid, int) or isinstance(pid, bool): return None
    records = []
    for path in (root/'data/spaces-with-agents/claude-usage').glob('*.json'):
        try:
            data = json.loads(path.read_text())
            if pid in data.get('ancestorPids', []) and isinstance(data.get('updatedAt'), (int, float)):
                records.append(data)
        except (OSError, ValueError, TypeError): continue
    if not records: return None
    data = max(records, key=lambda d: d['updatedAt'])
    reset = data.get('mpResetsAt')
    mp = pct(data.get('mp'))
    if isinstance(reset, (int, float)) and reset <= datetime.now(timezone.utc).timestamp(): mp = None
    return {'hp': pct(data.get('hp')), 'mp': mp, 'updatedAt': data['updatedAt'], 'model': data.get('model'), 'mpLabel': data.get('mpLabel')}

def collect(agents, root):
    result={}
    rows=[]
    dbs=sorted((Path.home()/'.codex').glob('state_*.sqlite'),key=lambda p:p.stat().st_mtime,reverse=True)
    if dbs:
        try:
            with sqlite3.connect(f'file:{dbs[0]}?mode=ro',uri=True) as c:
                c.row_factory=sqlite3.Row
                rows=c.execute('select cwd,name,title,model,rollout_path,updated_at from threads where archived=0').fetchall()
        except sqlite3.Error: pass
    for a in agents:
        address=a['address']
        if '/' in address: continue
        try:
            if a.get('app')=='codex':
                row=select_thread(rows,a)
                if row:
                    result[address]=codex_usage(row['rollout_path']) or {}
                    result[address]['model']=row['model']
            elif a.get('app') in ('claude', 'claude-code'):
                data=claude_usage(a, root)
                if data is not None: result[address]=data
            else:
                p=root/'data/traveler/sessions'/f'{address}.json'
                if p.exists():
                    d=json.loads(p.read_text())
                    result[address]={'hp':pct(d.get('contextRemainingPct')), 'mp':pct(d.get('fiveHourRemainingPct')), 'updatedAt':d.get('updatedAt'), 'mpLabel':'Five-hour usage allowance remaining', 'model':d.get('model')}
        except (OSError,ValueError,TypeError,KeyError): pass
    return result

if __name__=='__main__':
    print(json.dumps(collect(json.loads(sys.argv[1]),Path(sys.argv[2]))))
