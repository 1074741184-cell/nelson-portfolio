import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser, scrolledtext
import threading
import subprocess
import os
import psutil
import json
import random
import sys
import ctypes
try:
    from PIL import Image, ImageDraw
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# 资源路径定位函数
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, relative_path)


class ModernButton(tk.Button):
    """现代化按钮类 - 应用 UI UX Pro Max 设计系统"""
    
    def __init__(self, parent, text, button_type="secondary", **kwargs):
        """
        button_type: "primary" (主操作/蓝色) | "secondary" (次操作/灰色) | "danger" (危险/红色)
        优化: 使用专业的颜色系统和平滑过渡
        """
        self.button_type = button_type
        self.is_disabled = False
        
        # 提取所有可能的参数
        font_arg = kwargs.pop('font', None)
        bg_arg = kwargs.pop('bg', None)
        fg_arg = kwargs.pop('fg', None)
        padx_arg = kwargs.pop('padx', None)
        pady_arg = kwargs.pop('pady', None)
        
        self.base_bg = bg_arg
        self.base_fg = fg_arg
        
        # UI UX Pro Max 优化配色系统
        if button_type == "primary":
            # 专业蓝色 - Primary Blue from Professional SaaS Palette
            self.base_bg = self.base_bg or "#0066CC"        # 主色
            self.base_fg = self.base_fg or "#FFFFFF"        # 白色文字
            self.hover_bg = "#0051A8"                         # 深蓝
            self.active_bg = "#003D7A"                        # 更深蓝
            self.disabled_bg = "#CCCCCC"                      # 灰色禁用
        elif button_type == "danger":
            # 警告红色 - 保持红色系
            self.base_bg = self.base_bg or "#FF6B35"         # 橙红
            self.base_fg = self.base_fg or "#FFFFFF"
            self.hover_bg = "#E55A28"
            self.active_bg = "#CC4922"
            self.disabled_bg = "#CCCCCC"
        else:  # secondary
            # 次要操作 - 优雅灰色
            self.base_bg = self.base_bg or "#E8E8E8"         # 浅灰
            self.base_fg = self.base_fg or "#2D3436"         # 深灰文字
            self.hover_bg = "#D0D0D0"
            self.active_bg = "#B8B8B8"
            self.disabled_bg = "#CCCCCC"
        
        self.disabled_fg = "#999999"
        self.border_color = "#0066CC" if button_type != "danger" else "#CC3311"
        
        # 使用提供的参数或默认值
        button_font = font_arg or ("Segoe UI", 9, "bold")
        button_padx = padx_arg or 16
        button_pady = pady_arg or 10
        
        # 设置按钮样式 - 现代扁平化风格，平滑过渡
        super().__init__(
            parent, 
            text=text,
            bg=self.base_bg,
            fg=self.base_fg,
            activebackground=self.hover_bg,
            activeforeground=self.base_fg,
            bd=0,                              # 移除边框 - 更现代
            relief="flat",                     # 扁平设计
            font=button_font,
            padx=button_padx,
            pady=button_pady,
            highlightthickness=0,              # 移除高光
            overrelief="flat",                 # 悬停效果平滑
            **kwargs
        )
        
        # 绑定事件
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
    
    def _on_enter(self, event):
        """Hover 效果 - 平滑色彩过渡"""
        if self['state'] != 'disabled':
            self.config(bg=self.hover_bg)
    
    def _on_leave(self, event):
        """Leave 效果 - 恢复"""
        if self['state'] != 'disabled':
            self.config(bg=self.base_bg)
    
    def _on_press(self, event):
        """Active 效果 - 按下感"""
        if self['state'] != 'disabled':
            self.config(bg=self.active_bg)
            
    def _on_release(self, event):
        """释放鼠标 - 恢复 Hover 状态"""
        if self['state'] != 'disabled':
            self.config(bg=self.hover_bg)
    
    def set_disabled(self, disabled=True):
        """设置禁用状态"""
        self.is_disabled = disabled
        if disabled:
            self.config(state='disabled', bg=self.disabled_bg, fg=self.disabled_fg)
        else:
            self.config(state='normal', bg=self.base_bg, fg=self.base_fg)


