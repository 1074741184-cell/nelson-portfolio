#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI优化版本快速启动脚本
运行此脚本查看新的UI界面
"""

import sys
import os

# 确保在正确的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# 导入应用
from videotestv2 import NelsonBatchStitcher
import tkinter as tk

if __name__ == "__main__":
    print("=" * 50)
    print("🎨 奈尔森的一键剪辑 - UI优化版")
    print("=" * 50)
    print("\n📋 UI优化内容：")
    print("  ✅ 深蓝主题 (#0A0E27) - 替代旧的灰色")
    print("  ✅ 彩色强调 - 橙红/绿色/金色")
    print("  ✅ 按钮hover效果 - 变为橙红色")
    print("  ✅ 连接状态绿色反馈")
    print("  ✅ Section标题左橙红竖条")
    print("  ✅ 更大的主执行按钮 + 播放符号")
    print("  ✅ 混音标签添加emoji")
    print("  ✅ 整体间距和排版优化")
    print("\n💡 交互提示：")
    print("  • 试试移动鼠标到按钮上看hover效果")
    print("  • 选择文件后，标签会变绿色✔")
    print("  • 注意观察新的深蓝背景色")
    print("  • 头部有版本号和装饰emoji")
    print("=" * 50 + "\n")
    
    root = tk.Tk()
    app = NelsonBatchStitcher(root)
    root.mainloop()
