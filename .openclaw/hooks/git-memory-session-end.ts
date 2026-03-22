#!/usr/bin/env node
/**
 * Git Memory Hook - Session End
 * 
 * 在 OpenClaw 会话结束时自动提交并推送记忆变更
 */

import { execSync } from 'child_process';
import { existsSync } from 'fs';
import { join } from 'path';

interface HookContext {
  session_id: string;
  workspace: string;
  agent_id: string;
  memory_changes?: string[];
}

export async function onSessionEnd(context: HookContext): Promise<void> {
  console.log('🫡 Git Memory: Session end hook triggered');
  
  const workspace = context.workspace || process.cwd();
  const gitDir = join(workspace, '.git');
  
  // 检查是否是 Git 仓库
  if (!existsSync(gitDir)) {
    console.log('⚠️  Git Memory: Not a git repository, skipping');
    return;
  }
  
  try {
    // 检查是否有未提交的变更
    const status = execSync('git status --porcelain', {
      cwd: workspace,
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'ignore']
    }).stdout.trim();
    
    if (!status) {
      console.log('✅ Git Memory: No uncommitted changes');
    } else {
      console.log('📝 Git Memory: Found uncommitted changes');
      
      // 获取变更文件列表
      const changedFiles = status.split('\n').map(line => line.trim().split(/\s+/)[1]);
      console.log(`   Changed files: ${changedFiles.join(', ')}`);
      
      // 自动提交
      const commitMsg = `feat(memory): Auto-commit session ${context.session_id.slice(0, 8)}\n\nAgent: ${context.agent_id}\nChanged files: ${changedFiles.join(', ')}`;
      
      execSync('git add -A', {
        cwd: workspace,
        stdio: ['ignore', 'pipe', 'pipe']
      });
      
      execSync(`git commit -m "${commitMsg}"`, {
        cwd: workspace,
        stdio: ['ignore', 'pipe', 'pipe']
      });
      
      console.log('✅ Git Memory: Changes committed');
    }
    
    // 检查远程并推送
    const hasRemote = execSync('git remote get-url origin', {
      cwd: workspace,
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'ignore']
    }).stdout.trim();
    
    if (hasRemote) {
      console.log('📤 Git Memory: Pushing to remote...');
      
      execSync('git push origin main', {
        cwd: workspace,
        stdio: ['ignore', 'pipe', 'pipe']
      });
      
      console.log('✅ Git Memory: Pushed successfully');
    } else {
      console.log('ℹ️  Git Memory: No remote configured');
    }
  } catch (error: any) {
    console.log(`⚠️  Git Memory: Session end hook error: ${error.message}`);
  }
}

// OpenClaw Hook 导出
export default {
  name: 'git-memory-session-end',
  version: '2.0.0',
  description: 'Auto-commit and push memory on session end',
  trigger: 'session.end',
  handler: onSessionEnd
};