class NelsonBatchStitcher:
    def __init__(self, main_root: tk.Tk):
        self.root = main_root
        self.root.title("Nelson's 1-Click Video Editor v9.0 - UI UX Pro Max Design")
        self.root.geometry("640x1100")
        self.root.configure(bg="#FFFFFF")

        # 修复UI缩放问题
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass
        scale = ctypes.windll.user32.GetDpiForSystem() / 96.0
        self.root.tk.call('tk', 'scaling', scale)

        # 默认字体目录
        self.paths = {"a": "", "b": "", "v": "", "m": "", "t": "", "srt": "", "font_dir": r"C:\\Users\\admin\\Desktop\\字体"}
        self.path_labels = {}

        # 语言系统 - 双语支持
        self.current_language = "English"  # 默认英文
        self.translations = {
            "title": {
                "English": "Nelson's Video Editor Pro",
                "中文": "奈尔森视频编辑器专业版"
            },
            "subtitle": {
                "English": "Powered by UI UX Pro Max Design System",
                "中文": "采用 UI UX Pro Max 设计系统"
            },
            "toggle_lang": {
                "English": "🌐 中文",
                "中文": "🌐 English"
            },
            "section_01": {
                "English": "01 | Resource Configuration",
                "中文": "01 | 资源配置"
            },
            "main_video_a": {
                "English": "Main Video A",
                "中文": "主视频 A"
            },
            "stitch_video_b": {
                "English": "Stitch Video B",
                "中文": "拼接视频 B"
            },
            "voiceover": {
                "English": "Voiceover Audio",
                "中文": "解说音频"
            },
            "bg_music": {
                "English": "Background Music",
                "中文": "背景音乐"
            },
            "subtitle_file": {
                "English": "Subtitle File",
                "中文": "字幕文件"
            },
            "export_dir": {
                "English": "Export Directory",
                "中文": "导出目录"
            },
            "waiting": {
                "English": "Waiting...",
                "中文": "等待..."
            },
            "connected": {
                "English": "✔ Connected",
                "中文": "✔ 已连接"
            },
            "section_02": {
                "English": "02 | Effects Engine",
                "中文": "02 | 效果引擎"
            },
            "transition_effect": {
                "English": "Transition Effect",
                "中文": "转场特效"
            },
            "hardware_mode": {
                "English": "Hardware Mode",
                "中文": "硬件模式"
            },
            "cpu_mode": {
                "English": "CPU Compatible",
                "中文": "兼容模式 (CPU)"
            },
            "gpu_mode": {
                "English": "NVIDIA GPU Acceleration",
                "中文": "NVIDIA GPU加速"
            },
            "random_color": {
                "English": "🎨 Random Color Mode",
                "中文": "🎨 全域颜色随机"
            },
            "enable_srt": {
                "English": "📝 Enable Subtitles",
                "中文": "📝 开启字幕渲染"
            },
            "section_03": {
                "English": "03 | Style Control Center",
                "中文": "03 | 样式控制中心"
            },
            "title_text": {
                "English": "Title Text:",
                "中文": "标题内容:"
            },
            "display_time": {
                "English": "Display Time:",
                "中文": "显示时间:"
            },
            "to_s": {
                "English": "s to",
                "中文": "s 到"
            },
            "s_to": {
                "English": "s to",
                "中文": "s 到"
            },
            "ready_label": {
                "English": "Ready",
                "中文": "就绪"
            },
            "font_mode": {
                "English": "Font Mode:",
                "中文": "字体模式:"
            },
            "single_font": {
                "English": "Single Font",
                "中文": "指定单一字体"
            },
            "random_font": {
                "English": "Random from Folder",
                "中文": "随机文件夹字体"
            },
            "import_fonts": {
                "English": "📂 Import Fonts",
                "中文": "📂 导入字体库"
            },
            "ready": {
                "English": "Ready:",
                "中文": "就绪:"
            },
            "title_color": {
                "English": "Title Color",
                "中文": "固定标题"
            },
            "border_color": {
                "English": "Border Color",
                "中文": "固定描边"
            },
            "subtitle": {
                "English": "Subtitle",
                "中文": "固定字幕"
            },
            "subtitle_border": {
                "English": "Subtitle Border",
                "中文": "字幕描边"
            },
            "title_size": {
                "English": "Title Size",
                "中文": "标题大小"
            },
            "border_width": {
                "English": "Border Width",
                "中文": "标题描边粗"
            },
            "subtitle_size": {
                "English": "Subtitle Size",
                "中文": "字幕大小"
            },
            "subtitle_border_width": {
                "English": "Subtitle Border",
                "中文": "字幕描边粗"
            },
            "subtitle_position": {
                "English": "Subtitle Position",
                "中文": "字幕位置(↑)"
            },
            "section_04": {
                "English": "04 | Audio Mixer",
                "中文": "04 | 混音矩阵"
            },
            "original_audio": {
                "English": "🎬 Original",
                "中文": "🎬 原音"
            },
            "voiceover_vol": {
                "English": "🎙 Voiceover",
                "中文": "🎙 解说"
            },
            "bgm_vol": {
                "English": "🎵 BGM",
                "中文": "🎵 BGM"
            },
            "start_btn": {
                "English": "▶ START PROCESSING",
                "中文": "▶ 一键执行全自动化剪辑"
            },
            "processing": {
                "English": "Processing... Please wait",
                "中文": "奈尔森引擎正在计算..."
            },
            "report_title": {
                "English": "🏆 Processing Report",
                "中文": "🏆 奈尔森剪辑任务报告"
            },
            "report_header": {
                "English": "🏆 Nelson's Processing Pipeline - Report",
                "中文": "🏆 奈尔森自动化流水线 - 任务报告"
            }
        }

        # UI UX Pro Max 配色方案 - Professional + Modern
        # 来自 UI UX Pro Max: SaaS Professional Palette
        self.primary_color = "#0066CC"         # 主色 - 专业蓝
        self.primary_dark = "#0051A8"          # 深蓝
        self.secondary_color = "#E8E8E8"       # 次要 - 浅灰
        self.accent_color = "#FF6B35"          # 强调 - 橙红
        self.success_color = "#00D084"         # 成功 - 绿
        self.warning_color = "#FFB81C"         # 警告 - 金色
        self.bg_primary = "#FFFFFF"            # 主背景
        self.bg_secondary = "#F5F5F5"          # 次背景
        self.bg_card = "#FAFAFA"               # 卡片背景
        self.text_primary = "#2D3436"          # 主文字
        self.text_secondary = "#7A8BA8"        # 次文字
        self.border_color = "#E0E0E0"          # 边框

        self.selected_color = "#FF6B35"
        self.selected_border_color = "#000000"
        self.srt_color = "#FFFFFF"
        self.srt_border_color = "#000000"
        self.selected_font_path = "C:/Windows/Fonts/arialbd.ttf"
        self.selected_font_name = "Arial Bold"

        self.xfade_effects = ['fade', 'wipeleft', 'wiperight', 'slideleft', 'slideright']
        self.combo_options = ['随机模式'] + self.xfade_effects

        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 优化进度条样式 - 现代设计
        self.style.configure("TProgressbar", thickness=8, troughcolor=self.bg_secondary, 
                           background=self.primary_color, borderwidth=0)
        
        # 优化下拉菜单样式
        self.style.configure("TCombobox", fieldbackground=self.bg_secondary, 
                           background=self.bg_secondary, 
                           foreground=self.text_primary, borderwidth=1, relief="solid", 
                           padding=3, font=("Segoe UI", 9))

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.setup_ui()

    def setup_ui(self):
        # 优化头部 - 现代设计
        header = tk.Frame(self.root, bg=self.primary_color, height=90)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # 顶部行 - 标题和语言切换按钮
        top_row = tk.Frame(header, bg=self.primary_color)
        top_row.pack(fill="x", pady=(8, 0))
        
        tk.Label(top_row, text=self.translations["title"][self.current_language], 
                font=("Segoe UI", 18, "bold"), 
                fg="#FFFFFF", bg=self.primary_color).pack(side="left", padx=20, pady=(12, 0))
        
        # 语言切换按钮
        self.lang_btn = ModernButton(top_row, text=self.translations["toggle_lang"][self.current_language], 
                                    command=self.toggle_language, button_type="secondary", width=12)
        self.lang_btn.pack(side="right", padx=20, pady=(12, 0))
        
        # 副标题
        tk.Label(header, text=self.translations["subtitle"][self.current_language], 
                font=("Segoe UI", 8), 
                fg="#E0E0E0", bg=self.primary_color).pack(pady=(0, 12))

        # 创建可滚动的主容器
        scrollable_frame = tk.Frame(self.root, bg=self.bg_primary)
        scrollable_frame.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(scrollable_frame, bg=self.bg_primary, highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
        main_container = tk.Frame(canvas, bg=self.bg_primary, padx=20, pady=15)
        
        main_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=main_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(fill="both", expand=True, side="left")
        scrollbar.pack(fill="y", side="right")
        
        # 鼠标滚轮滚动支持
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # 01 资源配置区
        self._add_section_title(main_container, self.translations["section_01"][self.current_language])
        path_grid = tk.Frame(main_container, bg=self.bg_primary)
        path_grid.pack(fill="x", pady=(0, 15))

        configs = [
            (self.translations["main_video_a"][self.current_language], "a"), 
            (self.translations["stitch_video_b"][self.current_language], "b"), 
            (self.translations["voiceover"][self.current_language], "v"), 
            (self.translations["bg_music"][self.current_language], "m"), 
            (self.translations["subtitle_file"][self.current_language], "srt"), 
            (self.translations["export_dir"][self.current_language], "t")
        ]
        
        for i, (text, key) in enumerate(configs):
            row, col = i // 2, i % 2 * 2
            btn = ModernButton(path_grid, text=text, command=lambda k=key: self.select_any(k), 
                              button_type="secondary", width=12)
            btn.grid(row=row, column=col, pady=6, sticky="w")
            
            lbl = tk.Label(path_grid, text=self.translations["waiting"][self.current_language], fg=self.text_secondary, 
                          bg=self.bg_primary, font=("Segoe UI", 8), width=20, anchor="w")
            lbl.grid(row=row, column=col + 1, padx=8, sticky="w")
            self.path_labels[key] = lbl

        # 02 效果引擎区
        self._add_section_title(main_container, self.translations["section_02"][self.current_language])
        visual_f = tk.Frame(main_container, bg=self.bg_primary)
        visual_f.pack(fill="x", pady=(0, 10))

        tk.Label(visual_f, text=self.translations["transition_effect"][self.current_language], fg=self.text_secondary, 
                bg=self.bg_primary, font=("Segoe UI", 9)).pack(side="left", padx=(0, 10))
        self.effect_combo = ttk.Combobox(visual_f, values=self.combo_options, state="readonly", width=14)
        self.effect_combo.current(0)
        self.effect_combo.pack(side="left", padx=(0, 20))

        tk.Label(visual_f, text=self.translations["hardware_mode"][self.current_language], fg=self.text_secondary, 
                bg=self.bg_primary, font=("Segoe UI", 9)).pack(side="left", padx=(0, 10))
        self.hw_mode = ttk.Combobox(visual_f, values=[self.translations["cpu_mode"][self.current_language], 
                                                      self.translations["gpu_mode"][self.current_language]], 
                                   state="readonly", width=16)
        self.hw_mode.current(0)
        self.hw_mode.pack(side="left", padx=0)

        # 选项开关
        switch_f = tk.Frame(main_container, bg=self.bg_primary)
        switch_f.pack(fill="x", pady=10)
        
        self.random_color_var = tk.BooleanVar(value=True)
        tk.Checkbutton(switch_f, text=self.translations["random_color"][self.current_language], variable=self.random_color_var, 
                      bg=self.bg_primary, fg=self.text_primary, selectcolor=self.bg_primary, 
                      activebackground=self.bg_primary, font=("Segoe UI", 9)).pack(side="left", padx=10)
        
        self.enable_srt_var = tk.BooleanVar(value=True)
        tk.Checkbutton(switch_f, text=self.translations["enable_srt"][self.current_language], variable=self.enable_srt_var, 
                      bg=self.bg_primary, fg=self.text_primary, selectcolor=self.bg_primary, 
                      activebackground=self.bg_primary, font=("Segoe UI", 9)).pack(side="left", padx=10)

        # 03 样式控制中心
        self._add_section_title(main_container, self.translations["section_03"][self.current_language])
        style_f = tk.Frame(main_container, bg=self.bg_card, padx=18, pady=15)
        style_f.pack(fill="x")

        tk.Label(style_f, text=self.translations["title_text"][self.current_language], fg=self.text_secondary, 
                bg=self.bg_card, font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", pady=(0, 8))
        
        self.sub_entry = tk.Entry(style_f, bg="#FFFFFF", fg=self.text_primary, 
                                 insertbackground=self.primary_color, bd=1, relief="solid", 
                                 width=40, font=("Segoe UI", 9))
        self.sub_entry.insert(0, "NelsonCreations")
        self.sub_entry.grid(row=0, column=1, columnspan=3, pady=(0, 8), ipady=5, sticky="ew")

        # 显示时间
        tk.Label(style_f, text=self.translations["display_time"][self.current_language], fg=self.text_secondary, 
                bg=self.bg_card, font=("Segoe UI", 9)).grid(row=1, column=0, pady=(0, 8), sticky="w")
        
        time_inner = tk.Frame(style_f, bg=self.bg_card)
        time_inner.grid(row=1, column=1, columnspan=3, sticky="w")
        
        self.time_start = tk.Entry(time_inner, bg="#FFFFFF", fg=self.primary_color, 
                                  bd=1, relief="solid", width=5, justify="center", 
                                  font=("Segoe UI", 9))
        self.time_start.insert(0, "2")
        self.time_start.pack(side="left")
        
        tk.Label(time_inner, text=self.translations["s_to"][self.current_language], fg=self.text_secondary, bg=self.bg_card, 
                padx=8, font=("Segoe UI", 9)).pack(side="left")
        
        self.time_end = tk.Entry(time_inner, bg="#FFFFFF", fg=self.primary_color, 
                                bd=1, relief="solid", width=5, justify="center", 
                                font=("Segoe UI", 9))
        self.time_end.insert(0, "8")
        self.time_end.pack(side="left")
        
        tk.Label(time_inner, text="s", fg=self.text_secondary, bg=self.bg_card, 
                padx=0, font=("Segoe UI", 9)).pack(side="left")

        # 字体模式
        tk.Label(style_f, text=self.translations["font_mode"][self.current_language], fg=self.text_secondary, 
                bg=self.bg_card, font=("Segoe UI", 9)).grid(row=2, column=0, pady=(8, 8), sticky="w")
        
        self.font_mode = ttk.Combobox(style_f, values=[self.translations["single_font"][self.current_language], 
                                                       self.translations["random_font"][self.current_language]], 
                                     state="readonly", width=16)
        self.font_mode.current(1)
        self.font_mode.grid(row=2, column=1, sticky="w")
        
        self.import_font_btn = ModernButton(style_f, text=self.translations["import_fonts"][self.current_language], 
                                           command=self.handle_font_selection, 
                                           button_type="secondary", width=16)
        self.import_font_btn.grid(row=2, column=2, padx=8, sticky="w")

        self.font_status_lbl = tk.Label(style_f, text=self.translations["ready_label"][self.current_language] + ": " + self.selected_font_name, 
                                       fg=self.primary_color, bg=self.bg_card, font=("Segoe UI", 8))
        self.font_status_lbl.grid(row=3, column=1, columnspan=3, sticky="w", pady=(8, 0))

        # 颜色选择按钮
        color_btns = tk.Frame(style_f, bg=self.bg_card)
        color_btns.grid(row=4, column=0, columnspan=4, pady=15, sticky="w")
        
        ModernButton(color_btns, text=self.translations["title_color"][self.current_language], command=self.pick_color, 
                    button_type="secondary", width=10).pack(side="left", padx=4)
        ModernButton(color_btns, text=self.translations["border_color"][self.current_language], command=self.pick_border_color, 
                    button_type="secondary", width=12).pack(side="left", padx=4)
        ModernButton(color_btns, text=self.translations["subtitle"][self.current_language], command=self.pick_srt_color, 
                    button_type="secondary", width=10).pack(side="left", padx=4)
        ModernButton(color_btns, text=self.translations["subtitle_border"][self.current_language], command=self.pick_srt_border_color, 
                    button_type="secondary", width=15).pack(side="left", padx=4)

        # 尺寸滑块
        self.size_scale = self._add_dark_scale(style_f, self.translations["title_size"][self.current_language], 80, 20, 250, 5)
        self.border_scale = self._add_dark_scale(style_f, self.translations["border_width"][self.current_language], 3, 0, 20, 6)
        self.srt_size_scale = self._add_dark_scale(style_f, self.translations["subtitle_size"][self.current_language], 24, 5, 150, 7)
        self.srt_border_scale = self._add_dark_scale(style_f, self.translations["subtitle_border_width"][self.current_language], 2, 0, 10, 8)
        self.srt_margin_scale = self._add_dark_scale(style_f, self.translations["subtitle_position"][self.current_language], 50, 0, 800, 9)

        # 04 混音矩阵
        self._add_section_title(main_container, self.translations["section_04"][self.current_language])
        mix_f = tk.Frame(main_container, bg=self.bg_primary)
        mix_f.pack(fill="x", pady=10)
        
        self.vol_a = self._add_mini_vol(mix_f, self.translations["original_audio"][self.current_language], 50, 0)
        self.vol_v = self._add_mini_vol(mix_f, self.translations["voiceover_vol"][self.current_language], 100, 1)
        self.vol_m = self._add_mini_vol(mix_f, self.translations["bgm_vol"][self.current_language], 30, 2)

        # 底部控制栏
        bottom_frame = tk.Frame(self.root, bg=self.bg_primary, height=60)
        bottom_frame.pack(fill="x", side="bottom")
        
        self.progress = ttk.Progressbar(bottom_frame, style="TProgressbar", 
                                       orient="horizontal", mode='determinate')
        self.progress.pack(fill="x")

        self.run_btn = ModernButton(bottom_frame, text=self.translations["start_btn"][self.current_language], 
                                   command=self.start_thread, button_type="primary",
                                   font=("Segoe UI", 12, "bold"), padx=20, pady=15)
        self.run_btn.pack(fill="x", padx=0, pady=0)
        self.run_btn.set_disabled(True)

        # 启动时，如果设置了字体目录，显示相关信息但不预选字体
        if os.path.isdir(self.paths.get("font_dir", "")):
            try:
                fonts = [f for f in os.listdir(self.paths["font_dir"]) 
                        if f.lower().endswith(('.ttf', '.otf', '.ttc'))]
                if fonts:
                    font_count = len(fonts)
                    # 更新状态标签显示字体库信息
                    status_text = f"Folder: {os.path.basename(self.paths['font_dir'])} ({font_count} fonts - Random mode ready)"
                else:
                    status_text = "Folder: Found but no fonts"
            except:
                status_text = "Folder: Error reading"
        else:
            status_text = "Default: Arial Bold"
        
        # 保存对主要UI元素的引用
        self.ui_elements = {}

    def toggle_language(self):
        """切换语言"""
        self.current_language = "中文" if self.current_language == "English" else "English"
        self.refresh_ui()

    def refresh_ui(self):
        """刷新整个UI以切换语言"""
        # 销毁所有子 widget 进行完整刷新
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 重新调用setup_ui
        self.setup_ui()

    def _add_section_title(self, parent, text):
        # 现代化标题 - 使用左边框
        title_frame = tk.Frame(parent, bg=self.bg_primary, height=35)
        title_frame.pack(anchor="w", pady=(15, 8), fill="x")
        title_frame.pack_propagate(False)
        
        left_border = tk.Frame(title_frame, bg=self.primary_color, width=4, height=20)
        left_border.pack(side="left", padx=(0, 12), pady=7)
        left_border.pack_propagate(False)
        
        tk.Label(title_frame, text=text, fg=self.text_primary, bg=self.bg_primary, 
                font=("Segoe UI", 11, "bold")).pack(side="left", padx=0)

    def _add_dark_scale(self, parent, label, val, f, t, row):
        tk.Label(parent, text=label, fg=self.text_secondary, bg=self.bg_card, 
                font=("Segoe UI", 9)).grid(row=row, column=0, sticky="w")
        
        s = tk.Scale(parent, from_=f, to=t, orient="horizontal", bg=self.bg_card, 
                    fg=self.primary_color, highlightthickness=0, bd=0, length=230, 
                    troughcolor=self.secondary_color, font=("Segoe UI", 8), 
                    activebackground=self.accent_color)
        s.set(val)
        s.grid(row=row, column=1, columnspan=3, sticky="ew", pady=8)
        return s

    def _add_mini_vol(self, parent, label, val, col):
        f = tk.Frame(parent, bg=self.bg_primary)
        f.grid(row=0, column=col, padx=30, pady=10)
        
        tk.Label(f, text=label, fg=self.text_secondary, bg=self.bg_primary, 
                font=("Segoe UI", 9, "bold")).pack(pady=5)
        
        s = tk.Scale(f, from_=200, to=0, orient="vertical", bg=self.bg_primary, 
                    fg=self.primary_color, highlightthickness=0, bd=0, length=80, 
                    troughcolor=self.secondary_color, font=("Segoe UI", 8), 
                    activebackground=self.accent_color)
        s.set(val)
        s.pack()
        return s

    def select_any(self, key):
        path = filedialog.askopenfilename(filetypes=[("SRT", "*.srt")]) if key == "srt" else filedialog.askdirectory()
        if path:
            self.paths[key] = os.path.abspath(path)
            self.path_labels[key].config(text="✔ Connected", fg=self.success_color)
            base_ready = all(self.paths[k] != "" for k in ["a", "b", "v", "m", "t"])
            srt_ready = (not self.enable_srt_var.get()) or (self.paths["srt"] != "")
            if base_ready and srt_ready: 
                self.run_btn.set_disabled(False)
            else:
                self.run_btn.set_disabled(True)

    def handle_font_selection(self):
        font_mode = self.font_mode.get()
        # 检查是否选择了单一字体模式（支持英文和中文）
        if "Single" in font_mode or "指定单一" in font_mode:
            f = filedialog.askopenfilename(initialdir="C:/Windows/Fonts", filetypes=[("Font", "*.ttf *.otf *.ttc")])
            if f: 
                self.selected_font_path = f.replace("\\", "/")
                self.selected_font_name = os.path.basename(f)
                self.font_status_lbl.config(text="Single: " + self.selected_font_name)
        else:
            d = filedialog.askdirectory()
            if d: 
                self.paths["font_dir"] = os.path.abspath(d)
                # 只更新目录，不预先选择字体 - 让批处理时为每个视频随机选择
                try:
                    fonts = [f for f in os.listdir(d) if f.lower().endswith(('.ttf', '.otf', '.ttc'))]
                    if fonts:
                        self.font_status_lbl.config(text=f"Folder: {os.path.basename(d)} ({len(fonts)} fonts)")
                    else:
                        self.font_status_lbl.config(text=f"Folder: {os.path.basename(d)} (no fonts found)")
                except:
                    self.font_status_lbl.config(text="Folder: " + os.path.basename(d))

    def pick_color(self):
        c = colorchooser.askcolor(initialcolor=self.selected_color)[1]
        if c: self.selected_color = c

    def pick_border_color(self):
        c = colorchooser.askcolor(initialcolor=self.selected_border_color)[1]
        if c: self.selected_border_color = c

    def pick_srt_color(self):
        c = colorchooser.askcolor(initialcolor=self.srt_color)[1]
        if c: self.srt_color = c

    def pick_srt_border_color(self):
        c = colorchooser.askcolor(initialcolor=self.srt_border_color)[1]
        if c: self.srt_border_color = c

    def get_duration(self, file_path):
        try:
            ffprobe_path = resource_path('ffprobe.exe')
            if not os.path.exists(ffprobe_path):
                print(f"Error: ffprobe.exe not found - {ffprobe_path}")
                return 10.0
            cmd = [ffprobe_path, '-v', 'quiet', '-print_format', 'json', '-show_format', file_path]
            res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            return float(json.loads(res.stdout)['format']['duration'])
        except Exception as e:
            print(f"Duration error: {str(e)}")
            return 10.0

    def start_thread(self):
        threading.Thread(target=self.batch_process, daemon=True).start()

    def show_final_report(self, logs):
        report_win = tk.Toplevel(self.root)
        report_win.title("🏆 Processing Report")
        report_win.geometry("600x700")
        report_win.configure(bg=self.bg_primary)
        
        # 标题栏
        title_bar = tk.Frame(report_win, bg=self.primary_color, height=60)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)
        
        tk.Label(title_bar, text="🏆 Nelson's Processing Pipeline - Report", 
                font=("Segoe UI", 13, "bold"), fg="#FFFFFF", bg=self.primary_color).pack(pady=12)
        
        area = scrolledtext.ScrolledText(report_win, bg=self.bg_card, fg=self.text_primary, 
                                        font=("Consolas", 9), bd=0, padx=12, pady=12)
        area.pack(fill="both", expand=True, padx=15, pady=12)
        
        for line in logs: 
            area.insert(tk.END, line + "\n" + "=" * 50 + "\n")
        area.configure(state='disabled')

    def batch_process(self):
        report_logs = []
        try:
            hw_mode = self.hw_mode.get()
            if "NVIDIA" in hw_mode:
                v_codec = "h264_nvenc"
                v_preset = "p1"
                hw_info = "⚡ NVIDIA GPU Acceleration"
            else:
                v_codec = "libx264"
                v_preset = "fast"
                hw_info = "🐢 CPU Compatible Mode"

            def scan(d):
                return sorted([f for f in os.listdir(d) if f.lower().endswith(('.mp4', '.mov', '.mp3', '.wav', '.m4a'))])

            def scan_fonts(d):
                return [os.path.join(d, f) for f in os.listdir(d) if f.lower().endswith(('.ttf', '.otf', '.ttc'))]

            files_a, files_b = scan(self.paths["a"]), scan(self.paths["b"])
            v_files, m_files = scan(self.paths["v"]), scan(self.paths["m"])

            random_fonts = []
            font_mode = self.font_mode.get()
            # 检查是否启用随机字体模式（支持英文和中文）
            if ("Random" in font_mode or "随机" in font_mode) and self.paths["font_dir"]:
                random_fonts = scan_fonts(self.paths["font_dir"])

            self.run_btn.set_disabled(True)
            self.run_btn.config(text="Processing... Please wait")
            self.progress['maximum'] = len(files_a)

            srt_file_path = self.paths["srt"].replace("\\", "/").replace(":", "\\:") if self.enable_srt_var.get() else ""

            for index, name_a in enumerate(files_a):
                if random_fonts:
                    font_path = random.choice(random_fonts)
                    font_basename = os.path.splitext(os.path.basename(font_path))[0]
                    font_name = font_basename
                else:
                    font_name = self.selected_font_name
                
                title_c = "#{:06x}".format(random.randint(0, 0xFFFFFF)) if self.random_color_var.get() else self.selected_color
                title_b_c = self.selected_border_color

                srt_final_filter = ""
                final_srt_color = "Disabled"
                final_srt_border = "Disabled"

                if self.enable_srt_var.get():
                    if self.random_color_var.get():
                        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                        srt_hex = f"#{r:02x}{g:02x}{b:02x}"
                        srt_b_hex = "#000000"
                    else:
                        srt_hex, srt_b_hex = self.srt_color, self.srt_border_color

                    final_srt_color = srt_hex
                    final_srt_border = srt_b_hex
                    s_h, s_b_h = srt_hex.lstrip('#'), srt_b_hex.lstrip('#')
                    srt_color_ff = f"&H{s_h[4:6]}{s_h[2:4]}{s_h[0:2]}&"
                    srt_border_ff = f"&H{s_b_h[4:6]}{s_b_h[2:4]}{s_b_h[0:2]}&"

                    srt_final_filter = (
                        f",subtitles='{srt_file_path}':force_style='Fontsize={self.srt_size_scale.get()},"
                        f"PrimaryColour={srt_color_ff},OutlineColour={srt_border_ff},"
                        f"BorderStyle=1,Outline={self.srt_border_scale.get()},Shadow=0,Alignment=2,"
                        f"MarginV={self.srt_margin_scale.get()}'")

                t_s, t_e = self.time_start.get(), self.time_end.get()

                report_logs.append(
                    f"Sequence: #{index + 1}\nFilename: {name_a}\nHardware: {hw_info}\n"
                    f"【Title Settings】\n  - Font: {font_name}\n  - Color: {title_c}\n  - Border: {title_b_c}\n"
                    f"  - Display Time: {t_s}s - {t_e}s\n"
                    f"【Subtitle Settings】\n  - Color: {final_srt_color}\n  - Border: {final_srt_border}\n"
                    f"  - Vertical Margin: {self.srt_margin_scale.get()}px"
                )

                effect_mode = self.effect_combo.get()
                # 检查是否启用随机转场特效（支持英文和中文）
                eff = random.choice(self.xfade_effects) if ("Random" in effect_mode or "随机" in effect_mode) else effect_mode

                try:
                    in_a = os.path.join(self.paths["a"], name_a)
                    in_b = os.path.join(self.paths["b"], files_b[index % len(files_b)])
                    in_v = os.path.join(self.paths["v"], random.choice(v_files))
                    in_m = os.path.join(self.paths["m"], random.choice(m_files))
                    out_p = os.path.join(self.paths["t"], f"Nelson_Output_{index + 1}.mp4")

                    for fp, fname in [(in_a, "Video A"), (in_b, "Video B"), (in_v, "Voiceover"), (in_m, "BGM")]:
                        if not os.path.exists(fp):
                            report_logs.append(f"❌ File not found: {fname} - {fp}")
                            raise FileNotFoundError(f"File not found: {fp}")

                    d_a = self.get_duration(in_a) / 1.2
                    off = max(0.1, (d_a - 1.5))

                    alpha_exp = f"if(lt(t,{t_s}),0,if(lt(t,{t_s}+1),t-{t_s},if(lt(t,{t_e}-1),1,if(lt(t,{t_e}),{t_e}-t,0))))"

                    drawtext_str = (f'drawtext=font={font_name}:text=\'{self.sub_entry.get()}\':'
                                    f'fontcolor={title_c}:fontsize={self.size_scale.get()}:'
                                    f'borderw={self.border_scale.get()}:bordercolor={title_b_c}:'
                                    f'x=(w-text_w)/2:y=250:alpha=\'{alpha_exp}\'')

                    f_str = (
                        f"[0:v]setpts=PTS/1.2,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,trim=start=1,setpts=PTS-STARTPTS[v0];"
                        f"[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30[v1];"
                        f"[v0][v1]xfade=transition={eff}:duration=0.5:offset={off:.2f},format=yuv420p[vm];"
                        f"[vm]{drawtext_str}{srt_final_filter}[v_out];"
                        f"[0:a]atrim=start=1,asetpts=PTS-STARTPTS,volume={self.vol_a.get() / 100:.2f}[a0];"
                        f"[2:a]volume={self.vol_v.get() / 100:.2f}[av];"
                        f"[3:a]volume={self.vol_m.get() / 100:.2f}[am];"
                        f"[a0][av][am]amix=inputs=3:dropout_transition=0[a_out]")

                    ffmpeg_path = resource_path('ffmpeg.exe')
                    if not os.path.exists(ffmpeg_path):
                        report_logs.append(f"❌ ffmpeg.exe not found: {ffmpeg_path}")
                        raise FileNotFoundError(f"ffmpeg.exe not found: {ffmpeg_path}")

                    cmd = [ffmpeg_path, '-y', '-hwaccel', 'auto', '-i', in_a, '-i', in_b, '-i', in_v,
                           '-stream_loop', '-1', '-i', in_m,
                           '-filter_complex', f_str, '-map', '[v_out]', '-map', '[a_out]', '-c:v', v_codec,
                           '-preset', v_preset, '-t', f"{(d_a + self.get_duration(in_b) - 2.5):.2f}", out_p]
                    
                    print("FFmpeg Command:", " ".join(cmd))
                    result = subprocess.run(cmd, capture_output=True, text=True, errors='ignore')
                    if result.returncode != 0:
                        print("FFmpeg Error:", result.stderr)
                        report_logs.append(f"❌ FFmpeg Failed: {result.stderr}")
                        
                except Exception as e:
                    print("Batch Process Error:", str(e))
                    report_logs.append(f"❌ Error: {str(e)}")
                
                self.progress['value'] = index + 1
                self.root.update_idletasks()
            
            self.show_final_report(report_logs)
        finally:
            self.run_btn.set_disabled(False)
            self.run_btn.config(text="▶ START PROCESSING")
            self.progress['value'] = 0

    def on_closing(self):
        for proc in psutil.process_iter(['name']):
            try:
                if "ffmpeg" in (proc.info['name'] or "").lower(): 
                    proc.kill()
            except:
                pass
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = NelsonBatchStitcher(root)
    root.mainloop()
