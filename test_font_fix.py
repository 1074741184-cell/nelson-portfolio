#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试系统字体方案是否有效
使用系统字体名称生成多个视频，验证字体是否真的改变
"""
import os
import subprocess
import sys

ffmpeg_exe = r"E:\VScodeProjects\ffmpeg.exe"
out_dir = r"C:\Users\admin\Desktop\测试用输出2"

# 清理旧文件
for f in os.listdir(out_dir):
    if "FontTest_" in f:
        try:
            os.remove(os.path.join(out_dir, f))
        except:
            pass

print("生成测试视频，每个用不同系统字体...\n")

# 常见 Windows 系统字体
test_fonts = [
    ("Impact", "Impact (粗体)"),
    ("Georgia", "Georgia (衬线)"),
    ("Arial", "Arial (无衬线)"),
    ("Calibri", "Calibri (现代)"),
]

success_count = 0

for font_name, description in test_fonts:
    out_file = os.path.join(out_dir, f"FontTest_{font_name}_{description.split('(')[1].rstrip(')')}.mp4")
    
    # drawtext 过滤器用 font 参数
    drawtext_filter = f"drawtext=font={font_name}:text='FONT TEST: {font_name}':fontsize=120:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2"
    
    cmd = [
        ffmpeg_exe, '-y',
        '-f', 'lavfi', '-i', 'color=c=black:s=1080x1920:d=2',
        '-vf', drawtext_filter,
        '-c:v', 'libx264', '-preset', 'fast',
        out_file
    ]
    
    print(f"生成: {description}...", end=' ')
    
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=30, errors='replace')
        if result.returncode == 0 and os.path.exists(out_file):
            size_mb = os.path.getsize(out_file) / 1024 / 1024
            print(f"OK ({size_mb:.1f} MB)")
            success_count += 1
        else:
            print(f"FAIL (code {result.returncode})")
    except Exception as e:
        print(f"ERROR: {e}")

print(f"\n成功: {success_count}/{len(test_fonts)}")
print("\n生成的文件:")
for f in sorted(os.listdir(out_dir)):
    if "FontTest_" in f:
        full_path = os.path.join(out_dir, f)
        size_mb = os.path.getsize(full_path) / 1024 / 1024
        print(f"  {f} ({size_mb:.1f} MB)")

print("\n提示: 使用视频播放器打开文件，检查文本字体是否不同")
