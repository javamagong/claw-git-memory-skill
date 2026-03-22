# Subsystems Guide

> Detailed documentation for Git Memory subsystems

---

## Overview

Subsystems are specialized memory directories for different domains. Each subsystem:

- Has its own Git branch namespace
- Can have custom merge strategies (`.mergerc.yaml`)
- Is independently queryable
- Maintains schema consistency

---

## Available Subsystems

### 1. Trading (`subsystems/trading/`)

**Purpose:** Stock trading records, holdings, and P/L tracking

**Files:**
- `holdings.json` - Current positions (symbol, cost, quantity)
- `transactions.json` - Buy/sell history with timestamps
- `summary.json` - Realized/unrealized P/L, total portfolio value

**Schema Example:**
```json
{
  "holdings": [
    {"symbol": "002149", "name": "西部材料", "cost": 44.69, "quantity": 100}
  ],
  "transactions": [
    {"id": "txn_001", "symbol": "000547", "type": "sell", "price": 33.3, "quantity": 100}
  ]
}
```

**Merge Strategy:**
- `transactions`: Union by `id` field
- `holdings`: Deep merge by `symbol`

**Commands:**
```bash
# View trading history
git log -- subsystems/trading/

# Search for specific stock
git grep "002149" -- subsystems/trading/
```

---

### 2. Conversation (`subsystems/conversation/`)

**Purpose:** Long-running conversation context and user preferences

**Files:**
- `user_profile.json` - User info (name, timezone, preferences)
- `projects.json` - Active projects and their status
- `context.json` - Ongoing conversation threads

**Use Cases:**
- Remember user's name and how to address them
- Track project preferences across sessions
- Maintain context for multi-session tasks

---

### 3. Skills (`subsystems/skills/`)

**Purpose:** Learned skills, patterns, and workflows

**Files:**
- `tools.json` - Available tools and their usage
- `patterns.json` - Recurring solution patterns
- `learnings.json` - Lessons from past mistakes

**Example:**
```json
{
  "tools": {
    "weather": {"skill": "weather", "trigger": ["weather", "temperature"]},
    "stock": {"skill": "akshare-stock", "trigger": ["股票", "行情"]}
  }
}
```

---

### 4. Tools (`subsystems/tools/`)

**Purpose:** Environment-specific tool configuration

**Files:**
- `ssh_hosts.json` - SSH host aliases and details
- `cameras.json` - Camera names and locations
- `tts_voices.json` - TTS voice preferences
- `devices.json` - Smart home device names

**Example:**
```json
{
  "ssh_hosts": {
    "home-server": {"ip": "192.168.1.100", "user": "admin"}
  },
  "cameras": {
    "living-room": "Main area, 180° wide angle"
  }
}
```

---

## Querying Subsystems

### View History for One Subsystem

```bash
git log --oneline -- subsystems/trading/
```

### Search Within Subsystem

```bash
git grep "西部材料" -- subsystems/trading/
```

### Compare Versions

```bash
git diff HEAD~5 HEAD -- subsystems/trading/holdings.json
```

### Restore Old Version

```bash
git checkout <commit-hash> -- subsystems/trading/holdings.json
```

---

## Adding New Subsystems

1. Create directory:
```bash
mkdir -p subsystems/newsub/
```

2. Initialize with schema:
```bash
echo '{"version": 1}' > subsystems/newsub/schema.json
```

3. (Optional) Add merge config:
```bash
cat > subsystems/newsub/.mergerc.yaml <<EOF
version: 1
fields:
  items:
    merge_strategy: union
    id_fields: ['id']
EOF
```

4. Commit:
```bash
git add subsystems/newsub/
git commit -m "feat: Add newsub subsystem"
```

---

## Best Practices

1. **Keep schemas simple** - Flat JSON structures merge better
2. **Use unique IDs** - Every record should have an `id` field
3. **Document changes** - Commit messages should explain _why_
4. **Review merges** - Check conflict prompts before accepting

---

## Troubleshooting

### Subsystem Not Showing in History

```bash
# Check if files are tracked
git ls-files subsystems/trading/

# If empty, add them
git add subsystems/trading/
git commit -m "Add trading subsystem"
```

### Merge Conflicts in Subsystem

See [conflict-resolution.md](conflict-resolution.md)

---

*Last updated: 2026-03-22*
