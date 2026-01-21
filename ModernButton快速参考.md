# ModernButton 快速参考指南

## 🎯 核心概念 - 30秒速览

```python
# 导入和使用
from videotestNewUI import ModernButton

# 三种按钮类型
ModernButton(parent, text="文字", button_type="primary")    # 橙色 - 主操作
ModernButton(parent, text="文字", button_type="secondary")  # 蓝灰 - 次操作  
ModernButton(parent, text="文字", button_type="danger")     # 红色 - 危险操作
```

---

## 📦 完整参数表

```python
ModernButton(
    parent,                    # 父容器
    text="按钮文字",          # 显示的文本（可含emoji）
    button_type="secondary",  # 类型: "primary" / "secondary" / "danger"
    command=callback,         # 点击时调用的函数
    width=10,                 # 按钮宽度（字符数）
    bg="#FF6B35",            # 自定义背景色（可选）
    fg="#FFFFFF",            # 自定义文字色（可选）
    font=("Arial", 10, "bold"), # 自定义字体（可选）
    padx=12,                 # 左右内边距（默认 12）
    pady=8,                  # 上下内边距（默认 8）
)
```

---

## 🎨 三种类型速查

### Primary（主操作）- 橙色

```python
btn = ModernButton(frame, text="▶ 执行", button_type="primary")
btn.pack(fill="x")
```

**颜色系统：**
```
默认:   #FF6B35 (橙色)
Hover:  #FF8557 (亮橙)
Active: #E55A24 (深橙)
```

**用途：**
- 页面最重要的操作
- 一页面最多 1 个
- 示例：执行、提交、保存

---

### Secondary（次操作）- 蓝灰色

```python
btn = ModernButton(frame, text="导入字体", button_type="secondary", width=12)
btn.pack(side="left", padx=4)
```

**颜色系统：**
```
默认:   #2A3F6B (深蓝灰)
Hover:  #3A5A8B (亮蓝灰)  
Active: #1A2F5B (更深)
```

**用途：**
- 辅助功能
- 可多个并排
- 示例：导入、选择、预览

---

### Danger（危险操作）- 红色

```python
btn = ModernButton(frame, text="删除", button_type="danger")
btn.pack()
```

**颜色系统：**
```
默认:   #EE5A6F (红色)
Hover:  #FF6B7D (亮红)
Active: #DD4956 (深红)
```

**用途：**
- 破坏性操作
- 需要确认
- 示例：删除、重置、清空

---

## 🔄 交互效果可视化

```
鼠标悬停 (Hover)
    ↓
背景色变亮 + 边框浮起 (relief="raised")
    ↓
点击鼠标 (Press)
    ↓
背景色变深 + 边框下压 (relief="sunken")
    ↓
释放鼠标 (Release)
    ↓
恢复 Hover 状态 (保持亮色)
    ↓
鼠标离开
    ↓
恢复默认状态 (relief="solid")
```

---

## ⚙️ 常见操作

### 启用/禁用按钮

```python
# 创建按钮
btn = ModernButton(frame, text="执行", button_type="primary")
btn.pack()

# 禁用
btn.set_disabled(True)   # 变灰，点击无效

# 启用
btn.set_disabled(False)  # 恢复颜色，可点击
```

### 修改按钮文字

```python
btn.config(text="新文字")  # 实时更新显示
```

### 修改按钮命令

```python
btn.config(command=new_callback)  # 改变点击事件
```

### 修改按钮状态

```python
# 完整的状态管理
if ready:
    btn.set_disabled(False)
    btn.config(text="▶ 执行")
else:
    btn.set_disabled(True)
    btn.config(text="等待配置...")
```

---

## 🎪 实战例子

### 例 1: 按钮组

```python
# 创建多个按钮在同一行
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

ModernButton(btn_frame, text="导入", button_type="secondary", width=8).pack(side="left", padx=4)
ModernButton(btn_frame, text="预览", button_type="secondary", width=8).pack(side="left", padx=4)
ModernButton(btn_frame, text="导出", button_type="primary", width=8).pack(side="left", padx=4)
```

### 例 2: 条件启用

```python
# 配置表单
form_frame = tk.Frame(root)
form_frame.pack(pady=20)

# 输入框
tk.Label(form_frame, text="用户名:").pack()
username = tk.Entry(form_frame)
username.pack()

tk.Label(form_frame, text="密码:").pack()
password = tk.Entry(form_frame, show="*")
password.pack()

# 按钮 - 初始禁用
submit_btn = ModernButton(form_frame, text="登录", button_type="primary")
submit_btn.pack(pady=10)
submit_btn.set_disabled(True)

# 检查输入
def check_input(*args):
    if username.get() and password.get():
        submit_btn.set_disabled(False)
    else:
        submit_btn.set_disabled(True)

username.bind("<KeyRelease>", check_input)
password.bind("<KeyRelease>", check_input)
```

### 例 3: 长耗时操作

