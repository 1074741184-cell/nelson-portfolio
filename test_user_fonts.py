#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test using fonts from user font directory
Path: C:\\Users\\admin\\Desktop\\字体
"""
import os
import subprocess
import sys

ffmpeg_exe = r"E:\VScodeProjects\ffmpeg.exe"
font_dir = r"C:\Users\admin\Desktop\字体"
out_dir = r"C:\Users\admin\Desktop\测试用输出2"

print("=" * 70)
print("使用本地字体目录生成视频 - 字体切换测试")
print("=" * 70)
print(f"字体目录: {font_dir}")
print(f"输出目录: {out_dir}\n")

# 扫描字体目录
font_files = [f for f in os.listdir(font_dir) if f.lower().endswith(('.ttf', '.otf'))]

if not font_files:
    print("错误: 字体目录中没有字体文件")
    sys.exit(1)

print(f"找到 {len(font_files)} 个字体文件:")
for i, f in enumerate(font_files, 1):
    print(f"  {i}. {f}")

# 选择差别比较大的字体
selected_fonts = [
    "Impact.ttf",
    "Georgia.ttf", 
    "arial.ttf",
    "Pacifico-Regular.ttf",
]

# 检查选定的字体是否存在
missing = [f for f in selected_fonts if f not in font_files]
if missing:
    print(f"\n警告: 以下字体不存在，使用前 4 个可用字体代替: {missing}")
    selected_fonts = font_files[:4]

print(f"\n使用的字体:")
for i, f in enumerate(selected_fonts, 1):
    print(f"  {i}. {f}")

print("\n开始生成视频...\n")

success = 0
failed = 0

for i, font_file in enumerate(selected_fonts, 1):
    font_path = os.path.join(font_dir, font_file)
    # 从文件名提取字体显示名（去掉扩展名）
    font_display_name = os.path.splitext(font_file)[0]
    out_file = os.path.join(out_dir, f"UserFont_Test_{i}_{font_display_name}.mp4")
    
    # 使用完整路径作为 fontfile 值
    # FFmpeg 期望: fontfile='C:/Users/admin/Desktop/字体/Impact.ttf'
    font_path_unix = font_path.replace("\\", "/")
    
    print(f"[{i}/4] 字体: {font_display_name}", end=' ', flush=True)
    print(f"(文件: {font_file})", end=' ')
    
    try:
        # 使用 font 参数（系统字体名称）
        drawtext = (f"drawtext=font={font_display_name}:text='UserFont Test':"
                   f"fontsize=100:fontcolor=yellow:borderw=2:bordercolor=black:"
                   f"x=(w-text_w)/2:y=(h-text_h)/2")
        
        cmd = [
            ffmpeg_exe, '-y',
            '-f', 'lavfi', '-i', 'color=c=black:s=1080x1920:d=2',
            '-vf', drawtext,
            '-c:v', 'libx264', '-preset', 'fast',
            out_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=60, errors='replace')
        
        if result.returncode == 0 and os.path.exists(out_file):
            size_mb = os.path.getsize(out_file) / 1024 / 1024
            print(f"✓ OK ({size_mb:.1f} MB)")
            success += 1
        else:
            print(f"✗ FAIL")
            failed += 1
    except Exception as e:
        print(f"✗ ERROR: {e}")
        failed += 1

print("\n" + "=" * 70)
print(f"结果: {success} 成功, {failed} 失败")
print("=" * 70)

print("\n生成的测试视频:")
for i, font_file in enumerate(selected_fonts, 1):
    font_display_name = os.path.splitext(font_file)[0]
    out_file = os.path.join(out_dir, f"UserFont_Test_{i}_{font_display_name}.mp4")
    
    if os.path.exists(out_file):
        size_mb = os.path.getsize(out_file) / 1024 / 1024
        print(f"  ✓ {os.path.basename(out_file)} ({size_mb:.1f} MB)")
    else:
        print(f"  ✗ {os.path.basename(out_file)} (未生成)")

print(f"\n提示:")
print(f"  - 所有测试视频已保存到: {out_dir}")
print(f"  - 请用视频播放器打开，对比各个视频的字体差异")
print(f"  - 使用系统字体名称（不是路径）能确保正常切换")
