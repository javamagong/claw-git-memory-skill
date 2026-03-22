# Git Memory Hooks for OpenClaw

> Automatic memory versioning hooks for OpenClaw sessions

---

## Available Hooks

### 1. Session Start Hook

**File:** `git-memory-session-start.ts`

**Trigger:** `session.start`

**Actions:**
- Detects if workspace is a Git repository
- Checks for remote repository configuration
- Fetches latest changes from remote
- Reports if merge will be needed

### 2. Session End Hook

**File:** `git-memory-session-end.ts`

**Trigger:** `session.end`

**Actions:**
- Detects uncommitted changes
- Automatically stages all changes (`git add -A`)
- Creates commit with session metadata
- Pushes to remote repository (if configured)

---

## Installation

### Automatic (Recommended)

Run the quick install script:

```bash
bash skills/git-memory/quick-install.sh
```

The script will:
1. Detect OpenClaw installation
2. Copy hooks to OpenClaw hooks directory
3. Register hooks in OpenClaw configuration

### Manual Installation

1. Copy hooks to OpenClaw:
```bash
cp -r .openclaw/hooks/* /path/to/openclaw/.openclaw/hooks/
```

2. Restart OpenClaw:
```bash
openclaw gateway restart
```

---

## Configuration

Hooks respect the Git Memory configuration in `config/git-memory.yaml`:

```yaml
remote:
  enabled: true
  url: git@github.com:user/repo.git
  auto_push: true

auto_commit:
  enabled: true
  format: "session"  # session | timestamp | custom
```

---

## Troubleshooting

### Hook Not Triggering

1. Check if hooks are in the correct directory:
```bash
ls -la /path/to/openclaw/.openclaw/hooks/
```

2. Verify OpenClaw configuration:
```bash
cat /path/to/openclaw/config.yaml | grep -A 10 hooks
```

3. Check OpenClaw logs:
```bash
tail -f /path/to/openclaw/logs/openclaw.log | grep "git-memory"
```

### Push Failed

Common issues:
- SSH key not configured
- Remote repository doesn't exist
- Network connectivity issues

Check SSH configuration:
```bash
ssh -T git@github.com
```

---

## Development

### Testing Hooks Locally

```bash
# Test session start hook
node -e "
const hook = require('./git-memory-session-start.ts');
hook.onSessionStart({
  session_id: 'test-123',
  workspace: process.cwd(),
  agent_id: 'test-agent'
});
"
```

### Debug Mode

Set environment variable to enable verbose logging:

```bash
export GIT_MEMORY_DEBUG=1
```

---

## License

MIT License

---

*Version: 2.0.0 | Built by JavaMaGong & A 小二*