```python
def start_processing():
    btn.set_disabled(True)
    btn.config(text="处理中...")
    
    # 后台处理
    def do_work():
        # 长耗时操作
        time.sleep(3)
        
        # UI 线程中更新
        btn.config(text="✓ 完成")
        btn.set_disabled(False)
    
    threading.Thread(target=do_work, daemon=True).start()

btn = ModernButton(root, text="开始处理", command=start_processing, button_type="primary")
btn.pack()
```

---

## 🎨 自定义颜色

### 方法 1: 创建按钮时指定

```python
# 完全自定义颜色
btn = ModernButton(
    frame, 
    text="自定义按钮",
    button_type="secondary",
    bg="#FF00FF",      # 紫色背景
    fg="#FFFF00"       # 黄色文字
)
```

### 方法 2: 修改类的颜色方案

```python
# 在 ModernButton 类中修改颜色常量
# 修改 __init__ 方法中的颜色定义

class ModernButton(tk.Button):
    def __init__(self, parent, text, button_type="secondary", **kwargs):
        # 修改这些颜色值
        if button_type == "primary":
            self.base_bg = "#YOUR_COLOR"        # 你的主色
            self.hover_bg = "#YOUR_HOVER_COLOR" # 你的 Hover 色
            # ...
```

---

## 📏 尺寸参考

### 常用尺寸组合

```python
# 小按钮 - 导入/删除/清空
ModernButton(..., width=6, padx=8, pady=6)

# 中等按钮 - 选择/浏览/编辑
ModernButton(..., width=10, padx=12, pady=8)

# 大按钮 - 主操作（执行/提交）
ModernButton(..., width=20, padx=15, pady=12, font=("Arial", 12, "bold"))

# 超大按钮 - 页面底部主按钮
ModernButton(..., padx=15, pady=12, font=("Arial", 14, "bold"))
```

---

## 🐛 常见问题

### Q: 如何改变按钮宽度？

```python
# 方法 1: width 参数
ModernButton(..., width=20)  # 按字符数

# 方法 2: pack 时指定
btn = ModernButton(...)
btn.pack(fill="x")  # 填满宽度
```

### Q: Hover 效果不显示？

```python
# 确保父容器设置了背景色
frame = tk.Frame(root, bg="#0A0E27")
btn = ModernButton(frame, ...)
```

### Q: 如何检测按钮是否被禁用？

```python
if btn.is_disabled:
    print("按钮已禁用")
else:
    print("按钮可用")
```

### Q: 如何快速创建多个类似的按钮？

```python
buttons = {}
for i, name in enumerate(['导入', '导出', '删除']):
    buttons[name] = ModernButton(
        frame, 
        text=name,
        button_type="secondary" if name != '删除' else "danger",
        width=8
    )
    buttons[name].pack(side="left", padx=4)

# 之后可以这样使用
buttons['导入'].config(command=import_func)
buttons['导出'].config(command=export_func)
buttons['删除'].config(command=delete_func)
```

---

## 📚 完整属性列表

| 属性 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `button_type` | str | "primary" / "secondary" / "danger" | `"primary"` |
| `text` | str | 按钮显示文本 | `"执行"` |
| `command` | func | 点击时调用的函数 | `self.on_click` |
| `width` | int | 宽度（字符数）| `10` |
| `padx` | int | 左右内边距 | `12` |
| `pady` | int | 上下内边距 | `8` |
| `bg` | str | 自定义背景色 | `"#FF6B35"` |
| `fg` | str | 自定义文字色 | `"#FFFFFF"` |
| `font` | tuple | 字体定义 | `("Arial", 10, "bold")` |
| `is_disabled` | bool | 是否被禁用 | `True/False` |

---

## 💾 源代码位置

文件：`videotestNewUI.py`

位置：第 24-105 行

```python
class ModernButton(tk.Button):
    """现代化按钮类，支持三种类型和完整交互效果"""
    def __init__(self, parent, text, button_type="secondary", **kwargs):
        # ... 实现代码
```

---

## 🔗 相关文件

- 📄 [按钮设计改进方案.md](按钮设计改进方案.md) - 详细设计文档
- 📄 [按钮改进对比分析.md](按钮改进对比分析.md) - 改进前后对比
- 📝 [videotestNewUI.py](videotestNewUI.py) - 源代码

---

## 🎓 进阶话题

### 如何扩展 ModernButton？

```python
# 添加图标支持
class ModernButtonWithIcon(ModernButton):
    def __init__(self, parent, text, icon_path, **kwargs):
        # 首先加载图标
        self.icon = tk.PhotoImage(file=icon_path)
        # 调用父类初始化
        super().__init__(parent, text, **kwargs)
        # 设置图标
        self.config(image=self.icon, compound="left")
```

### 如何创建动画按钮？

```python
def animate_button(btn, duration=1):
    start_time = time.time()
    
    def animate():
        elapsed = time.time() - start_time
        progress = elapsed / duration
        
        if progress < 1:
            # 计算中间颜色
            btn.update_idletasks()
            root.after(50, animate)
        else:
            btn.config(bg=btn.base_bg)
    
    animate()
```

---

**最后更新：** 2025-01-19  
**版本：** 1.0  
**适用于：** videotestNewUI.py v8.8.0+
