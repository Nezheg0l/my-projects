# Autonomous AI Cyber-Defense Framework

This project evolved from a simple concept of AI-driven code patching to a fully autonomous defense orchestration system.

## 🏗️ Evolution of the Project

### Phase 1: Proof of Concept (v1)
**Goal:** Demonstrate that a local LLM can identify vulnerabilities and generate secure patches in real-time.
- **Features:** Streamlit-based UI, manual vulnerability input, AI-driven code rewriting.
- **Outcome:** Successfully proved that LLMs can replace unsafe functions (like `os.popen`) with secure alternatives (like `subprocess.run`).

![Version 1 Demo](./assets/demo_v1.jpg) 
*(Above: Screenshot of the v1 dashboard showing the AI-generated patch(sorry bad photo))*

### Phase 2: Autonomous Framework (v2)
**Goal:** Remove human intervention and create a "Self-Healing" environment.
- **Features:** 
    - **Red Team Agent:** Automatically attacks the target.
    - **Blue Team Agent:** Analyzes logs and patches code.
    - **Orchestrator:** Manages Docker containers, runs regression tests, and handles rollbacks.
- **Outcome:** A complete CI/CD pipeline for security that fixes itself when under attack.
