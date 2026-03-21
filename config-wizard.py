#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git Memory 多设备同步配置向导
"""

import sys
import os
from pathlib import Path

# 添加库路径
sys.path.insert(0, str(Path(__file__).parent / 'skills' / 'git-memory' / 'lib'))

from git_memory.sync_manager import SyncManager


def print_header(text: str):
    """打印标题"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def print_step(step: int, text: str):
    """打印步骤"""
    print(f"\n📍 步骤 {step}: {text}\n")


def input_with_default(prompt: str, default: str = None) -> str:
    """带默认值的输入"""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()


def main():
    """配置向导主函数"""
    print_header("🫡 Git Memory 配置向导")
    
    # 检测当前目录
    repo_path = Path.cwd()
    print(f"📁 检测到工作目录：{repo_path}")
    
    if not (repo_path / '.git').exists():
        print("❌ 当前目录不是 Git 仓库")
        print("   请先执行：git init")
        sys.exit(1)
    
    # 初始化同步管理器
    sync_mgr = SyncManager(str(repo_path))
    
    # 步骤 1: 是否启用远程同步
    print_step(1, "启用远程同步？（可选）")
    print("   远程同步功能：")
    print("   - 多设备自动同步记忆")
    print("   - GitHub/GitLab 备份")
    print("   - 云端 + 本地协作")
    print("")
    print("   ℹ️  不启用也能用！本地版本控制完全正常")
    print("")
    
    enable_remote = input_with_default("是否启用远程同步？(y/n)", "n").lower() == 'y'
    
    remote_enabled = False
    remote_url = ""
    
    if enable_remote:
        print("\n📦 在 GitHub/GitLab 创建私有仓库后，输入仓库地址")
        print("   格式：git@github.com:username/repo.git")
        print("   或：https://github.com/username/repo.git")
        
        remote_url = input_with_default("远程仓库地址", "").strip()
        
        if remote_url:
            print(f"\n🔗 配置远程仓库：{remote_url}")
            result = sync_mgr.configure_remote(remote_url)
            
            if result['success']:
                print(f"✅ {result['message']}")
                remote_enabled = True
            else:
                print(f"❌ 配置失败：{result.get('error', '未知错误')}")
                print("   可以稍后手动配置：git remote add origin <url>")
                print("   继续本地配置...")
        else:
            print("ℹ️  跳过远程配置")
    else:
        print("ℹ️  不启用远程同步，使用本地版本控制")
    
    # 步骤 2: 是否启用多设备同步
    multi_device_enabled = False
    device_type = "local"
    device_name = sync_mgr.device_name
    sync_start = True
    sync_end = True
    conflict_resolution = "auto"
    
    if remote_enabled:
        print_step(2, "启用多设备同步？（可选）")
        print("   多设备同步功能：")
        print("   - 自动识别设备（云端/本地）")
        print("   - 智能冲突解决")
        print("   - 设备标识记录")
        print("")
        
        enable_multi = input_with_default("是否启用多设备同步？(y/n)", "y").lower() == 'y'
        
        if enable_multi:
            multi_device_enabled = True
            
            # 设备类型
            print("\n选择设备类型：")
            print("   1) local  - 本地电脑（Mac/Windows/Linux）")
            print("   2) cloud  - 云端服务器（vefaas/VPS）")
            print("   3) mobile - 移动设备")
            
            device_input = input_with_default("请选择", "1")
            device_choices = {'1': 'local', '2': 'cloud', '3': 'mobile'}
            device_type = device_choices.get(device_input, 'local')
            print(f"✅ 设备类型：{device_type}")
            
            # 设备名称
            default_name = f"{device_type}-{device_name[:20]}"
            device_name = input_with_default("设备名称", default_name)
            print(f"✅ 设备名称：{device_name}")
            
            # 同步选项
            print("\n自动同步选项：")
            sync_start = input_with_default("会话开始自动拉取？(y/n)", "y").lower() == 'y'
            sync_end = input_with_default("会话结束自动推送？(y/n)", "y").lower() == 'y'
            
            # 冲突解决
            print("\n冲突解决策略：")
            print("   1) auto       - 自动尝试合并，失败时中止")
            print("   2) local_wins - 本地优先")
            print("   3) remote_wins - 远程优先")
            print("   4) manual     - 手动解决")
            
            conflict_input = input_with_default("请选择", "1")
            conflict_choices = {'1': 'auto', '2': 'local_wins', '3': 'remote_wins', '4': 'manual'}
            conflict_resolution = conflict_choices.get(conflict_input, 'auto')
        else:
            print("ℹ️  不启用多设备同步，使用基础远程同步")
    else:
        print("\n⚠️  多设备同步需要远程同步，已跳过")
    
    # 步骤 3: 保存配置
    print_step(3, "保存配置")
    
    # 更新配置
    sync_mgr.remote_enabled = remote_enabled
    sync_mgr.remote_url = remote_url
    sync_mgr.device_type = type('obj', (object,), {'value': device_type})()
    sync_mgr.device_name = device_name
    sync_mgr.sync_on_start = sync_start
    sync_mgr.sync_on_end = sync_end
    sync_mgr.conflict_resolution = type('obj', (object,), {'value': conflict_resolution})()
    
    # 保存到文件
    sync_mgr._save_config()
    print("✅ 配置已保存到：config/git-memory.yaml")
    
    # 步骤 4: 测试同步（如果配置了远程）
    if remote_enabled:
        print_step(4, "测试同步")
        
        test_sync = input_with_default("是否测试拉取？(y/n)", "y").lower() == 'y'
        
        if test_sync:
            print("\n📥 测试拉取...")
            result = sync_mgr.sync_on_session_start()
            
            if result['success']:
                print(f"✅ {result['message']}")
            else:
                print(f"⚠️  {result.get('message', '拉取失败')}")
                print("   可能原因：")
                print("   1. 远程仓库为空（需要先 git push）")
                print("   2. 网络连接问题")
                print("   3. SSH Key 未配置")
    
    # 完成
    print_header("✅ 配置完成！")
    
    print("\n📊 配置摘要:")
    print(f"   远程同步：{'✅ 已启用' if remote_enabled else '❌ 未启用'}")
    if remote_enabled:
        print(f"   远程地址：{remote_url}")
        print(f"   多设备同步：{'✅ 已启用' if multi_device_enabled else '❌ 未启用'}")
        if multi_device_enabled:
            print(f"   设备类型：{device_type}")
            print(f"   设备名称：{device_name}")
            print(f"   会话开始同步：{'✅' if sync_start else '❌'}")
            print(f"   会话结束同步：{'✅' if sync_end else '❌'}")
            print(f"   冲突解决：{conflict_resolution}")
    
    print("\n📝 下一步:")
    
    if not remote_enabled:
        print("   ✅ 配置完成！重启 OpenClaw 即可使用")
        print("   sh /workspace/projects/scripts/restart.sh")
        print("")
        print("   ℹ️  如需启用远程同步：")
        print("   1. 在 GitHub 创建私有仓库")
        print("   2. 运行此配置向导")
        print("   3. 输入仓库地址")
    else:
        if not remote_url:
            print("   1. 在 GitHub 创建私有仓库")
            print("   2. 配置远程：git remote add origin <url>")
            print("   3. 首次推送：git push -u origin main")
        else:
            print("   1. 重启 OpenClaw 生效")
            print("   sh /workspace/projects/scripts/restart.sh")
            print("")
            print("   2. 正常使用，记忆自动同步")
            print("")
            print("   3. 本地 Mac 部署：")
            print("   git clone <repo> ~/openclaw-local")
            print("   cd ~/openclaw-local")
            print("   python3 skills/git-memory/config-wizard.py")
    
    print("\n📖 查看配置：cat config/git-memory.yaml")
    print("📖 查看日志：tail -f logs/git-memory.log")
    print("📖 用户指南：GIT_MEMORY_USER_GUIDE.md")
    print("")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  配置已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
