#!/usr/bin/env python3
"""
配置校验脚本 — 飞书多Agent群聊通信
用法：python scripts/validate_config.py

检查项：
1. 配置模板文件是否存在
2. 必填字段是否已替换（无占位符残留）
3. open_id 格式是否正确（ou_ 开头）
4. 群ID格式是否正确（oc_ 开头）
5. 是否有重复ID（复制粘贴易出错）
"""

import re
import sys
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent / "references" / "配置模板.yaml"

PLACEHOLDERS = [
    "ou_你的open_id",
    "oc_你的群ID",
    "你的bot_a名字",
    "你的bot_b名字",
    "你的群名",
]

def check_file_exists():
    if not CONFIG_FILE.exists():
        print(f"\u274c 错误：配置文件不存在")
        print(f"   路径：{CONFIG_FILE}")
        return False
    print(f"\u2705 配置文件存在：{CONFIG_FILE}")
    return True

def check_placeholders(content):
    found = [p for p in PLACEHOLDERS if p in content]
    if found:
        print(f"\u274c 错误：发现 {len(found)} 个未填写的占位符：")
        for p in found:
            print(f"   - {p}")
        print(f"\n\U0001f4a1 请打开 {CONFIG_FILE} 替换所有占位符为实际值")
        return False
    print("\u2705 所有必填字段已填写")
    return True

def check_id_formats(content):
    errors = []

    # 检查 open_id（ou_ 开头）
    ou_ids = re.findall(r'open_id:\s*"?([\w_]+)"?', content)
    for oid in ou_ids:
        if not oid.startswith("ou_"):
            errors.append(f"open_id 格式错误：{oid}（应以 ou_ 开头）")

    # 检查群ID（oc_ 开头）
    group_ids = re.findall(r'group_id:\s*"?([\w_]+)"?', content)
    for gid in group_ids:
        if not gid.startswith("oc_"):
            errors.append(f"group_id 格式错误：{gid}（应以 oc_ 开头）")

    if errors:
        print(f"\u274c 发现 {len(errors)} 个ID格式错误：")
        for e in errors:
            print(f"   - {e}")
        return False
    print("\u2705 所有ID格式正确")
    return True

def check_duplicate_ids(content):
    all_ous = re.findall(r'(ou_[\w]+)', content)
    count = {}
    for ou in all_ous:
        count[ou] = count.get(ou, 0) + 1
    duplicates = {k: v for k, v in count.items() if v > 1 and k != "ou_你的open_id"}
    if duplicates:
        print(f"\u26a0\ufe0f 警告：发现重复的 open_id：")
        for ou, c in duplicates.items():
            print(f"   - {ou} 出现 {c} 次")
        return True  # 只警告不阻断
    print("\u2705 无重复ID")
    return True

def main():
    print("=" * 50)
    print("飞书多Agent群聊通信 — 配置校验")
    print("=" * 50)
    print()

    if not check_file_exists():
        sys.exit(1)

    content = CONFIG_FILE.read_text(encoding="utf-8")

    results = [check_placeholders(content), check_id_formats(content)]
    check_duplicate_ids(content)

    print()
    print("=" * 50)
    if all(results):
        print("\u2705 配置校验通过！可以启动协作。")
        print()
        print("下一步：")
        print("1. 在飞书群里发送测试消息验证通信")
        print('   执行者名字 通信测试，请回复"收到"')
        sys.exit(0)
    else:
        print("\u274c 配置校验未通过，请修正后重新运行。")
        sys.exit(1)

if __name__ == "__main__":
    main()
