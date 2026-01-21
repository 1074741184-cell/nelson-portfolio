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

# 资源路径定位函数
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, relative_path)

class NelsonBatchStitcher:
    def __init__(self, main_root: tk.Tk):
        self.root = main_root
        self.root.title("奈尔森的一键剪辑 v8.8.0 - 自适应动力版")
        self.root.geometry("620x1080")
        self.root.configure(bg="#121212")

        # 修复UI缩放问题
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass
        scale = ctypes.windll.user32.GetDpiForSystem() / 96.0
        self.root.tk.call('tk', 'scaling', scale)

        # 默认将你提供的字体目录设为 font_dir，以便程序启动时能自动选中字体（更稳定）
        self.paths = {"a": "", "b": "", "v": "", "m": "", "t": "", "srt": "", "font_dir": r"C:\\Users\\admin\\Desktop\\字体"}
        self.path_labels = {}

        self.theme_cyan = "#00f5ff"
        self.dark_cyan = "#008b8b"
        self.bg_dark = "#121212"
        self.card_bg = "#1e1e1e"

        self.selected_color = "#FFA500"
        self.selected_border_color = "#000000"
        self.srt_color = "#FFFFFF"
        self.srt_border_color = "#000000"
        self.selected_font_path = "C:/Windows/Fonts/arialbd.ttf"
        self.selected_font_name = "Arial Bold"

        self.xfade_effects = ['fade', 'wipeleft', 'wiperight', 'slideleft', 'slideright']
        self.combo_options = ['随机模式'] + self.xfade_effects

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TProgressbar", thickness=8, troughcolor='#333333', background=self.theme_cyan,
                             borderwidth=0)
        self.style.configure("TCombobox", fieldbackground="#2a2a2a", background="#333333", foreground="white",
                             borderwidth=0)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self.root, bg=self.theme_cyan, height=60)
        header.pack(fill="x")
        tk.Label(header, text="奈尔森的一键剪辑", font=("Microsoft YaHei", 16, "bold"), fg="#000000",
                 bg=self.theme_cyan).pack(pady=10)

        # 创建可滚动的主容器
        scrollable_frame = tk.Frame(self.root, bg=self.bg_dark)
        scrollable_frame.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(scrollable_frame, bg=self.bg_dark, highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
        main_container = tk.Frame(canvas, bg=self.bg_dark, padx=25, pady=15)
        
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

        self._add_section_title(main_container, "01 | 资源目录配置")
        path_grid = tk.Frame(main_container, bg=self.bg_dark)
        path_grid.pack(fill="x", pady=(0, 15))

        configs = [("主视频 A", "a"), ("拼接视频 B", "b"), ("解说音频", "v"), ("背景音乐", "m"), ("字幕文件", "srt"),
                   ("导出目录", "t")]
        for i, (text, key) in enumerate(configs):
            row, col = i // 2, i % 2 * 2
            btn = tk.Button(path_grid, text=text, command=lambda k=key: self.select_any(k), bg="#2a2a2a", fg="#ffffff",
                            bd=0, width=10, activebackground=self.theme_cyan, font=("Segoe UI", 9))
            btn.grid(row=row, column=col, pady=4, sticky="w")
            lbl = tk.Label(path_grid, text="等待连接...", fg="#555555", bg=self.bg_dark, font=("Segoe UI", 8), width=18,
                           anchor="w")
            lbl.grid(row=row, column=col + 1, padx=5, sticky="w")
            self.path_labels[key] = lbl

        self._add_section_title(main_container, "02 | 奈尔森 AI 视觉引擎")
        visual_f = tk.Frame(main_container, bg=self.bg_dark)
        visual_f.pack(fill="x", pady=(0, 15))

        tk.Label(visual_f, text="转场特效", fg="#888888", bg=self.bg_dark).pack(side="left")
        self.effect_combo = ttk.Combobox(visual_f, values=self.combo_options, state="readonly", width=12)
        self.effect_combo.current(0);
        self.effect_combo.pack(side="left", padx=10)

        tk.Label(visual_f, text="动力模式", fg="#888888", bg=self.bg_dark).pack(side="left", padx=(10, 0))
        self.hw_mode = ttk.Combobox(visual_f, values=["兼容模式 (CPU)", "NVIDIA GPU加速"], state="readonly", width=15)
        self.hw_mode.current(0)
        self.hw_mode.pack(side="left", padx=10)

        switch_f = tk.Frame(main_container, bg=self.bg_dark)
        switch_f.pack(fill="x", pady=5)
        self.random_color_var = tk.BooleanVar(value=True)
        tk.Checkbutton(switch_f, text="全域颜色随机", variable=self.random_color_var, bg=self.bg_dark,
                       fg=self.theme_cyan, selectcolor=self.bg_dark, activebackground=self.bg_dark).pack(side="left",
                                                                                                         padx=5)
        self.enable_srt_var = tk.BooleanVar(value=True)
        tk.Checkbutton(switch_f, text="开启字幕渲染", variable=self.enable_srt_var, bg=self.bg_dark, fg="#FFD700",
                       selectcolor=self.bg_dark, activebackground=self.bg_dark).pack(side="left", padx=5)

        self._add_section_title(main_container, "03 | 样式控制中心")
        style_f = tk.Frame(main_container, bg=self.card_bg, padx=15, pady=15)
        style_f.pack(fill="x")

        tk.Label(style_f, text="标题内容:", fg="#888888", bg=self.card_bg).grid(row=0, column=0, sticky="w")
        self.sub_entry = tk.Entry(style_f, bg="#2a2a2a", fg="white", insertbackground=self.theme_cyan, bd=0, width=40)
        self.sub_entry.insert(0, "NelsonTest");
        self.sub_entry.grid(row=0, column=1, columnspan=3, pady=5, ipady=3)

        tk.Label(style_f, text="显示时间:", fg="#888888", bg=self.card_bg).grid(row=1, column=0, pady=5, sticky="w")
        time_inner = tk.Frame(style_f, bg=self.card_bg)
        time_inner.grid(row=1, column=1, columnspan=3, sticky="w")
        self.time_start = tk.Entry(time_inner, bg="#2a2a2a", fg=self.theme_cyan, bd=0, width=5, justify="center")
        self.time_start.insert(0, "2");
        self.time_start.pack(side="left")
        tk.Label(time_inner, text="s 到", fg="#555555", bg=self.card_bg, padx=5).pack(side="left")
        self.time_end = tk.Entry(time_inner, bg="#2a2a2a", fg=self.theme_cyan, bd=0, width=5, justify="center")
        self.time_end.insert(0, "8");
        self.time_end.pack(side="left")
        tk.Label(time_inner, text="s", fg="#555555", bg=self.card_bg, padx=5).pack(side="left")

        tk.Label(style_f, text="字体模式:", fg="#888888", bg=self.card_bg).grid(row=2, column=0, pady=5, sticky="w")
        self.font_mode = ttk.Combobox(style_f, values=["指定单一字体", "随机文件夹字体"], state="readonly", width=14)
        self.font_mode.current(1);
        self.font_mode.grid(row=2, column=1, sticky="w")
        tk.Button(style_f, text="📂 导入字体库", command=self.handle_font_selection, bg=self.dark_cyan, fg="white", bd=0,
                  width=15).grid(row=2, column=2, padx=5, sticky="w")

        self.font_status_lbl = tk.Label(style_f, text="就绪: " + self.selected_font_name, fg=self.theme_cyan,
                                        bg=self.card_bg, font=("Segoe UI", 8))
        self.font_status_lbl.grid(row=3, column=1, columnspan=3, sticky="w")

        color_btns = tk.Frame(style_f, bg=self.card_bg)
        color_btns.grid(row=4, column=0, columnspan=4, pady=10, sticky="w")
        btn_cfg = {"bg": "#333333", "fg": "white", "bd": 0, "width": 8, "font": ("Segoe UI", 8)}
        tk.Button(color_btns, text="固定标题", command=self.pick_color, **btn_cfg).pack(side="left", padx=2)
        tk.Button(color_btns, text="固定描边", command=self.pick_border_color, **btn_cfg).pack(side="left", padx=2)
        tk.Button(color_btns, text="固定字幕", command=self.pick_srt_color, **btn_cfg).pack(side="left", padx=2)
        tk.Button(color_btns, text="字幕描边", command=self.pick_srt_border_color, **btn_cfg).pack(side="left", padx=2)

        self.size_scale = self._add_dark_scale(style_f, "标题大小", 80, 20, 250, 5)
        self.border_scale = self._add_dark_scale(style_f, "标题描边粗", 3, 0, 20, 6)
        self.srt_size_scale = self._add_dark_scale(style_f, "字幕大小", 24, 5, 150, 7)
        self.srt_border_scale = self._add_dark_scale(style_f, "字幕描边粗", 2, 0, 10, 8)
        self.srt_margin_scale = self._add_dark_scale(style_f, "字幕位置(↑)", 50, 0, 800, 9)

        self._add_section_title(main_container, "04 | 混音矩阵")
        mix_f = tk.Frame(main_container, bg=self.bg_dark)
        mix_f.pack(fill="x")
        self.vol_a = self._add_mini_vol(mix_f, "原音", 50, 0)
        self.vol_v = self._add_mini_vol(mix_f, "解说", 100, 1)
        self.vol_m = self._add_mini_vol(mix_f, "BGM", 30, 2)

        # 底部控制栏
        bottom_frame = tk.Frame(self.root, bg=self.bg_dark)
        bottom_frame.pack(fill="x", side="bottom")
        
        self.progress = ttk.Progressbar(bottom_frame, style="TProgressbar", orient="horizontal", mode='determinate')
        self.progress.pack(fill="x")

        self.run_btn = tk.Button(bottom_frame, text="一键执行全自动化剪辑", command=self.start_thread, bg=self.theme_cyan,
                                 fg="#000000", font=("Microsoft YaHei", 11, "bold"), bd=0, height=2, state="disabled")
        self.run_btn.pack(fill="x")

        # 启动后如果默认字体目录存在则立即初始化并选中一个字体，保证界面显示与实际渲染一致
        if os.path.isdir(self.paths.get("font_dir", "")):
            try:
                self._init_font_from_dir(self.paths["font_dir"])
            except Exception:
                pass

    def _add_section_title(self, parent, text):
        tk.Label(parent, text=text, fg=self.theme_cyan, bg=self.bg_dark, font=("Segoe UI", 9, "bold")).pack(anchor="w",
                                                                                                            pady=(10,
                                                                                                                  5))

    def _add_dark_scale(self, parent, label, val, f, t, row):
        tk.Label(parent, text=label, fg="#666666", bg=self.card_bg, font=("Segoe UI", 8)).grid(row=row, column=0)
        s = tk.Scale(parent, from_=f, to=t, orient="horizontal", bg=self.card_bg, fg=self.theme_cyan,
                     highlightthickness=0, bd=0, length=220, troughcolor="#2a2a2a")
        s.set(val);
        s.grid(row=row, column=1, columnspan=3, sticky="we")
        return s

    def _add_mini_vol(self, parent, label, val, col):
        f = tk.Frame(parent, bg=self.bg_dark);
        f.grid(row=0, column=col, padx=25)
        tk.Label(f, text=label, fg="#555555", bg=self.bg_dark, font=("Segoe UI", 8)).pack()
        s = tk.Scale(f, from_=200, to=0, orient="vertical", bg=self.bg_dark, fg=self.theme_cyan, highlightthickness=0,
                     bd=0, length=70, troughcolor="#2a2a2a")
        s.set(val);
        s.pack();
        return s

    def select_any(self, key):
        path = filedialog.askopenfilename(filetypes=[("SRT", "*.srt")]) if key == "srt" else filedialog.askdirectory()
        if path:
            self.paths[key] = os.path.abspath(path)
            self.path_labels[key].config(text="已连接 ✔", fg=self.theme_cyan)
            base_ready = all(self.paths[k] != "" for k in ["a", "b", "v", "m", "t"])
            srt_ready = (not self.enable_srt_var.get()) or (self.paths["srt"] != "")
            if base_ready and srt_ready: self.run_btn.config(state="normal")

    def handle_font_selection(self):
        if "单一" in self.font_mode.get():
            f = filedialog.askopenfilename(initialdir="C:/Windows/Fonts", filetypes=[("Font", "*.ttf *.otf *.ttc")])
            if f: self.selected_font_path = f.replace("\\", "/"); self.selected_font_name = os.path.basename(
                f); self.font_status_lbl.config(text="单一: " + self.selected_font_name)
        else:
            d = filedialog.askdirectory()
            if d: self.paths["font_dir"] = os.path.abspath(d); self.font_status_lbl.config(
                text="目录: " + os.path.basename(d))
        """扫描目录并选中一个字体，更新界面标签和内部选择路径。"""
        try:
            fonts = [os.path.join(d, fn) for fn in os.listdir(d) if fn.lower().endswith(('.ttf', '.otf', '.ttc'))]
            if fonts:
                chosen = random.choice(fonts)
                self.selected_font_path = chosen.replace("\\", "/")
                self.selected_font_name = os.path.basename(chosen)
                # 如果 UI 已经构建，更新标签显示
                try:
                    self.font_status_lbl.config(text=f"目录: {os.path.basename(d)} | 当前: {self.selected_font_name}")
                except Exception:
                    pass
            else:
                self.selected_font_path = ""
                self.selected_font_name = "未找到字体"
                try:
                    self.font_status_lbl.config(text=f"目录: {os.path.basename(d)} | 未找到字体")
                except Exception:
                    pass
        except Exception:
            pass

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
                print(f"错误: ffprobe.exe 不存在 - {ffprobe_path}")
                return 10.0
            cmd = [ffprobe_path, '-v', 'quiet', '-print_format', 'json', '-show_format', file_path]
            res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            return float(json.loads(res.stdout)['format']['duration'])
        except Exception as e:
            print(f"获取时长异常: {str(e)}")
            return 10.0

    def start_thread(self):
        threading.Thread(target=self.batch_process, daemon=True).start()

    def show_final_report(self, logs):
        report_win = tk.Toplevel(self.root)
        report_win.title("奈尔森剪辑任务详情报告")
        report_win.geometry("550x650");
        report_win.configure(bg="#121212")
        tk.Label(report_win, text="🏆 奈尔森自动化流水线 - 任务报告", font=("Microsoft YaHei", 12, "bold"),
                 fg=self.theme_cyan, bg="#121212").pack(pady=15)
        area = scrolledtext.ScrolledText(report_win, bg="#1e1e1e", fg="#ffffff", font=("Consolas", 10), bd=0, padx=10,
                                         pady=10)
        area.pack(fill="both", expand=True, padx=15, pady=10)
        for line in logs: area.insert(tk.END, line + "\n" + "=" * 50 + "\n")
        area.configure(state='disabled')

    def batch_process(self):
        report_logs = []
        try:
            if "NVIDIA" in self.hw_mode.get():
                v_codec = "h264_nvenc";
                v_preset = "p1";
                hw_info = "⚡ NVIDIA GPU 加速"
            else:
                v_codec = "libx264";
                v_preset = "fast";
                hw_info = "🐢 兼容模式 (CPU)"

            def scan(d):
                return sorted(
                    [f for f in os.listdir(d) if f.lower().endswith(('.mp4', '.mov', '.mp3', '.wav', '.m4a'))])

            def scan_fonts(d):
                return [os.path.join(d, f) for f in os.listdir(d) if f.lower().endswith(('.ttf', '.otf', '.ttc'))]

            files_a, files_b = scan(self.paths["a"]), scan(self.paths["b"])
            v_files, m_files = scan(self.paths["v"]), scan(self.paths["m"])

            random_fonts = []
            if "随机" in self.font_mode.get() and self.paths["font_dir"]:
                random_fonts = scan_fonts(self.paths["font_dir"])

            self.run_btn.config(state="disabled", text="奈尔森引擎正在计算...")
            self.progress['maximum'] = len(files_a)

            srt_file_path = self.paths["srt"].replace("\\", "/").replace(":",
                                                                         "\\:") if self.enable_srt_var.get() else ""

            for index, name_a in enumerate(files_a):
                # 获取随机字体名称（使用系统字体名，不用路径）
                if random_fonts:
                    font_path = random.choice(random_fonts)
                    # 从路径提取字体名称（如 "C:\...\Impact.ttf" -> "Impact"）
                    font_basename = os.path.splitext(os.path.basename(font_path))[0]
                    font_name = font_basename
                else:
                    font_name = self.selected_font_name
                
                # 关键修复：使用系统字体名称而不是 fontfile 路径
                # FFmpeg drawtext 过滤器在 filter_complex 中对 fontfile 参数有限制
                # 改用 font 参数，传入系统字体名称（更稳定）

                title_c = "#{:06x}".format(
                    random.randint(0, 0xFFFFFF)) if self.random_color_var.get() else self.selected_color
                title_b_c = self.selected_border_color

                srt_final_filter = ""
                final_srt_color = "未开启";
                final_srt_border = "未开启"

                if self.enable_srt_var.get():
                    if self.random_color_var.get():
                        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                        srt_hex = f"#{r:02x}{g:02x}{b:02x}";
                        srt_b_hex = "#000000"
                    else:
                        srt_hex, srt_b_hex = self.srt_color, self.srt_border_color

                    final_srt_color = srt_hex;
                    final_srt_border = srt_b_hex
                    s_h, s_b_h = srt_hex.lstrip('#'), srt_b_hex.lstrip('#')
                    srt_color_ff = f"&H{s_h[4:6]}{s_h[2:4]}{s_h[0:2]}&"
                    srt_border_ff = f"&H{s_b_h[4:6]}{s_b_h[2:4]}{s_b_h[0:2]}&"

                    srt_final_filter = (
                        f",subtitles='{srt_file_path}':force_style='Fontsize={self.srt_size_scale.get()},"
                        f"PrimaryColour={srt_color_ff},OutlineColour={srt_border_ff},"
                        f"BorderStyle=1,Outline={self.srt_border_scale.get()},Shadow=0,Alignment=2,"
                        f"MarginV={self.srt_margin_scale.get()}'")

                # 获取用户设定的标题出现时间
                t_s, t_e = self.time_start.get(), self.time_end.get()

                # 报告信息：补齐标题出现时间
                report_logs.append(
                    f"视频序号: #{index + 1}\n文件名: {name_a}\n动力模式: {hw_info}\n"
                    f"【标题属性】\n  - 字体: {font_name}\n  - 颜色: {title_c}\n  - 描边: {title_b_c}\n"
                    f"  - 出现时间: {t_s}s - {t_e}s\n"
                    f"【字幕属性】\n  - 颜色: {final_srt_color}\n  - 描边: {final_srt_border}\n"
                    f"  - 垂直边距: {self.srt_margin_scale.get()}px"
                )

                eff = random.choice(
                    self.xfade_effects) if "随机" in self.effect_combo.get() else self.effect_combo.get()

                try:
                    in_a, in_b = os.path.join(self.paths["a"], name_a), os.path.join(self.paths["b"],
                                                                                     files_b[index % len(files_b)])
                    in_v, in_m = os.path.join(self.paths["v"], random.choice(v_files)), os.path.join(self.paths["m"],
                                                                                                     random.choice(
                                                                                                         m_files))
                    out_p = os.path.join(self.paths["t"], f"Nelson_Output_{index + 1}.mp4")

                    # 检查输入文件是否存在
                    for fp, fname in [(in_a, "视频A"), (in_b, "视频B"), (in_v, "解说"), (in_m, "BGM")]:
                        if not os.path.exists(fp):
                            report_logs.append(f"❌ 文件不存在: {fname} - {fp}")
                            raise FileNotFoundError(f"文件不存在: {fp}")

                    d_a = self.get_duration(in_a) / 1.2;
                    off = max(0.1, (d_a - 1.5))

                    # 动态时间 alpha 表达式
                    alpha_exp = f"if(lt(t,{t_s}),0,if(lt(t,{t_s}+1),t-{t_s},if(lt(t,{t_e}-1),1,if(lt(t,{t_e}),{t_e}-t,0))))"

                    # 关键修复：用 font 参数（系统字体名称）而不是 fontfile（路径）
                    # 这样避免了 filter_complex 中路径特殊字符的解析问题
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
                        report_logs.append(f"❌ ffmpeg.exe 不存在: {ffmpeg_path}")
                        raise FileNotFoundError(f"ffmpeg.exe 不存在: {ffmpeg_path}")

                    cmd = [ffmpeg_path, '-y', '-hwaccel', 'auto', '-i', in_a, '-i', in_b, '-i', in_v,
                           '-stream_loop', '-1', '-i', in_m,
                           '-filter_complex', f_str, '-map', '[v_out]', '-map', '[a_out]', '-c:v', v_codec,
                           '-preset', v_preset, '-t', f"{(d_a + self.get_duration(in_b) - 2.5):.2f}", out_p]
                    # 打印命令和错误输出，便于排查
                    print("FFmpeg 命令：", " ".join(cmd))
                    result = subprocess.run(cmd, capture_output=True, text=True, errors='ignore')
                    if result.returncode != 0:
                        print("FFmpeg 错误输出：", result.stderr)
                        report_logs.append(f"❌ FFmpeg 执行失败: {result.stderr}")
                except Exception as e:
                    print("批处理异常：", str(e))
                    report_logs.append(f"❌ 批处理异常: {str(e)}")
                self.progress['value'] = index + 1;
                self.root.update_idletasks()
            self.show_final_report(report_logs)
        finally:
            self.run_btn.config(state="normal", text="一键执行全自动化剪辑")
            self.progress['value'] = 0

    def on_closing(self):
        for proc in psutil.process_iter(['name']):
            try:
                if "ffmpeg" in (proc.info['name'] or "").lower(): proc.kill()
            except:
                pass
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk();
    app = NelsonBatchStitcher(root);
    root.mainloop()