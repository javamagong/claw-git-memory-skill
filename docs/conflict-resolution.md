# Conflict Resolution Guide

> How Git Memory handles multi-session conflicts

---

## When Conflicts Occur

Conflicts happen when:

1. **Multiple active sessions** modify the same memory file
2. **Divergent branches** can't auto-merge
3. **Schema mismatch** between local and remote

---

## Conflict Detection Flow

```
Session End
    ↓
Check for divergent branches
    ↓
┌─────────────────────────────┐
│ Can auto-merge?             │
├─────────────────────────────┤
│ YES → Apply schema merge    │
│ NO  → Prompt user           │
└─────────────────────────────┘
    ↓
Merge complete / User resolves
```

---

## Auto-Merge Strategies

Git Memory uses schema-driven merge based on `.mergerc.yaml`:

### Union Merge (for lists)
```yaml
transactions:
  merge_strategy: union
  id_fields: ['id']
```
**Behavior:** Combine all unique items by ID

### Deep Merge (for objects)
```yaml
holdings:
  merge_strategy: deep_merge
  key_field: 'symbol'
```
**Behavior:** Merge by key, update conflicting fields

### Local Preference
```yaml
context:
  merge_strategy: local
```
**Behavior:** Keep local version, discard incoming

---

## Manual Resolution

When auto-merge fails, you'll see a prompt:

```
⚠️ Memory Conflict Detected

File: subsystems/trading/holdings.json

Local (your changes):
  - 002149: 100 shares @ ¥44.69

Incoming (other session):
  - 002149: 200 shares @ ¥44.50
  - 600320: 500 shares @ ¥5.03

Choose action:
  [1] Accept incoming changes
  [2] Keep local changes
  [3] Manual merge (open editor)
  [4] Abort merge
```

### Option 1: Accept Incoming

```bash
git-memory resolve --accept-incoming
```

**Use when:** Other session has more recent/correct data

### Option 2: Keep Local

```bash
git-memory resolve --keep-local
```

**Use when:** Your changes are more accurate

### Option 3: Manual Merge

```bash
git-memory resolve --manual
```

Opens your editor to manually combine changes.

### Option 4: Abort

```bash
git-memory resolve --abort
```

Cancels the merge, keeps both branches separate.

---

## Prevention Strategies

### 1. Short-Lived Sessions

Keep sessions focused and brief to reduce overlap.

### 2. Sync Before Major Changes

```bash
git-memory pull  # Get latest before editing
```

### 3. Use Subsystems

Separate concerns into different subsystems:
- Trading → `subsystems/trading/`
- Preferences → `subsystems/conversation/`

Less overlap = fewer conflicts.

### 4. Enable Auto-Push

```yaml
# In TOOLS.md
git-memory:
  auto-push: true  # Push after each session
```

Keeps remote up-to-date for other devices.

---

## Advanced: Custom Merge Hooks

Create a merge hook for complex logic:

```bash
# subsystems/trading/merge-hook.py
#!/usr/bin/env python3

def merge(local, incoming):
    # Custom merge logic
    if local['cost'] != incoming['cost']:
        # Use weighted average
        return {'cost': (local['cost'] + incoming['cost']) / 2}
    return incoming
```

Configure in `.mergerc.yaml`:
```yaml
holdings:
  merge_strategy: custom
  hook: merge-hook.py
```

---

## Debugging

### View Divergent Branches

```bash
git branch --all
git log --graph --oneline --all
```

### Check Merge Status

```bash
python3 -c "
from git_memory import GitMemorySkill
skill = GitMemorySkill('.')
print(skill.get_merge_status())
"
```

### Force Reset (Last Resort)

```bash
# Discard all local changes
git reset --hard origin/main

# Warning: This deletes uncommitted memory!
```

---

## Examples

### Example 1: Two Sessions, Same Stock

**Session A:** Buys 100 shares of 002149 @ ¥44.69
**Session B:** Sells 50 shares of 002149 @ ¥45.00

**Auto-Merge Result:**
```json
{
  "symbol": "002149",
  "quantity": 50,
  "cost": 44.69,
  "transactions": [
    {"type": "buy", "qty": 100, "price": 44.69},
    {"type": "sell", "qty": 50, "price": 45.00}
  ]
}
```

### Example 2: Conflicting User Preferences

**Session A:** Sets TTS voice to "Nova"
**Session B:** Sets TTS voice to "Echo"

**Resolution:** Prompt user (can't auto-merge scalar values)

---

## FAQ

### Q: How often do conflicts occur?

**A:** Rarely! Most memory changes are to different files/fields.

### Q: Can I disable auto-merge?

**A:** Yes, set `auto-merge: false` in TOOLS.md config.

### Q: What if I choose wrong?

**A:** No worries! All versions are in Git history, recoverable anytime.

---

*Last updated: 2026-03-22*
