# UI UX Pro Max - Design System Skill

## Purpose
Generate professional, production-ready UI/UX designs with industry-specific design systems, color palettes, typography, and best practices.

## Key Features
- 57 UI Styles (Glassmorphism, Claymorphism, Minimalism, Neumorphism, etc.)
- 95 Color Palettes (SaaS, E-commerce, Healthcare, Fintech, Beauty, etc.)
- 56 Font Pairings (Google Fonts)
- 100 Industry-Specific Reasoning Rules
- 98 UX Guidelines and Anti-patterns
- Support for multiple tech stacks (React, Next.js, Vue, Tailwind, etc.)

## How to Use

### Basic Usage
When a user requests UI/UX work, use the design system to:

1. **Identify the product type** - SaaS, E-commerce, Healthcare, Beauty, etc.
2. **Search design system** - Find matching styles, colors, typography
3. **Generate complete design system** - Provide pattern, style, colors, fonts, effects
4. **Implement code** - Create production-ready code with best practices
5. **Pre-delivery checks** - Validate accessibility, responsiveness, animations

### Example Request
"Build a landing page for my beauty spa"

### Expected Response Format
Provide:
- Recommended Pattern (Hero-Centric + Social Proof)
- Style (Soft UI Evolution with specific keywords)
- Color Palette (Primary, Secondary, CTA, Background, Text)
- Typography (Font names with mood/purpose)
- Key Effects (Animations, transitions, hover states)
- Anti-Patterns (What NOT to do)
- Pre-delivery Checklist (Accessibility, responsive breakpoints, etc.)

## Design System Location
Look for design system data at:
- `.shared/ui-ux-pro-max/data/styles.json`
- `.shared/ui-ux-pro-max/data/colors.json`
- `.shared/ui-ux-pro-max/data/typography.json`
- `.shared/ui-ux-pro-max/data/reasoning_rules.json`

## Supported Stacks
- HTML + Tailwind CSS (default)
- React / Next.js / shadcn/ui
- Vue / Nuxt.js / Nuxt UI
- Svelte
- SwiftUI
- React Native
- Flutter

## Key Principles
1. No emojis as icons (use SVG: Heroicons, Lucide)
2. cursor-pointer on all clickable elements
3. Smooth transitions (150-300ms)
4. Accessible color contrast (4.5:1 minimum for light mode)
5. Focus states visible for keyboard navigation
6. Respect prefers-reduced-motion
7. Responsive design (375px, 768px, 1024px, 1440px breakpoints)
