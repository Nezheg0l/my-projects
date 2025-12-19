# 🛡️ Deep-Fake Ecosystem: Autonomous AI Honeypot & Self-Healing Infrastructure

An advanced AI-driven cybersecurity ecosystem deployed on an air-gapped server. This project merges **Active Defense (Deception)** with **Self-Healing architectures**.

## 🚀 Overview
Traditional security is reactive. This framework is **proactive**. It doesn't just block attacks; it deceives attackers, studies their behavior, and automatically repairs the underlying vulnerabilities using local LLMs.

### 🧠 Core Features
1. **Self-Healing Logic:** Autonomous detection of SQLi/RCE. The system analyzes the breach, writes a secure patch (Qwen2.5-Coder), runs regression tests, and redeploys via Docker.
2. **Generative Honeypot:** Instead of a 403 error, the attacker is redirected to a simulated environment. The AI (Dolphin-Llama3) generates realistic terminal responses to keep the attacker engaged.
3. **Psychological Countermeasures:** If an attacker tries to exfiltrate "bait files" (e.g., `passwords.txt`), the system triggers a **Rickroll payload**, marking the attack as detected and demoralizing the intruder.

## 🛠️ Technical Stack
- **OS:** Ubuntu 24.04 LTS (Local Air-gapped Server)
- **Hardware:** NVIDIA RTX 3060 Ti (CUDA 12.x)
- **AI Engine:** Ollama (Dolphin-Llama3 & Qwen2.5-Coder)
- **Orchestration:** Docker, Python 3.11, Flask

## 📸 Proof of Concept

### Phase 1: AI Code Patching (v1)
Demonstrated the ability to rewrite vulnerable code into secure, parameterized structures.

### Phase 2: Generative Active Defense (v2)
Captured logs showing the Honeypot intercepting `ls` and `cat` commands, followed by a triggered Rickroll redirect.
![Honeypot Logs](./assets/honeypot_v2.jpg)

## 🏆 Engineering Highlights
- **Zero-Latency Deception:** AI-generated terminal responses provide an immersive trap for automated scripts.
- **On-Premise Privacy:** 100% of the computation happens locally. No data leaves the server.
- **Fail-Safe Orchestration:** Includes an automatic Rollback mechanism if an AI-generated patch fails QA tests.
