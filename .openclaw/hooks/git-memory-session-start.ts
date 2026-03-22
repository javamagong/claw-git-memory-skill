#!/usr/bin/env node
/**
 * Git Memory Hook - Session Start
 * 
 * 在 OpenClaw 会话开始时自动拉取最新记忆
 */

import { execSync } from 'child_process';
import { existsSync } from 'fs';
import { join } from 'path';

interface HookContext {
  session_id: string;
  workspace: string;
  agent_id: string;
}

export async function onSessionStart(context: HookContext): Promise<void> {
  console.log('🫡 Git Memory: Session start hook triggered');
  
  const workspace = context.workspace || process.cwd();
  const gitDir = join(workspace, '.git');
  
  // 检查是否是 Git 仓库
  if (!existsSync(gitDir)) {
    console.log('⚠️  Git Memory: Not a git repository, skipping');
    return;
  }
  
  try {
    // 检查是否有远程仓库
    const hasRemote = execSync('git remote get-url origin', {
      cwd: workspace,
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'ignore']
    }).stdout.trim();
    
    if (hasRemote) {
      console.log('📥 Git Memory: Pulling latest memory from remote...');
      
      // 拉取远程最新记忆（不自动合并）
      execSync('git fetch origin', {
        cwd: workspace,
        stdio: ['ignore', 'pipe', 'pipe']
      });
      
      // 检查是否需要合并
      const localCommit = execSync('git rev-parse HEAD', {
        cwd: workspace,
        encoding: 'utf-8'
      }).stdout.trim();
      
      const remoteCommit = execSync('git rev-parse origin/main', {
        cwd: workspace,
        encoding: 'utf-8'
      }).stdout.trim();
      
      if (localCommit !== remoteCommit) {
        console.log(`🔄 Git Memory: Remote has changes (${localCommit.slice(0, 7)} → ${remoteCommit.slice(0, 7)})`);
        console.log('💡 Git Memory: Will merge on session end');
      } else {
        console.log('✅ Git Memory: Already up to date');
      }
    } else {
      console.log('ℹ️  Git Memory: No remote configured, local-only mode');
    }
  } catch (error: any) {
    console.log(`⚠️  Git Memory: Session start hook error: ${error.message}`);
  }
}

// OpenClaw Hook 导出
export default {
  name: 'git-memory-session-start',
  version: '2.0.0',
  description: 'Auto-pull latest memory on session start',
  trigger: 'session.start',
  handler: onSessionStart
};
