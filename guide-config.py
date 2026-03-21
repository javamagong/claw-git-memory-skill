#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git Memory 对话式配置引导
通过问答引导用户完成配置
"""

import sys
import os
from pathlib import Path

# 添加库路径
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from git_memory import GitMemorySkill


def print_slow(text: str, delay: float = 0.02):
    """逐字打印（模拟对话）"""
    import time
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def print_options(options: list):
    """打印选项"""
    print()
    for i, option in enumerate(options, 1):
        print(f"  {i}) {option}")
    print()


def get_choice(options: list, default: int = 1) -> int:
    """获取用户选择"""
    while True:
        try:
            choice = input(f"请选择 [{default}]: ").strip()
            if not choice:
                return default
            choice = int(choice)
            if 1 <= choice <= len(options):
                return choice
            print(f"请输入 1-{len(options)} 之间的数字")
        except ValueError:
            print("请输入数字")


def get_input(prompt: str, default: str = None) -> str:
    """获取用户输入"""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()


def check_installation(skill: GitMemorySkill) -> bool:
    """检查安装状态"""
    # 检查配置文件
    config_path = skill.repo_path / 'config' / 'git-memory.yaml'
    if not config_path.exists():
        return False
    
    # 检查 Hooks
    hooks_dir = skill.repo_path / '.openclaw' / 'hooks'
    if not hooks_dir.exists():
        return False
    
    return True


def configure_scenario(skill: GitMemorySkill):
    """配置使用场景"""
    print("\n" + "="*60)
    print("  🫡 Git Memory 配置向导")
    print("="*60 + "\n")
    
    # 检查安装
    print_slow("正在检查安装状态...")
    if not check_installation(skill):
        print("❌ Git Memory Skill 还未安装")
        print("\n请先安装：")
        print("   bash skills/git-memory/quick-install.sh")
        return False
    
    print("✅ Git Memory 已安装\n")
    
    # 了解使用场景
    print_slow("你打算如何使用 Git Memory？")
    print_options([
        "单设备使用（就这一台电脑）",
        "云端 + 本地双设备同步",
        "只需要远程备份"
    ])
    
    scenario = get_choice([
        "single",
        "multi_device",
        "backup_only"
    ])
    
    # 根据场景配置
    if scenario == 1:
        # 单设备使用
        print("\n" + "="*60)
        print("  场景 1: 单设备使用")
        print("="*60 + "\n")
        
        print_slow("好的！已为你配置为单设备模式。")
        print()
        
        # 更新配置
        skill._update_config('remote.enabled', False)
        skill._update_config('multi_device.enabled', False)
        
        print("✅ 配置完成！")
        print()
        print("配置说明：")
        print("  - 记忆会自动保存到本地 Git 仓库")
        print("  - 可以随时查看历史版本")
        print("  - 不需要远程同步")
        print()
        print_slow("可以直接使用了！")
        
    elif scenario == 2:
        # 多设备同步
        print("\n" + "="*60)
        print("  场景 2: 云端 + 本地双设备同步")
        print("="*60 + "\n")
        
        print_slow("好的！需要先配置远程同步。")
        print()
        
        # 步骤 1：配置远程
        print("📦 需要创建一个 GitHub 私有仓库：")
        print()
        print("  1. 访问 https://github.com/new")
        print("  2. 创建私有仓库（名称如：openclaw-memory）")
        print("  3. 复制仓库地址")
        print()
        
        repo_url = get_input("GitHub 仓库地址")
        
        if not repo_url:
            print("⚠️  未提供仓库地址，配置已取消")
            return False
        
        print(f"\n🔗 配置远程仓库：{repo_url}")
        result = skill.enable_remote_sync(repo_url)
        
        if not result['success']:
            print(f"❌ 配置失败：{result.get('error', '未知错误')}")
            return False
        
        print(f"✅ {result['message']}")
        print()
        
        # 步骤 2：配置设备类型
        print_slow("这是哪个设备？")
        print_options([
            "local - 本地电脑（Mac/Windows/Linux）",
            "cloud - 云端服务器（vefaas/VPS）",
            "mobile - 移动设备"
        ])
        
        device_choice = get_choice(['local', 'cloud', 'mobile'])
        device_types = {1: 'local', 2: 'cloud', 3: 'mobile'}
        device_type = device_types[device_choice]
        
        device_name = get_input("设备名称", f"{device_type}-{os.uname().nodename()}")
        
        # 配置多设备同步
        result = skill.enable_multi_device_sync(device_type, device_name)
        
        if result['success']:
            print(f"\n✅ {result['message']}")
            print()
            print("配置说明：")
            print(f"  - 设备类型：{device_type}")
            print(f"  - 设备名称：{device_name}")
            print(f"  - 冲突解决：{result.get('conflict_resolution', 'auto')}")
            print()
            
            if device_type == 'local':
                print_slow("💡 提示：在云端设备上也配置，选择 cloud 类型。")
            elif device_type == 'cloud':
                print_slow("💡 提示：在本地设备上也配置，选择 local 类型。")
        else:
            print(f"❌ 配置失败：{result.get('error', '未知错误')}")
            return False
        
    elif scenario == 3:
        # 远程备份
        print("\n" + "="*60)
        print("  场景 3: 远程备份")
        print("="*60 + "\n")
        
        print_slow("好的！配置远程备份。")
        print()
        
        # 配置远程
        print("📦 GitHub 仓库地址：")
        repo_url = get_input("仓库地址（留空跳过）")
        
        if repo_url:
            result = skill.enable_remote_sync(repo_url)
            
            if result['success']:
                print(f"\n✅ {result['message']}")
                print()
                print("配置说明：")
                print("  - 记忆会自动推送到 GitHub")
                print("  - 不会启用多设备同步")
                print("  - 本地优先，不自动拉取远程")
                print()
                print_slow("适合只需要备份的场景！")
            else:
                print(f"❌ 配置失败：{result.get('error', '未知错误')}")
                return False
        else:
            print("ℹ️  跳过远程配置")
            return False
    
    print("\n" + "="*60)
    print("  ✅ 配置完成！")
    print("="*60 + "\n")
    
    print("下一步：")
    print("  1. 重启 OpenClaw：sh /workspace/projects/scripts/restart.sh")
    print("  2. 正常使用，记忆自动保存")
    print()
    print("查看配置：cat config/git-memory.yaml")
    print("查看状态：python3 -c \"from skills.git-memory.lib.git_memory import GitMemorySkill; GitMemorySkill('.').get_config()\"")
    print()
    
    return True


def main():
    """主函数"""
    try:
        # 初始化 Skill
        skill = GitMemorySkill('.')
        
        # 运行配置向导
        success = configure_scenario(skill)
        
        sys.exit(0 if success else 1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  配置已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
