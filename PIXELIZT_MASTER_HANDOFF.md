# Pixelizt SOP Portal — Master Handoff

## 1. Project Overview
This repository contains the source code and documentation for **app.pixelizt.com**, the internal SOP (Standard Operating Procedure) portal for the Pixelizt Website and SEO Agency.

**Tech Stack:**
- **Framework:** React + Vite + TypeScript
- **Styling:** Vanilla CSS + x.ai design system (`DESIGN.md`)
- **Content:** Markdown (MDX/React-Markdown) for SOPs, Mermaid.js for flowcharts, and custom components for Loom video embeds.

## 2. Architecture & Design Principles
- **Markdown-Driven:** All SOPs live in `src/content/{category}/`. The app dynamically parses these files.
- **Rich Media:** SOPs natively support Loom video embeds (via custom markdown directives or React components) and flowcharts (via Mermaid syntax ` ```mermaid `).
- **Navigation:** A persistent sidebar categorizes SOPs (Sales, SEO, Marketing, Operations). Clicking a category displays all relevant SOPs.
- **Design System:** We strictly follow the `DESIGN.md` guidelines (inspired by x.ai) for a sleek, minimal, and highly professional internal tool.

## 3. Strict AI Rules (MANDATORY FOR ALL AGENTS)

### Rule A: Auto-Recording Chat History
EVERY SINGLE reply or action taken by an AI agent must be logged in the `/chat_history/` directory.
1. Format: `YYYY-MM-DD_session_XX.md`
2. Include the exact user request and a detailed summary of actions taken, files modified, and rationale.
3. This is non-negotiable.

### Rule B: Read Before Writing
Any new AI agent joining this repository MUST read this `PIXELIZT_MASTER_HANDOFF.md` and the most recent `chat_history` files BEFORE executing any commands or making changes.

### Rule C: Design Adherence
Do NOT invent new CSS patterns. Always consult `DESIGN.md` and use the established tokens and component styles.

## 4. Current State & Next Steps
- **Phase 1 (Current):** Initialized Vite React project, added x.ai design system, established handoff protocols.
- **Phase 2:** Implement React Router, Markdown parsing (`react-markdown`, `remark-gfm`), Mermaid integration, and Loom embed component.
- **Phase 3:** Build the UI shell (Sidebar + Content area) and populate initial SOPs for Sales.

## 5. Deployment
This app will eventually be deployed and connected to `app.pixelizt.com`. Keep build artifacts optimized.
