#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git Memory Skill - 核心功能测试
"""

import sys
import os
import json
from pathlib import Path

# 添加库路径
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from git_memory.merger import SchemaDrivenMerger
from git_memory.formatter import CommitFormatter
from git_memory.lock import CrossPlatformLock, FineGrainedLockManager


def test_schema_driven_merge():
    """测试 Schema-Driven Merge"""
    print("\n" + "="*60)
    print("🧪 测试 Schema-Driven Merge")
    print("="*60)
    
    merger = SchemaDrivenMerger()
    
    # 测试数据
    base = {
        'transactions': [
            {'transaction_id': '1', 'stock': 'AAPL', 'action': 'BUY', 'quantity': 100}
        ],
        'count': 10,
        'last_updated': '2026-03-19T10:00:00'
    }
    
    remote = {
        'transactions': [
            {'transaction_id': '1', 'stock': 'AAPL', 'action': 'BUY', 'quantity': 100},
            {'transaction_id': '2', 'stock': 'TSLA', 'action': 'SELL', 'quantity': 50}
        ],
        'count': 15,
        'last_updated': '2026-03-19T11:00:00'
    }
    
    local = {
        'transactions': [
            {'transaction_id': '1', 'stock': 'AAPL', 'action': 'BUY', 'quantity': 100},
            {'transaction_id': '3', 'stock': 'MSFT', 'action': 'BUY', 'quantity': 200}
        ],
        'count': 12,
        'last_updated': '2026-03-19T12:00:00'
    }
    
    # 创建临时 schema 文件
    test_dir = Path('/tmp/test-merger')
    test_dir.mkdir(exist_ok=True)
    
    schema_file = test_dir / '.mergerc.yaml'
    schema_file.write_text("""
version: 1
fields:
  transactions:
    type: array
    merge_strategy: union
    id_fields: ['transaction_id']
    dedup: true
  
  count:
    type: scalar
    merge_strategy: max
  
  last_updated:
    type: scalar
    merge_strategy: latest
    key: 'last_updated'

_default:
  merge_strategy: local
""")
    
    # 执行合并
    result = merger.merge(str(test_dir), base, remote, local)
    
    print("\n✅ 合并结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 验证
    assert len(result['transactions']) == 3, "交易记录应该是 3 条（并集）"
    assert result['count'] == 15, "count 应该取最大值 15"
    assert result['last_updated'] == '2026-03-19T12:00:00', "应该取最新时间"
    
    print("\n✅ Schema-Driven Merge 测试通过！")
    return True


def test_commit_formatter():
    """测试 Commit Formatter"""
    print("\n" + "="*60)
    print("🧪 测试 Commit Formatter")
    print("="*60)
    
    formatter = CommitFormatter()
    
    # 测试交易记录
    commit_msg = formatter.format_trade(
        stock_code='AAPL',
        action='卖出',
        quantity=100,
        price=180.5,
        pnl=500,
        session_id='test123',
        agent_name='A 小二'
    )
    
    print("\n📝 交易记录 Commit:")
    print(commit_msg)
    
    # 解析验证
    parsed = formatter.parse(commit_msg)
    
    assert parsed['type'] == 'trade', "类型应该是 trade"
    assert parsed['subsystem'] == 'trading', "子系统应该是 trading"
    assert 'AAPL' in parsed['summary'], "摘要应该包含 AAPL"
    assert parsed['metadata']['session'] == 'test123', "session_id 应该正确"
    
    print("\n✅ Commit Formatter 测试通过！")
    return True


def test_lock_manager():
    """测试锁管理器"""
    print("\n" + "="*60)
    print("🧪 测试 Lock Manager")
    print("="*60)
    
    test_lock_dir = Path('/tmp/test-locks')
    test_lock_dir.mkdir(exist_ok=True)
    
    lock_mgr = FineGrainedLockManager(str(test_lock_dir), max_wait=5)
    
    # 测试细粒度锁
    print("\n🔐 测试子系统锁...")
    
    with lock_mgr.acquire_subsystem_lock('trading'):
        print("✅ trading 锁已获取")
        
        # 尝试获取同一个锁（应该阻塞）
        import threading
        import time
        
        lock_acquired = [False]
        
        def try_acquire():
            try:
                with lock_mgr.acquire_subsystem_lock('trading'):
                    lock_acquired[0] = True
            except:
                pass
        
        thread = threading.Thread(target=try_acquire)
        thread.start()
        time.sleep(0.5)
        
        # 锁被占用，线程应该还在等待
        assert not lock_acquired[0], "锁应该被占用"
    
    # 释放后，线程应该能获取
    time.sleep(1)
    print("✅ 锁已释放，其他线程可以获取")
    
    # 测试不同子系统锁（应该并行）
    print("\n🔐 测试并行锁...")
    
    with lock_mgr.acquire_subsystem_lock('trading'):
        with lock_mgr.acquire_subsystem_lock('conversation'):
            print("✅ trading 和 conversation 锁可以同时获取（并行）")
    
    print("\n✅ Lock Manager 测试通过！")
    return True


def test_git_search():
    """测试 Git 检索"""
    print("\n" + "="*60)
    print("🧪 测试 Git 检索")
    print("="*60)
    
    from git_memory.tools import GitMemorySearcher
    
    repo_path = Path(__file__).parent
    searcher = GitMemorySearcher(str(repo_path))
    
    # 测试搜索
    print("\n🔍 搜索最近的 commit...")
    results = searcher.search(limit=5)
    
    print(f"✅ 找到 {results['count']} 条记录")
    
    if results['count'] > 0:
        print("\n最近提交:")
        for commit in results['results']:
            print(f"  - {commit['commit_id'][:7]}: {commit['message']}")
    
    # 测试统计
    print("\n📊 获取统计信息...")
    stats = searcher.get_stats()
    print(f"  总 commit 数：{stats['total_commits']}")
    print(f"  存储大小：{stats['storage_size']}")
    
    print("\n✅ Git 检索测试通过！")
    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("🚀 Git Memory Skill - 核心功能测试")
    print("="*60)
    
    tests = [
        ("Schema-Driven Merge", test_schema_driven_merge),
        ("Commit Formatter", test_commit_formatter),
        ("Lock Manager", test_lock_manager),
        ("Git 检索", test_git_search),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"\n❌ {name} 测试失败：{e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    # 总结
    print("\n" + "="*60)
    print("📊 测试结果")
    print("="*60)
    print(f"✅ 通过：{passed}/{len(tests)}")
    print(f"❌ 失败：{failed}/{len(tests)}")
    
    if failed == 0:
        print("\n🎉 所有测试通过！")
        return True
    else:
        print(f"\n⚠️  {failed} 个测试失败")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
