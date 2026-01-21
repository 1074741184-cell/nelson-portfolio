# UI UX Pro Max - GitHub Copilot Setup

## Installation Status: ✅ COMPLETE

### What's Installed

您已成功为项目配置了 UI UX Pro Max 设计系统技能。

```
.github/
└── prompts/
    └── ui-ux-pro-max.prompt.md          ← GitHub Copilot 提示文件

.shared/
└── ui-ux-pro-max/
    ├── data/
    │   ├── styles.json                  ← 57 种 UI 风格
    │   ├── colors.json                  ← 95 个配色方案
    │   ├── typography.json              ← 56 套字体组合
    │   └── reasoning_rules.json         ← 100 条行业推理规则
    └── README.md
```

## 如何使用

在 GitHub Copilot 中，使用 `/ui-ux-pro-max` 前缀来调用该技能：

```
/ui-ux-pro-max Build a landing page for my SaaS product
```

### 示例提示

```
/ui-ux-pro-max Build a landing page for a beauty spa with booking functionality

/ui-ux-pro-max Create a modern dashboard for fintech analytics

/ui-ux-pro-max Design a portfolio website with dark mode support

/ui-ux-pro-max Build an e-commerce product page with mobile responsiveness
```

## 完整安装方式

如果之后想使用完整的 CLI 工具，可以：

1. **确保已安装 Node.js**
   ```
   node --version
   npm --version
   ```

2. **全局安装 uipro-cli**
   ```
   npm install -g uipro-cli
   ```

3. **在项目目录运行**
   ```
   uipro init --ai copilot
   ```

## 功能概览

✅ **57 种 UI 风格**
- Glassmorphism, Claymorphism, Neumorphism, Minimalism, Brutalism, Bento Grid, Dark Mode 等

✅ **95 个配色方案**
- 针对 SaaS, E-commerce, Healthcare, Fintech, Beauty, Creative 等行业

✅ **56 套字体组合**
- Google Fonts 精选配对，适配各种设计风格

✅ **100 条行业推理规则**
- 针对不同行业的设计建议和最佳实践

✅ **98 个 UX 准则**
- 可访问性规则、反模式、最佳实践

## 支持的技术栈

- HTML + Tailwind CSS（默认）
- React / Next.js / shadcn/ui
- Vue / Nuxt.js / Nuxt UI
- Svelte
- SwiftUI
- React Native
- Flutter

## 核心原则

1. ✅ 无表情符号作为图标（使用 SVG: Heroicons, Lucide）
2. ✅ 所有可点击元素都有 cursor-pointer
3. ✅ 平滑过渡（150-300ms）
4. ✅ 可访问性色彩对比（浅色模式最小 4.5:1）
5. ✅ 键盘导航的焦点状态可见
6. ✅ 尊重 prefers-reduced-motion
7. ✅ 响应式设计（375px, 768px, 1024px, 1440px 断点）

## 故障排除

**问题：Copilot 中看不到 /ui-ux-pro-max？**

- 确保已保存 `.github/prompts/ui-ux-pro-max.prompt.md` 文件
- 在 Copilot 聊天中刷新或重启 VS Code
- 尝试在聊天中输入 `/` 查看所有可用命令

**问题：需要完整的搜索脚本？**

- 运行 `uipro init --ai copilot` 获取完整的 Python 搜索脚本
- 需要 Python 3.x（已安装：3.13.1）

## 相关资源

- 项目主页：https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- 文档：https://ui-ux-pro-max-skill.nextlevelbuilder.io/
- NPM 包：https://www.npmjs.com/package/uipro-cli

---

**安装完成于：2026-01-21**
**状态：就绪，可以开始使用**
