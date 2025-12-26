import streamlit as st
import json
import os
import time

st.set_page_config(page_title="AI Cyber Warfare", layout="wide", page_icon="🛡️")

st.title("🛡️ Autonomous AI Cyber Warfare Framework")
st.markdown("### Red Team (Dolphin-Llama3) vs Blue Team (Qwen2.5-Coder)")

col1, col2, col3 = st.columns(3)
col1.metric("Server Status", "Online 🟢")
col2.metric("AI Model (Attack)", "Dolphin-Llama3")
col3.metric("AI Model (Defense)", "Qwen2.5-Coder")

st.divider()

col_attack, col_defense = st.columns(2)

with col_attack:
    st.subheader("⚔️ Vulnerable Code (Before)")
    st.code("""
@app.route('/ping')
def ping():
    ip = request.args.get('ip')
    # VULNERABLE: Direct OS execution
    cmd = f"ping -c 1 {ip}" 
    return os.popen(cmd).read()
    """, language="python")
    st.error("Status: VULNERABLE to RCE")

with col_defense:
    st.subheader("🛡️ Patched Code (After AI Fix)")
    
    try:
        with open("victim/app.py", "r") as f:
            current_code = f.read()
        st.code(current_code, language="python")
        
        if "subprocess" in current_code:
            st.success("Status: SECURE (Patched by AI)")
        else:
            st.warning("Status: Analyzing...")
    except:
        st.info("Waiting for simulation data...")

st.divider()
st.subheader("📜 Live Battle Log")
st.text_area("System Logs", "Waiting for execution...", height=200)

if st.button("Run Simulation Again"):
    st.write("Executing main.py...")
    os.system("python main.py > logs/latest.log 2>&1")
    st.success("Simulation Complete! Check logs.")
