# Changelog

All notable changes to Git Memory Skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-04-10

### Added
- **Hermes Agent Support** - Full integration with Hermes memory provider system
- `gitmemory_status` tool - Check sync status, pending changes, branch info
- `gitmemory_commit` tool - Manual commit with auto-generated messages
- `gitmemory_push` tool - Push to remote repository
- `gitmemory_pull` tool - Pull latest from remote
- Auto-commit on session end for Hermes
- Auto-push on session end (configurable)
- Multi-device sync support (扣子云电脑 + 腾讯云 + OpenClaw)
- Unified memory repository structure (MEMORY.md, USER.md, SOUL.md, TOOLS.md)

### Changed
- README updated with Hermes installation instructions
- Architecture documentation now shows dual-platform support

### Technical
- Python provider implements `MemoryProvider` interface from Hermes
- Compatible with Hermes's built-in memory (MEMORY.md/USER.md)
- Hooks `on_memory_write` for auto-staging files
- Hooks `on_session_end` for auto-sync

## [2.0.0] - 2026-03-22

### Added
- Auto-trigger mechanism
- Subsystem memory (trading/conversation/skills/tools)
- Schema-Driven Merge for JSON conflicts
- Conflict detection and resolution
- Remote sync and multi-device support
- Bilingual documentation (EN/zh)
- OpenClaw Hook Integration
- Integration Guide

### Changed
- Major version upgrade with breaking changes
- Restructured memory directory layout

## [1.1.0] - 2026-03-21

### Added
- Conversation-style configuration wizard
- Multi-agent support
- Task group usage documentation

### Fixed
- Import errors in hooks

## [1.0.0] - 2026-03-19

### Added
- Initial release
- Git-based memory version control
- Basic OpenClaw integration
- Session start/end hooks
- Daily memory files
