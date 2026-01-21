#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Build script to create EXE using PyInstaller
构建脚本 - 创建 EXE 可执行程序
"""
import subprocess
import sys
import os

print("开始构建 EXE...")

# 确定输出目录
output_dir = r"C:\Users\admin\Desktop"
script = r"e:\VScodeProjects\videotestv.py"

# PyInstaller 命令
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",  # 单个可执行文件
    "--windowed",  # 隐藏控制台
    "--name=轻剪内测版",
    f"--distpath={output_dir}",
    "--specpath=.build",
    "--buildpath=.build",
    script
]

print(f"命令: {' '.join(cmd)}\n")

try:
    result = subprocess.run(cmd, cwd="e:\\VScodeProjects", timeout=300)
    
    if result.returncode == 0:
        exe_path = os.path.join(output_dir, "轻剪内测版.exe")
        if os.path.exists(exe_path):
            print(f"\n✓ 成功! EXE 已生成:")
            print(f"  位置: {exe_path}")
            print(f"  大小: {os.path.getsize(exe_path) / 1024 / 1024:.1f} MB")
        else:
            print(f"\n⚠ 构建成功但文件未找到")
    else:
        print(f"\n✗ 构建失败 (code {result.returncode})")
        
except Exception as e:
    print(f"✗ 错误: {e}")
