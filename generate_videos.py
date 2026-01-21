#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
使用 NelsonTest 文本和不同字体自动生成视频
"""
import os
import subprocess
import sys
import random

# 配置路径
ffmpeg_exe = r"E:\VScodeProjects\ffmpeg.exe"

paths = {
    "a": r"C:\Users\admin\Desktop\主视频A",
    "b": r"C:\Users\admin\Desktop\B视频",
    "v": r"C:\Users\admin\Desktop\onepiece",
    "m": r"C:\Users\admin\Desktop\musics",
    "t": r"C:\Users\admin\Desktop\测试用输出2"
}

# 验证路径
for key, path in paths.items():
    if not os.path.isdir(path):
        print(f"错误: 目录不存在 {path}")
        sys.exit(1)

print("=" * 60)
print("自动生成多个视频 - 使用不同字体")
print("=" * 60)

# 获取文件列表
files_a = [f for f in os.listdir(paths["a"]) if f.lower().endswith(('.mp4', '.mov', '.avi'))]
files_b = [f for f in os.listdir(paths["b"]) if f.lower().endswith(('.mp4', '.mov', '.avi'))]
v_files = [f for f in os.listdir(paths["v"]) if f.lower().endswith(('.mp4', '.mov', '.avi'))]
m_files = [f for f in os.listdir(paths["m"]) if f.lower().endswith(('.mp3', '.m4a', '.wav'))]

print(f"视频A: {len(files_a)} 个")
print(f"视频B: {len(files_b)} 个")
print(f"视频库: {len(v_files)} 个")
print(f"音乐: {len(m_files)} 个\n")

if not all([files_a, files_b, v_files, m_files]):
    print("错误: 某些目录中没有文件")
    sys.exit(1)

# 选择差别比较大的字体
fonts = [
    "Impact",      # 粗体，现代风格
    "Georgia",     # 衬线字体，古典风格
    "Arial",       # 无衬线，简洁风格
    "Calibri",     # 现代无衬线
]

print("生成视频配置:")
print(f"  标题文本: NelsonTest")
print(f"  字体列表: {', '.join(fonts)}")
print(f"  输出目录: {paths['t']}\n")

text_content = "NelsonTest"
title_color = "#FFA500"  # 橙色
border_color = "#000000"
border_width = 2
font_size = 60

# 生成视频参数
video_config = []
for i in range(len(fonts)):
    font = fonts[i]
    input_a = os.path.join(paths["a"], files_a[i % len(files_a)])
    input_b = os.path.join(paths["b"], files_b[i % len(files_b)])
    input_v = os.path.join(paths["v"], random.choice(v_files))
    input_m = os.path.join(paths["m"], random.choice(m_files))
    output = os.path.join(paths["t"], f"NelsonTest_Video_{i+1}_{font}.mp4")
    
    video_config.append({
        "index": i + 1,
        "font": font,
        "input_a": input_a,
        "input_b": input_b,
        "input_v": input_v,
        "input_m": input_m,
        "output": output,
    })

print("视频列表:")
for config in video_config:
    print(f"  [{config['index']}] 字体={config['font']:10s} -> {os.path.basename(config['output'])}")

print("\n开始生成...")

success = 0
failed = 0

for config in video_config:
    idx = config['index']
    font = config['font']
    
    print(f"\n[{idx}/{len(video_config)}] 生成: {font}...", end=' ', flush=True)
    
    try:
        # 构建 drawtext 过滤器
        drawtext = (f"drawtext=font={font}:text='{text_content}':"
                   f"fontsize={font_size}:fontcolor={title_color}:"
                   f"borderw={border_width}:bordercolor={border_color}:"
                   f"x=(w-text_w)/2:y=250")
        
        # 简单的 FFmpeg 命令 - 直接合并视频
        cmd = [
            ffmpeg_exe, '-y',
            '-i', config['input_a'],
            '-i', config['input_b'],
            '-vf', f"{drawtext}",
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-c:a', 'aac',
            '-t', '5',
            config['output']
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=60, errors='replace')
        
        if result.returncode == 0 and os.path.exists(config['output']):
            size_mb = os.path.getsize(config['output']) / 1024 / 1024
            print(f"完成 ({size_mb:.1f} MB)")
            success += 1
        else:
            print(f"失败 (code {result.returncode})")
            failed += 1
            if result.stderr:
                err_lines = [l for l in result.stderr.split('\n') if 'error' in l.lower()]
                if err_lines:
                    print(f"    Error: {err_lines[0][:80]}")
    except Exception as e:
        print(f"异常: {e}")
        failed += 1

print("\n" + "=" * 60)
print(f"完成统计: {success} 成功, {failed} 失败")
print("=" * 60)

print("\n生成的视频:")
for config in video_config:
    if os.path.exists(config['output']):
        size_mb = os.path.getsize(config['output']) / 1024 / 1024
        print(f"  ✓ {os.path.basename(config['output'])} ({size_mb:.1f} MB)")
    else:
        print(f"  ✗ {os.path.basename(config['output'])} (未生成)")

print(f"\n提示: 所有视频已保存到: {paths['t']}")
