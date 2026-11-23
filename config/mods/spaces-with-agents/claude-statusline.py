"""Forward the existing status line and save only usage metadata for local cards."""
import json, math, os, re, subprocess, sys, tempfile, time
from pathlib import Path

def pct(value):
    return value if isinstance(value, (float, int)) and not isinstance(value, bool) and math.isfinite(value) and 0 <= value <= 100 else None

def metrics(data):
    context = data.get('context_window') or {}
    hp = pct(context.get('remaining_percentage'))
    used = pct(context.get('used_percentage'))
    if hp is None and used is not None:
        hp = 100 - used
    rate = (data.get('rate_limits') or {}).get('five_hour') or {}
    used_rate = pct(rate.get('used_percentage'))
    reset = rate.get('resets_at')
    mp = 100 - used_rate if used_rate is not None and (not reset or isinstance(reset, (int, float)) and reset > time.time()) else None
    model = data.get('model') or {}
    return {'hp': hp, 'mp': mp, 'mpResetsAt': reset, 'model': model.get('display_name') or model.get('id'), 'updatedAt': time.time(), 'mpLabel': 'Five-hour usage allowance remaining'}

def publish(data, root):
    sid = data.get('session_id')
    if not isinstance(sid, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,128}', sid):
        return
    # Snapshot ancestors once. No environment, prompts, or transcript content is saved.
    proc = subprocess.run(['ps', '-axo', 'pid=,ppid='], capture_output=True, text=True, timeout=2, check=True)
    parents = dict(tuple(map(int, line.split())) for line in proc.stdout.splitlines() if len(line.split()) == 2)
    ancestors = []; pid = os.getppid()
    while pid > 1 and pid not in ancestors and len(ancestors) < 32:
        ancestors.append(pid); pid = parents.get(pid, 0)
    record = metrics(data); record.update(sessionId=sid, ancestorPids=ancestors)
    root.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix='.usage-', dir=root)
    try:
        with os.fdopen(fd, 'w') as out: json.dump(record, out)
        os.replace(temp, root / (sid + '.json'))
    finally:
        if os.path.exists(temp): os.unlink(temp)

def main():
    raw = sys.stdin.buffer.read()
    try:
        root = Path(os.environ.get('HERDR_APP_HOME', str(Path.home()/'.config/herdr-app'))) / 'data/spaces-with-agents/claude-usage'
        publish(json.loads(raw), root)
    except (ValueError, TypeError, OSError, subprocess.SubprocessError):
        pass  # A metrics failure must not break the user's status line.
    return subprocess.run(['bash', str(Path.home()/'.claude/statusline-command.sh')], input=raw).returncode

if __name__ == '__main__':
    sys.exit(main())
