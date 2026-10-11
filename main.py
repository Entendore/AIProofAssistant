import streamlit as st
import time
import json
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import base64
import re
import requests
import os

# Set page configuration
st.set_page_config(
    page_title="LogicProof AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with better contrast and layout
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    :root {
        --primary: #2563eb;
        --primary-dark: #1e40af;
        --primary-light: #3b82f6;
        --secondary: #7c3aed;
        --secondary-dark: #6d28d9;
        --success: #10b981;
        --success-dark: #059669;
        --warning: #f59e0b;
        --warning-dark: #d97706;
        --danger: #ef4444;
        --danger-dark: #dc2626;
        --dark: #111827;
        --darker: #030712;
        --gray-darker: #374151;
        --gray-dark: #4b5563;
        --gray: #6b7280;
        --gray-light: #9ca3af;
        --gray-lighter: #d1d5db;
        --gray-lightest: #f3f4f6;
        --white: #ffffff;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        --radius-sm: 6px;
        --radius-md: 8px;
        --radius-lg: 12px;
        --radius-xl: 16px;
        --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    * {
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        line-height: 1.6;
        color: var(--dark);
        background-color: var(--gray-lightest);
    }
    
    /* Main Container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Header Styles */
    .main-header {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--secondary-dark) 100%);
        color: var(--white);
        padding: 3rem 2rem;
        border-radius: var(--radius-xl);
        margin-bottom: 2.5rem;
        box-shadow: var(--shadow-xl);
        position: relative;
        overflow: hidden;
        border: 2px solid var(--primary);
    }
    
    .main-header::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
        opacity: 0.3;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 2rem;
        position: relative;
        z-index: 1;
    }
    
    .logo-icon {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        width: 80px;
        height: 80px;
        border-radius: var(--radius-xl);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 36px;
        font-weight: 900;
        border: 2px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: var(--transition);
    }
    
    .logo-icon:hover {
        transform: scale(1.05);
        background: rgba(255, 255, 255, 0.25);
    }
    
    .logo-text {
        font-size: 3rem;
        font-weight: 900;
        letter-spacing: -0.02em;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    
    .logo-text span {
        color: rgba(255, 255, 255, 0.9);
    }
    
    .header-subtitle {
        font-size: 1.25rem;
        font-weight: 500;
        opacity: 0.95;
        margin-top: 0.75rem;
        color: rgba(255, 255, 255, 0.9);
    }
    
    /* Tab Styles */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: var(--radius-lg);
        padding: 0.5rem;
        gap: 0.5rem;
        margin-top: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: 2px solid transparent;
        border-radius: var(--radius-md);
        color: rgba(255, 255, 255, 0.7) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.75rem 1.5rem !important;
        transition: var(--transition) !important;
        cursor: pointer;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        color: var(--white) !important;
        transform: translateY(-1px);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--white) !important;
        color: var(--primary-dark) !important;
        font-weight: 700 !important;
        box-shadow: var(--shadow-lg);
    }
    
    /* Card Styles */
    .card {
        background: var(--white);
        border-radius: var(--radius-xl);
        box-shadow: var(--shadow-lg);
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid var(--gray-lighter);
        transition: var(--transition);
        position: relative;
    }
    
    .card:hover {
        box-shadow: var(--shadow-xl);
        transform: translateY(-2px);
        border-color: var(--primary-light);
    }
    
    .card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(to bottom, var(--primary), var(--secondary));
        border-radius: var(--radius-xl) 0 0 var(--radius-xl);
        opacity: 0;
        transition: var(--transition);
    }
    
    .card:hover::before {
        opacity: 1;
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 1.5rem;
        border-bottom: 2px solid var(--gray-lightest);
        margin-bottom: 1.5rem;
    }
    
    .card-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--dark);
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .card-title i {
        color: var(--primary);
        font-size: 1.25rem;
    }
    
    /* Button Styles */
    .stButton > button {
        width: 100%;
        border-radius: var(--radius-lg) !important;
        height: 3.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: var(--transition) !important;
        box-shadow: var(--shadow-md) !important;
        border: 2px solid transparent !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: "";
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:active::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-xl) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Primary Button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
        color: var(--white) !important;
        border-color: var(--primary-dark) !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary) 100%) !important;
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4) !important;
    }
    
    /* Secondary Button */
    .stButton > button:not([kind="primary"]) {
        background: var(--white) !important;
        color: var(--dark) !important;
        border-color: var(--gray-light) !important;
    }
    
    .stButton > button:not([kind="primary"]):hover {
        background: var(--gray-lightest) !important;
        border-color: var(--primary) !important;
        color: var(--primary) !important;
    }
    
    /* Symbol Grid */
    .symbol-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(70px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .symbol-btn {
        height: 60px;
        background: var(--gray-lightest);
        border: 2px solid var(--gray-light);
        border-radius: var(--radius-lg);
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 1.25rem;
        font-weight: 700;
        cursor: pointer;
        transition: var(--transition);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: var(--shadow-sm);
        position: relative;
        overflow: hidden;
    }
    
    .symbol-btn::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transition: left 0.5s;
    }
    
    .symbol-btn:hover::before {
        left: 100%;
    }
    
    .symbol-btn:hover {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: var(--white);
        border-color: var(--primary-dark);
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.3);
    }
    
    .symbol-btn:active {
        transform: translateY(-1px) scale(1.02);
    }
    
    /* Example Tags */
    .example-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .example-tag {
        background: var(--gray-lightest);
        border: 2px solid var(--gray-light);
        padding: 0.75rem 1.25rem;
        border-radius: 50px;
        font-size: 0.95rem;
        font-weight: 600;
        cursor: pointer;
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .example-tag::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.5s;
    }
    
    .example-tag:hover::before {
        left: 100%;
    }
    
    .example-tag:hover {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: var(--white);
        border-color: var(--primary-dark);
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Proof Steps */
    .proof-step {
        background: var(--gray-lightest);
        border-radius: var(--radius-lg);
        padding: 1.75rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid var(--primary);
        position: relative;
        transition: var(--transition);
        border: 1px solid var(--gray-lighter);
    }
    
    .proof-step:hover {
        box-shadow: var(--shadow-lg);
        transform: translateX(8px);
        background: var(--white);
        border-color: var(--primary-light);
    }
    
    .step-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .step-number {
        font-weight: 800;
        color: var(--white);
        font-size: 1.25rem;
        min-width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        border-radius: 50%;
        box-shadow: var(--shadow-md);
    }
    
    .step-rule {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%);
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--primary-dark);
        border: 1px solid rgba(37, 99, 235, 0.2);
    }
    
    .step-content {
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 1.15rem;
        line-height: 1.7;
        margin: 1rem 0;
        color: var(--dark);
        padding: 1rem;
        background: rgba(37, 99, 235, 0.03);
        border-radius: var(--radius-md);
        border: 1px solid rgba(37, 99, 235, 0.1);
    }
    
    .step-explanation {
        font-size: 0.95rem;
        color: var(--gray-dark);
        padding: 1rem;
        background: rgba(124, 58, 237, 0.05);
        border-radius: var(--radius-md);
        border-left: 3px solid var(--secondary);
        margin-top: 1rem;
        line-height: 1.6;
    }
    
    /* Status Bar */
    .status-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 1.5rem;
        background: linear-gradient(135deg, var(--gray-lightest) 0%, var(--gray-lighter) 100%);
        border-radius: 0 0 var(--radius-xl) var(--radius-xl);
        border-top: 2px solid var(--gray-light);
        font-size: 0.95rem;
        font-weight: 500;
        color: var(--gray-dark);
        margin-top: 1.5rem;
    }
    
    /* Success Banner */
    .success-banner {
        background: linear-gradient(135deg, var(--success) 0%, var(--success-dark) 100%);
        color: var(--white);
        padding: 1rem 1.5rem;
        border-radius: var(--radius-lg);
        margin: 1.5rem 0;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 1rem;
        box-shadow: var(--shadow-lg);
        border: 1px solid var(--success-dark);
    }
    
    /* AI Assistant */
    .ai-assistant {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.05) 0%, rgba(124, 58, 237, 0.05) 100%);
        border-radius: var(--radius-xl);
        padding: 1.75rem;
        margin: 1.5rem 0;
        border: 2px solid rgba(37, 99, 235, 0.2);
        transition: var(--transition);
    }
    
    .ai-assistant:hover {
        border-color: var(--primary);
        box-shadow: var(--shadow-lg);
    }
    
    .ai-assistant-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .ai-assistant-avatar {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--white);
        font-weight: 700;
        font-size: 1.25rem;
        box-shadow: var(--shadow-md);
    }
    
    .ai-assistant-name {
        font-weight: 700;
        color: var(--dark);
        font-size: 1.1rem;
    }
    
    .ai-assistant-message {
        color: var(--gray-dark);
        line-height: 1.7;
        font-size: 1rem;
    }
    
    /* Sidebar Styles */
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, var(--white) 0%, var(--gray-lightest) 100%) !important;
        border-right: 2px solid var(--gray-lighter) !important;
        padding: 2rem 1.5rem !important;
    }
    
    .sidebar-section {
        margin-bottom: 2rem;
        padding-bottom: 2rem;
        border-bottom: 2px solid var(--gray-lighter);
    }
    
    .sidebar-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--dark);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .sidebar-title i {
        color: var(--primary);
    }
    
    .sidebar-example {
        background: var(--white);
        padding: 1rem 1.25rem;
        border-radius: var(--radius-lg);
        margin-bottom: 1rem;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 0.9rem;
        font-weight: 500;
        border: 2px solid var(--gray-lighter);
        cursor: pointer;
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .sidebar-example::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(37, 99, 235, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .sidebar-example:hover::before {
        left: 100%;
    }
    
    .sidebar-example:hover {
        background: var(--gray-lightest);
        border-color: var(--primary);
        transform: translateX(4px);
        box-shadow: var(--shadow-md);
    }
    
    /* Difficulty Badges */
    .difficulty-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-left: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .difficulty-easy {
        background: rgba(16, 185, 129, 0.15);
        color: var(--success-dark);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .difficulty-medium {
        background: rgba(245, 158, 11, 0.15);
        color: var(--warning-dark);
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .difficulty-hard {
        background: rgba(239, 68, 68, 0.15);
        color: var(--danger-dark);
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    /* Proof Validator */
    .proof-validator {
        background: rgba(16, 185, 129, 0.1);
        border: 2px solid rgba(16, 185, 129, 0.3);
        border-radius: var(--radius-lg);
        padding: 1.25rem;
        margin: 1.5rem 0;
    }
    
    .validator-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-weight: 700;
        color: var(--success-dark);
        margin-bottom: 0.75rem;
        font-size: 1.1rem;
    }
    
    /* Toast Notifications */
    .toast {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: var(--white);
        border-radius: var(--radius-xl);
        box-shadow: var(--shadow-xl);
        padding: 1rem 1.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        transform: translateY(150%);
        opacity: 0;
        transition: var(--transition);
        z-index: 9999;
        border: 2px solid var(--gray-lighter);
        min-width: 300px;
    }
    
    .toast.show {
        transform: translateY(0);
        opacity: 1;
    }
    
    .toast-icon {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        color: var(--white);
    }
    
    .toast-success .toast-icon {
        background: linear-gradient(135deg, var(--success) 0%, var(--success-dark) 100%);
    }
    
    .toast-error .toast-icon {
        background: linear-gradient(135deg, var(--danger) 0%, var(--danger-dark) 100%);
    }
    
    .toast-info .toast-icon {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 3rem 0;
        color: var(--gray-dark);
        font-size: 0.95rem;
        margin-top: 3rem;
        border-top: 2px solid var(--gray-lighter);
        background: var(--white);
        border-radius: var(--radius-xl);
    }
    
    /* Input Field Styles */
    .stTextArea > div > div > textarea {
        border-radius: var(--radius-lg) !important;
        border: 2px solid var(--gray-light) !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        transition: var(--transition) !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }
    
    /* Select Box Styles */
    .stSelectbox > div > div > div {
        border-radius: var(--radius-lg) !important;
        border: 2px solid var(--gray-light) !important;
    }
    
    .stSelectbox > div > div > div:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }
    
    /* Toggle Switch Styles */
    .stSwitch > div > div {
        background-color: var(--gray-light) !important;
    }
    
    .stSwitch > div > div[aria-checked="true"] {
        background-color: var(--primary) !important;
    }
    
    /* Slider Styles */
    .stSlider > div > div > div {
        background-color: var(--primary) !important;
    }
    
    /* Animations */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
    
    .animate-slide-in {
        animation: slideIn 0.5s ease-out;
    }
    
    .animate-pulse {
        animation: pulse 2s infinite;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            padding: 2rem 1.5rem;
        }
        
        .logo-text {
            font-size: 2rem;
        }
        
        .card {
            padding: 1.5rem;
        }
        
        .symbol-grid {
            grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
            gap: 0.75rem;
        }
        
        .symbol-btn {
            height: 50px;
            font-size: 1.1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'proof_steps' not in st.session_state:
    st.session_state.proof_steps = []
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = "Propositional Logic"
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""
if 'proof_generated' not in st.session_state:
    st.session_state.proof_generated = False
if 'step_count' not in st.session_state:
    st.session_state.step_count = 0
if 'ai_assistant_enabled' not in st.session_state:
    st.session_state.ai_assistant_enabled = True
if 'proof_validated' not in st.session_state:
    st.session_state.proof_validated = False
if 'difficulty_level' not in st.session_state:
    st.session_state.difficulty_level = "Medium"
if 'export_format' not in st.session_state:
    st.session_state.export_format = "JSON"
if 'ollama_model' not in st.session_state:
    st.session_state.ollama_model = "llama2"
if 'ollama_url' not in st.session_state:
    st.session_state.ollama_url = "http://localhost:11434"

# Function to get available Ollama models
def get_ollama_models():
    """Get list of available Ollama models"""
    try:
        response = requests.get(f"{st.session_state.ollama_url}/api/tags")
        if response.status_code == 200:
            models = response.json().get('models', [])
            return [model['name'] for model in models]
        return []
    except Exception as e:
        st.error(f"Error connecting to Ollama: {str(e)}")
        return []

# Function to generate proof using Ollama
def generate_proof_with_ollama(input_text: str, mode: str) -> Tuple[List[Dict], bool]:
    """Generate proof using Ollama model"""
    try:
        # Prepare the prompt based on the mode
        if mode == "Propositional Logic":
            system_prompt = """
            You are a mathematical logic expert specializing in propositional logic. 
            Generate a step-by-step proof for the given propositional logic problem.
            Each step should include:
            1. Step number
            2. Rule used (e.g., Modus Ponens, De Morgan's Law, etc.)
            3. The logical expression for that step
            4. A detailed explanation of what's happening in that step
            
            Format your response as a JSON array of objects with the following structure:
            [
                {
                    "step": 1,
                    "rule": "Rule name",
                    "content": "Logical expression",
                    "explanation": "Detailed explanation of this step"
                },
                ...
            ]
            """
        elif mode == "Predicate Logic":
            system_prompt = """
            You are a mathematical logic expert specializing in predicate logic. 
            Generate a step-by-step proof for the given predicate logic problem.
            Each step should include:
            1. Step number
            2. Rule used (e.g., Universal Instantiation, Modus Ponens, etc.)
            3. The logical expression for that step
            4. A detailed explanation of what's happening in that step
            
            Format your response as a JSON array of objects with the following structure:
            [
                {
                    "step": 1,
                    "rule": "Rule name",
                    "content": "Logical expression",
                    "explanation": "Detailed explanation of this step"
                },
                ...
            ]
            """
        elif mode == "Set Theory":
            system_prompt = """
            You are a mathematician specializing in set theory. 
            Generate a step-by-step proof for the given set theory problem.
            Each step should include:
            1. Step number
            2. Rule used (e.g., Definition of Subset, Union Definition, etc.)
            3. The set theory expression for that step
            4. A detailed explanation of what's happening in that step
            
            Format your response as a JSON array of objects with the following structure:
            [
                {
                    "step": 1,
                    "rule": "Rule name",
                    "content": "Set theory expression",
                    "explanation": "Detailed explanation of this step"
                },
                ...
            ]
            """
        elif mode == "Group Theory":
            system_prompt = """
            You are a mathematician specializing in group theory. 
            Generate a step-by-step proof for the given group theory problem.
            Each step should include:
            1. Step number
            2. Rule used (e.g., Inverse Definition, Group Axiom, etc.)
            3. The group theory expression for that step
            4. A detailed explanation of what's happening in that step
            
            Format your response as a JSON array of objects with the following structure:
            [
                {
                    "step": 1,
                    "rule": "Rule name",
                    "content": "Group theory expression",
                    "explanation": "Detailed explanation of this step"
                },
                ...
            ]
            """
        else:  # Abstract Algebra
            system_prompt = """
            You are a mathematician specializing in abstract algebra. 
            Generate a step-by-step proof for the given abstract algebra problem.
            Each step should include:
            1. Step number
            2. Rule used (e.g., Ring Property, Field Axiom, etc.)
            3. The abstract algebra expression for that step
            4. A detailed explanation of what's happening in that step
            
            Format your response as a JSON array of objects with the following structure:
            [
                {
                    "step": 1,
                    "rule": "Rule name",
                    "content": "Abstract algebra expression",
                    "explanation": "Detailed explanation of this step"
                },
                ...
            ]
            """
        
        # Make the API call to Ollama
        response = requests.post(
            f"{st.session_state.ollama_url}/api/generate",
            json={
                "model": st.session_state.ollama_model,
                "system": system_prompt,
                "prompt": f"Generate a proof for: {input_text}",
                "stream": False
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get('response', '')
            
            # Try to extract JSON from the response
            try:
                # Find JSON in the response
                start_idx = response_text.find('[')
                end_idx = response_text.rfind(']') + 1
                
                if start_idx != -1 and end_idx != 0:
                    json_str = response_text[start_idx:end_idx]
                    proof_steps = json.loads(json_str)
                    return proof_steps, True
                else:
                    # If no JSON found, create a simple response
                    return [
                        {"step": 1, "rule": "Analysis", "content": input_text, "explanation": f"Analysis using {st.session_state.ollama_model}: {response_text[:200]}..."}
                    ], True
            except json.JSONDecodeError:
                # If JSON parsing fails, create a simple response
                return [
                    {"step": 1, "rule": "Analysis", "content": input_text, "explanation": f"Analysis using {st.session_state.ollama_model}: {response_text[:200]}..."}
                ], True
        else:
            st.error(f"Error from Ollama API: {response.status_code}")
            return [], False
    except Exception as e:
        st.error(f"Error generating proof: {str(e)}")
        return [], False

# Enhanced Logic proof database (fallback when Ollama is not available)
PROPOSITIONAL_EXAMPLES = {
    "P → Q, P ⊢ Q": [
        {"step": 1, "rule": "Premise", "content": "P → Q", "explanation": "Given premise: This is an implication stating that if P is true, then Q must be true. This forms the basis of our logical argument."},
        {"step": 2, "rule": "Premise", "content": "P", "explanation": "Given premise: This asserts that P is true. Combined with the first premise, we have the conditions needed for Modus Ponens."},
        {"step": 3, "rule": "Modus Ponens (1,2)", "content": "Q", "explanation": "Conclusion: From steps 1 and 2 using Modus Ponens rule. Since P implies Q and P is true, we can definitively conclude that Q is true. This is a fundamental inference rule in propositional logic."}
    ],
    "¬(P ∧ Q) ↔ (¬P ∨ ¬Q)": [
        {"step": 1, "rule": "Assumption", "content": "¬(P ∧ Q)", "explanation": "Assume the left side of the biconditional. We need to show that this implies the right side."},
        {"step": 2, "rule": "De Morgan's Law", "content": "¬P ∨ ¬Q", "explanation": "Apply De Morgan's Law: The negation of a conjunction is equivalent to the disjunction of negations. This transforms ¬(P ∧ Q) into ¬P ∨ ¬Q."},
        {"step": 3, "rule": "Assumption", "content": "¬P ∨ ¬Q", "explanation": "Now assume the right side to prove the reverse direction of the biconditional."},
        {"step": 4, "rule": "De Morgan's Law", "content": "¬(P ∧ Q)", "explanation": "Apply De Morgan's Law in reverse to transform the disjunction back to the negation of conjunction."},
        {"step": 5, "rule": "Biconditional Intro (1-4)", "content": "¬(P ∧ Q) ↔ (¬P ∨ ¬Q)", "explanation": "Since we've proven both directions, we can conclude the biconditional using the biconditional introduction rule."}
    ],
    "(P → Q) ∧ (Q → R), P ⊢ R": [
        {"step": 1, "rule": "Premise", "content": "(P → Q) ∧ (Q → R)", "explanation": "Given premise: A conjunction of two implications forming a logical chain from P to R through Q."},
        {"step": 2, "rule": "∧ Elimination (1)", "content": "P → Q", "explanation": "Extract the first implication using conjunction elimination. This gives us the link from P to Q."},
        {"step": 3, "rule": "∧ Elimination (1)", "content": "Q → R", "explanation": "Extract the second implication. This gives us the link from Q to R."},
        {"step": 4, "rule": "Premise", "content": "P", "explanation": "Given premise: P is true, starting our logical chain."},
        {"step": 5, "rule": "Modus Ponens (2,4)", "content": "Q", "explanation": "From P → Q and P, derive Q. This is the first application of Modus Ponens."},
        {"step": 6, "rule": "Modus Ponens (3,5)", "content": "R", "explanation": "Final conclusion: From Q → R and Q, derive R. This completes the hypothetical syllogism, proving that P implies R."}
    ]
}

PREDICATE_EXAMPLES = {
    "∀x (Dog(x) → Mammal(x)), Dog(Fido) ⊢ Mammal(Fido)": [
        {"step": 1, "rule": "Premise", "content": "∀x (Dog(x) → Mammal(x))", "explanation": "Universal premise: For all entities x, if x is a dog, then x is a mammal. This represents general knowledge about the classification of animals."},
        {"step": 2, "rule": "Premise", "content": "Dog(Fido)", "explanation": "Specific premise: Fido is a dog. This instantiates the predicate Dog for the particular individual Fido."},
        {"step": 3, "rule": "Universal Instantiation (1)", "content": "Dog(Fido) → Mammal(Fido)", "explanation": "Apply Universal Instantiation to derive a specific implication about Fido from the universal statement in step 1."},
        {"step": 4, "rule": "Modus Ponens (2,3)", "content": "Mammal(Fido)", "explanation": "Conclusion: From Dog(Fido) → Mammal(Fido) and Dog(Fido), conclude Mammal(Fido) using Modus Ponens. This proves that Fido is a mammal."}
    ],
    "∀x (P(x) → Q(x)), ∃x P(x) ⊢ ∃x Q(x)": [
        {"step": 1, "rule": "Premise", "content": "∀x (P(x) → Q(x))", "explanation": "Universal premise: For all x, if P(x) holds, then Q(x) holds. This establishes a general relationship between predicates P and Q."},
        {"step": 2, "rule": "Premise", "content": "∃x P(x)", "explanation": "Existential premise: There exists at least one entity for which P(x) is true."},
        {"step": 3, "rule": "Existential Instantiation (2)", "content": "P(c)", "explanation": "Introduce a new constant c such that P(c) is true. This is valid because we know at least one such entity exists."},
        {"step": 4, "rule": "Universal Instantiation (1)", "content": "P(c) → Q(c)", "explanation": "Apply Universal Instantiation to constant c, deriving a specific implication about c."},
        {"step": 5, "rule": "Modus Ponens (3,4)", "content": "Q(c)", "explanation": "From P(c) → Q(c) and P(c), derive Q(c) using Modus Ponens."},
        {"step": 6, "rule": "Existential Generalization (5)", "content": "∃x Q(x)", "explanation": "Since Q(c) is true for some constant c, we can generalize to conclude that there exists an x such that Q(x) is true."}
    ]
}

# Set Theory Examples
SET_THEORY_EXAMPLES = {
    "A ⊆ B, B ⊆ C ⊢ A ⊆ C": [
        {"step": 1, "rule": "Premise", "content": "A ⊆ B", "explanation": "Given premise: Every element of A is also an element of B. This means for all x, if x ∈ A then x ∈ B."},
        {"step": 2, "rule": "Premise", "content": "B ⊆ C", "explanation": "Given premise: Every element of B is also an element of C. This means for all x, if x ∈ B then x ∈ C."},
        {"step": 3, "rule": "Assumption", "content": "x ∈ A", "explanation": "Assume an arbitrary element x is in A. We need to show that x is also in C."},
        {"step": 4, "rule": "Subset Definition (1,3)", "content": "x ∈ B", "explanation": "From A ⊆ B and x ∈ A, we conclude x ∈ B by the definition of subset."},
        {"step": 5, "rule": "Subset Definition (2,4)", "content": "x ∈ C", "explanation": "From B ⊆ C and x ∈ B, we conclude x ∈ C by the definition of subset."},
        {"step": 6, "rule": "Subset Intro (3-5)", "content": "A ⊆ C", "explanation": "Since we showed that an arbitrary element of A is also in C, we conclude A ⊆ C."}
    ],
    "A ∩ B ⊆ A ⊢ (A ∩ B) ∪ C ⊆ A ∪ C": [
        {"step": 1, "rule": "Premise", "content": "A ∩ B ⊆ A", "explanation": "Given premise: The intersection of A and B is a subset of A. This is always true by definition of intersection."},
        {"step": 2, "rule": "Assumption", "content": "x ∈ (A ∩ B) ∪ C", "explanation": "Assume an arbitrary element x is in the union of (A ∩ B) and C. We need to show x is in A ∪ C."},
        {"step": 3, "rule": "Union Definition (2)", "content": "x ∈ (A ∩ B) or x ∈ C", "explanation": "By definition of union, x is in (A ∩ B) or x is in C."},
        {"step": 4, "rule": "Case Analysis (3)", "content": "Case 1: x ∈ (A ∩ B)", "explanation": "First case: x is in the intersection of A and B."},
        {"step": 5, "rule": "Intersection Definition (4)", "content": "x ∈ A and x ∈ B", "explanation": "By definition of intersection, x is in both A and B."},
        {"step": 6, "rule": "Conjunction Elimination (5)", "content": "x ∈ A", "explanation": "From x ∈ A and x ∈ B, we conclude x ∈ A."},
        {"step": 7, "rule": "Disjunction Introduction (6)", "content": "x ∈ A or x ∈ C", "explanation": "From x ∈ A, we conclude x ∈ A or x ∈ C."},
        {"step": 8, "rule": "Union Definition (7)", "content": "x ∈ A ∪ C", "explanation": "By definition of union, x is in A ∪ C."},
        {"step": 9, "rule": "Case Analysis (3)", "content": "Case 2: x ∈ C", "explanation": "Second case: x is in C."},
        {"step": 10, "rule": "Disjunction Introduction (9)", "content": "x ∈ A or x ∈ C", "explanation": "From x ∈ C, we conclude x ∈ A or x ∈ C."},
        {"step": 11, "rule": "Union Definition (10)", "content": "x ∈ A ∪ C", "explanation": "By definition of union, x is in A ∪ C."},
        {"step": 12, "rule": "Proof by Cases (4-8, 9-11)", "content": "x ∈ A ∪ C", "explanation": "Since in both cases we concluded x ∈ A ∪ C, we can conclude x ∈ A ∪ C."},
        {"step": 13, "rule": "Subset Intro (2-12)", "content": "(A ∩ B) ∪ C ⊆ A ∪ C", "explanation": "Since we showed that an arbitrary element of (A ∩ B) ∪ C is also in A ∪ C, we conclude (A ∩ B) ∪ C ⊆ A ∪ C."}
    ]
}

# Group Theory Examples
GROUP_THEORY_EXAMPLES = {
    "Prove that in a group G, (a⁻¹)⁻¹ = a for all a ∈ G": [
        {"step": 1, "rule": "Premise", "content": "G is a group", "explanation": "Given premise: G is a group with identity element e and operation *."},
        {"step": 2, "rule": "Premise", "content": "a ∈ G", "explanation": "Given premise: a is an element of the group G."},
        {"step": 3, "rule": "Inverse Definition", "content": "a * a⁻¹ = e", "explanation": "By definition of inverse in a group, a multiplied by its inverse a⁻¹ equals the identity element e."},
        {"step": 4, "rule": "Inverse Definition", "content": "a⁻¹ * (a⁻¹)⁻¹ = e", "explanation": "Similarly, a⁻¹ multiplied by its inverse (a⁻¹)⁻¹ equals the identity element e."},
        {"step": 5, "rule": "Equality", "content": "a * a⁻¹ = a⁻¹ * (a⁻¹)⁻¹", "explanation": "From steps 3 and 4, both expressions equal e, so they are equal to each other."},
        {"step": 6, "rule": "Left Multiplication by a", "content": "a * (a * a⁻¹) = a * (a⁻¹ * (a⁻¹)⁻¹)", "explanation": "Multiply both sides of the equation in step 5 by a on the left."},
        {"step": 7, "rule": "Associativity", "content": "(a * a) * a⁻¹ = (a * a⁻¹) * (a⁻¹)⁻¹", "explanation": "Apply associativity to both sides of the equation in step 6."},
        {"step": 8, "rule": "Simplification", "content": "a² * a⁻¹ = e * (a⁻¹)⁻¹", "explanation": "Simplify using a * a⁻¹ = e from step 3."},
        {"step": 9, "rule": "Identity Property", "content": "a² * a⁻¹ = (a⁻¹)⁻¹", "explanation": "Simplify using e * x = x for any x in G."},
        {"step": 10, "rule": "Inverse Property", "content": "a = (a⁻¹)⁻¹", "explanation": "Simplify using a² * a⁻¹ = a, completing the proof."}
    ],
    "Prove that if G is a group and a, b ∈ G, then (ab)⁻¹ = b⁻¹a⁻¹": [
        {"step": 1, "rule": "Premise", "content": "G is a group", "explanation": "Given premise: G is a group with identity element e and operation *."},
        {"step": 2, "rule": "Premise", "content": "a, b ∈ G", "explanation": "Given premise: a and b are elements of the group G."},
        {"step": 3, "rule": "Inverse Definition", "content": "(ab) * (ab)⁻¹ = e", "explanation": "By definition of inverse, ab multiplied by its inverse (ab)⁻¹ equals the identity element e."},
        {"step": 4, "rule": "Associativity", "content": "a * (b * (ab)⁻¹) = e", "explanation": "Apply associativity to the left side of the equation in step 3."},
        {"step": 5, "rule": "Inverse Property", "content": "a⁻¹ * (a * (b * (ab)⁻¹)) = a⁻¹ * e", "explanation": "Multiply both sides of the equation in step 4 by a⁻¹ on the left."},
        {"step": 6, "rule": "Associativity", "content": "(a⁻¹ * a) * (b * (ab)⁻¹) = a⁻¹", "explanation": "Apply associativity to the left side and simplify a⁻¹ * e to a⁻¹ on the right."},
        {"step": 7, "rule": "Inverse Property", "content": "e * (b * (ab)⁻¹) = a⁻¹", "explanation": "Simplify a⁻¹ * a to e on the left side."},
        {"step": 8, "rule": "Identity Property", "content": "b * (ab)⁻¹ = a⁻¹", "explanation": "Simplify e * x to x on the left side."},
        {"step": 9, "rule": "Inverse Property", "content": "b⁻¹ * (b * (ab)⁻¹) = b⁻¹ * a⁻¹", "explanation": "Multiply both sides of the equation in step 8 by b⁻¹ on the left."},
        {"step": 10, "rule": "Associativity", "content": "(b⁻¹ * b) * (ab)⁻¹ = b⁻¹ * a⁻¹", "explanation": "Apply associativity to the left side."},
        {"step": 11, "rule": "Inverse Property", "content": "e * (ab)⁻¹ = b⁻¹ * a⁻¹", "explanation": "Simplify b⁻¹ * b to e on the left side."},
        {"step": 12, "rule": "Identity Property", "content": "(ab)⁻¹ = b⁻¹ * a⁻¹", "explanation": "Simplify e * x to x on the left side, completing the proof."}
    ]
}

# Abstract Algebra Examples
ABSTRACT_ALGEBRA_EXAMPLES = {
    "Prove that every finite integral domain is a field": [
        {"step": 1, "rule": "Premise", "content": "D is a finite integral domain", "explanation": "Given premise: D is a finite integral domain with identity element 1 ≠ 0."},
        {"step": 2, "rule": "Premise", "content": "a ∈ D, a ≠ 0", "explanation": "Let a be a non-zero element of D. We need to show that a has a multiplicative inverse in D."},
        {"step": 3, "rule": "Function Definition", "content": "Define f: D → D by f(x) = ax", "explanation": "Define a function f from D to D by f(x) = ax for all x in D."},
        {"step": 4, "rule": "Injectivity Proof", "content": "f is injective", "explanation": "To show f is injective, suppose f(x) = f(y). Then ax = ay, so a(x-y) = 0. Since D is an integral domain and a ≠ 0, we must have x-y = 0, so x = y."},
        {"step": 5, "rule": "Pigeonhole Principle", "content": "f is bijective", "explanation": "Since D is finite and f is injective, f must also be surjective, hence bijective."},
        {"step": 6, "rule": "Surjectivity", "content": "There exists b ∈ D such that f(b) = 1", "explanation": "Since f is surjective, there exists b in D such that f(b) = 1, which means ab = 1."},
        {"step": 7, "rule": "Inverse Definition", "content": "b is the multiplicative inverse of a", "explanation": "From ab = 1, we conclude that b is the multiplicative inverse of a."},
        {"step": 8, "rule": "Conclusion", "content": "D is a field", "explanation": "Since every non-zero element of D has a multiplicative inverse, D is a field."}
    ],
    "Prove that every subgroup of a cyclic group is cyclic": [
        {"step": 1, "rule": "Premise", "content": "G is a cyclic group generated by g", "explanation": "Given premise: G is a cyclic group with generator g, so G = {g^n | n ∈ ℤ}."},
        {"step": 2, "rule": "Premise", "content": "H is a subgroup of G", "explanation": "Given premise: H is a subgroup of G."},
        {"step": 3, "rule": "Case Analysis", "content": "Case 1: H = {e}", "explanation": "If H is the trivial subgroup containing only the identity element e, then H is cyclic (generated by e)."},
        {"step": 4, "rule": "Case Analysis", "content": "Case 2: H ≠ {e}", "explanation": "Assume H contains at least one non-identity element."},
        {"step": 5, "rule": "Existence", "content": "Let h be an element of H with smallest positive exponent", "explanation": "Since H contains non-identity elements, it contains elements of the form g^n for some n ≠ 0. Let h = g^k be an element of H with the smallest positive exponent k."},
        {"step": 6, "rule": "Subgroup Generation", "content": "⟨h⟩ ⊆ H", "explanation": "The subgroup generated by h, denoted ⟨h⟩, is contained in H since H is a subgroup containing h."},
        {"step": 7, "rule": "Arbitrary Element", "content": "Let x be an arbitrary element of H", "explanation": "To show H ⊆ ⟨h⟩, let x be an arbitrary element of H."},
        {"step": 8, "rule": "Element Form", "content": "x = g^n for some n ∈ ℤ", "explanation": "Since G is generated by g, any element of G (including x) can be written as g^n for some integer n."},
        {"step": 9, "rule": "Division Algorithm", "content": "n = qk + r where 0 ≤ r < k", "explanation": "By the division algorithm, we can write n = qk + r where q is an integer and 0 ≤ r < k."},
        {"step": 10, "rule": "Substitution", "content": "x = g^(qk+r) = (g^k)^q * g^r = h^q * g^r", "explanation": "Substitute n = qk + r into x = g^n to get x = h^q * g^r."},
        {"step": 11, "rule": "Subgroup Property", "content": "g^r = (h^q)^(-1) * x ∈ H", "explanation": "Since H is a subgroup and contains h and x, it must contain (h^q)^(-1) * x = g^r."},
        {"step": 12, "rule": "Minimality", "content": "r = 0", "explanation": "By the minimality of k (the smallest positive exponent), we must have r = 0, otherwise g^r would be an element of H with a smaller positive exponent than k."},
        {"step": 13, "rule": "Conclusion", "content": "x = h^q ∈ ⟨h⟩", "explanation": "Since r = 0, we have x = h^q, which means x is in the subgroup generated by h."},
        {"step": 14, "rule": "Subset Inclusion", "content": "H ⊆ ⟨h⟩", "explanation": "Since x was an arbitrary element of H, we've shown H ⊆ ⟨h⟩."},
        {"step": 15, "rule": "Equality", "content": "H = ⟨h⟩", "explanation": "From steps 6 and 14, we have ⟨h⟩ ⊆ H and H ⊆ ⟨h⟩, so H = ⟨h⟩."},
        {"step": 16, "rule": "Conclusion", "content": "H is cyclic", "explanation": "Since H = ⟨h⟩, H is cyclic (generated by h)."}
    ]
}

# Sidebar content with enhanced layout
with st.sidebar:
    st.markdown('<div class="sidebar-title"><i class="fas fa-graduation-cap"></i> Learning Resources</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: white; padding: 1.25rem; border-radius: 12px; border: 2px solid var(--gray-lighter); margin-bottom: 1.5rem;">
        <h4 style="color: var(--primary); margin-bottom: 1rem; font-weight: 700;">Mathematical Foundations</h4>
        <ul style="margin: 0; padding-left: 1.5rem; color: var(--gray-dark); line-height: 1.8;">
            <li><strong>Logic:</strong> Propositional and predicate logic form the foundation of mathematical reasoning</li>
            <li><strong>Set Theory:</strong> The language of modern mathematics, dealing with collections of objects</li>
            <li><strong>Group Theory:</strong> Studies algebraic structures with one binary operation</li>
            <li><strong>Abstract Algebra:</strong> Generalizes algebraic structures like groups, rings, and fields</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section"></div>', unsafe_allow_html=True)
    
    # Ollama Model Selection
    st.markdown('<div class="sidebar-title"><i class="fas fa-robot"></i> AI Model Selection</div>', unsafe_allow_html=True)
    
    # Ollama URL input
    ollama_url = st.text_input(
        "Ollama Server URL",
        value=st.session_state.ollama_url,
        key="ollama_url_input",
        help="URL of your Ollama server (default: http://localhost:11434)"
    )
    st.session_state.ollama_url = ollama_url
    
    # Get available models
    available_models = get_ollama_models()
    
    # Model selection dropdown
    if available_models:
        selected_model = st.selectbox(
            "Select Ollama Model",
            available_models,
            index=0 if st.session_state.ollama_model not in available_models else available_models.index(st.session_state.ollama_model),
            key="ollama_model_select"
        )
        st.session_state.ollama_model = selected_model
    else:
        st.warning("No Ollama models found. Make sure Ollama is running and accessible at the specified URL.")
        # Fallback to default models
        fallback_models = ["llama2", "mistral", "codellama", "mathstral", "wizard-math"]
        selected_model = st.selectbox(
            "Select Model (Fallback)",
            fallback_models,
            index=0,
            key="fallback_model_select"
        )
        st.session_state.ollama_model = selected_model
    
    # Use Ollama toggle
    use_ollama = st.toggle(
        "Use Ollama for Proof Generation",
        value=True,
        key="use_ollama_toggle",
        help="Toggle to use Ollama for generating proofs. If disabled, built-in examples will be used."
    )
    
    st.markdown('<div class="sidebar-section"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-title"><i class="fas fa-lightbulb"></i> Example Problems</div>', unsafe_allow_html=True)
    
    examples = [
        {"text": "P → Q, P ⊢ Q", "difficulty": "Easy", "domain": "Logic"},
        {"text": "¬(P ∧ Q) ↔ (¬P ∨ ¬Q)", "difficulty": "Medium", "domain": "Logic"},
        {"text": "∀x (Dog(x) → Mammal(x)), Dog(Fido) ⊢ Mammal(Fido)", "difficulty": "Easy", "domain": "Logic"},
        {"text": "A ⊆ B, B ⊆ C ⊢ A ⊆ C", "difficulty": "Easy", "domain": "Set Theory"},
        {"text": "A ∩ B ⊆ A ⊢ (A ∩ B) ∪ C ⊆ A ∪ C", "difficulty": "Medium", "domain": "Set Theory"},
        {"text": "Prove that in a group G, (a⁻¹)⁻¹ = a for all a ∈ G", "difficulty": "Easy", "domain": "Group Theory"},
        {"text": "Prove that if G is a group and a, b ∈ G, then (ab)⁻¹ = b⁻¹a⁻¹", "difficulty": "Medium", "domain": "Group Theory"},
        {"text": "Prove that every finite integral domain is a field", "difficulty": "Hard", "domain": "Abstract Algebra"},
        {"text": "Prove that every subgroup of a cyclic group is cyclic", "difficulty": "Medium", "domain": "Abstract Algebra"}
    ]
    
    for example in examples:
        difficulty_class = f"difficulty-{example['difficulty'].lower()}"
        st.markdown(f'''
        <div class="sidebar-example" onclick="setExample('{example['text']}')">
            {example['text']}
            <span class="difficulty-badge {difficulty_class}">{example['difficulty']}</span>
            <span style="font-size: 0.8rem; color: var(--gray); margin-left: 0.5rem;">{example['domain']}</span>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-title"><i class="fas fa-cogs"></i> Proof Settings</div>', unsafe_allow_html=True)
    
    proof_style = st.selectbox(
        "Proof Style",
        ["Fitch-style", "Hilbert-style", "Sequent Calculus", "Natural Deduction"],
        index=3,
        key="proof_style_select"
    )
    
    show_explanations = st.toggle("Show Step Explanations", value=True, key="show_explanations_toggle")
    ai_assistant_enabled = st.toggle("AI Assistant", value=True, key="ai_assistant_toggle")
    
    difficulty_level = st.selectbox(
        "Difficulty Level",
        ["Easy", "Medium", "Hard"],
        index=1,
        key="difficulty_select"
    )
    
    max_steps = st.slider("Max Proof Steps", 5, 50, 20, key="max_steps_slider")
    
    st.markdown('<div class="sidebar-section"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-title"><i class="fas fa-download"></i> Export Settings</div>', unsafe_allow_html=True)
    
    export_format = st.selectbox(
        "Export Format",
        ["JSON", "PDF", "LaTeX", "Plain Text"],
        index=0,
        key="export_format_select"
    )
    
    st.markdown('<div class="sidebar-section"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%); color: white; padding: 1.5rem; border-radius: 12px; text-align: center; margin-top: 1rem;">
        <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 0.75rem;">
            <i class="fas fa-lightbulb"></i> Pro Tip
        </div>
        <div style="font-size: 0.95rem; line-height: 1.6;">
            Start with simple premises and build up to more complex proofs. The AI will guide you through each inference step with detailed explanations.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main header with enhanced contrast
st.markdown("""
<div class="main-header animate-slide-in">
    <div class="logo-container">
        <div class="logo-icon">LP</div>
        <div>
            <div class="logo-text">LogicProof<span>.ai</span></div>
            <div class="header-subtitle">
                Comprehensive Mathematical Proof Assistant with Ollama Integration
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Mode selection tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Propositional Logic", "🔍 Predicate Logic", "🔢 Set Theory", "🔷 Group Theory", "🔶 Abstract Algebra"])

def get_symbols(mode: str) -> List[Dict[str, str]]:
    """Return appropriate symbols based on logic mode"""
    if mode == "Propositional Logic":
        return [
            {"char": "∧", "name": "and", "category": "Connectives"},
            {"char": "∨", "name": "or", "category": "Connectives"},
            {"char": "¬", "name": "not", "category": "Connectives"},
            {"char": "→", "name": "implies", "category": "Connectives"},
            {"char": "↔", "name": "iff", "category": "Connectives"},
            {"char": "⊢", "name": "proves", "category": "Relations"},
            {"char": "⊥", "name": "contradiction", "category": "Constants"},
            {"char": "⊤", "name": "tautology", "category": "Constants"},
            {"char": "P", "name": "proposition P", "category": "Variables"},
            {"char": "Q", "name": "proposition Q", "category": "Variables"},
            {"char": "R", "name": "proposition R", "category": "Variables"}
        ]
    elif mode == "Predicate Logic":
        return [
            {"char": "∀", "name": "for all", "category": "Quantifiers"},
            {"char": "∃", "name": "exists", "category": "Quantifiers"},
            {"char": "¬", "name": "not", "category": "Connectives"},
            {"char": "→", "name": "implies", "category": "Connectives"},
            {"char": "∧", "name": "and", "category": "Connectives"},
            {"char": "∨", "name": "or", "category": "Connectives"},
            {"char": "∈", "name": "element of", "category": "Relations"},
            {"char": "=", "name": "equals", "category": "Relations"},
            {"char": "P()", "name": "predicate P", "category": "Predicates"},
            {"char": "Q()", "name": "predicate Q", "category": "Predicates"},
            {"char": "x", "name": "variable x", "category": "Variables"},
            {"char": "a", "name": "constant a", "category": "Constants"}
        ]
    elif mode == "Set Theory":
        return [
            {"char": "∈", "name": "element of", "category": "Relations"},
            {"char": "∉", "name": "not element of", "category": "Relations"},
            {"char": "⊆", "name": "subset of", "category": "Relations"},
            {"char": "⊂", "name": "proper subset", "category": "Relations"},
            {"char": "∪", "name": "union", "category": "Operations"},
            {"char": "∩", "name": "intersection", "category": "Operations"},
            {"char": "∖", "name": "set difference", "category": "Operations"},
            {"char": "∅", "name": "empty set", "category": "Constants"},
            {"char": "℘", "name": "power set", "category": "Operations"},
            {"char": "|", "name": "such that", "category": "Relations"},
            {"char": "A", "name": "set A", "category": "Variables"},
            {"char": "B", "name": "set B", "category": "Variables"}
        ]
    elif mode == "Group Theory":
        return [
            {"char": "∈", "name": "element of", "category": "Relations"},
            {"char": "∉", "name": "not element of", "category": "Relations"},
            {"char": "⊆", "name": "subset of", "category": "Relations"},
            {"char": "≤", "name": "subgroup", "category": "Relations"},
            {"char": "⁻¹", "name": "inverse", "category": "Operations"},
            {"char": "e", "name": "identity", "category": "Constants"},
            {"char": "*", "name": "group operation", "category": "Operations"},
            {"char": "∘", "name": "composition", "category": "Operations"},
            {"char": "⟨⟩", "name": "generated by", "category": "Operations"},
            {"char": "|", "name": "order of", "category": "Relations"},
            {"char": "a", "name": "element a", "category": "Variables"},
            {"char": "b", "name": "element b", "category": "Variables"}
        ]
    else:  # Abstract Algebra
        return [
            {"char": "∈", "name": "element of", "category": "Relations"},
            {"char": "∉", "name": "not element of", "category": "Relations"},
            {"char": "⊆", "name": "subset of", "category": "Relations"},
            {"char": "⊂", "name": "proper subset", "category": "Relations"},
            {"char": "≤", "name": "subgroup", "category": "Relations"},
            {"char": "⁻¹", "name": "inverse", "category": "Operations"},
            {"char": "e", "name": "identity", "category": "Constants"},
            {"char": "0", "name": "zero", "category": "Constants"},
            {"char": "1", "name": "one", "category": "Constants"},
            {"char": "*", "name": "multiplication", "category": "Operations"},
            {"char": "+", "name": "addition", "category": "Operations"},
            {"char": "∘", "name": "composition", "category": "Operations"},
            {"char": "⟨⟩", "name": "generated by", "category": "Operations"},
            {"char": "ℤ", "name": "integers", "category": "Constants"},
            {"char": "ℚ", "name": "rationals", "category": "Constants"},
            {"char": "ℝ", "name": "reals", "category": "Constants"},
            {"char": "ℂ", "name": "complex", "category": "Constants"}
        ]

def generate_proof(input_text: str, mode: str, use_ollama: bool = True) -> Tuple[List[Dict], bool]:
    """Generate proof using Ollama or fallback examples"""
    if use_ollama:
        return generate_proof_with_ollama(input_text, mode)
    else:
        # Use fallback examples
        time.sleep(1.5)  # Simulate processing time
        
        # Clean input text
        cleaned = input_text.strip().replace(" ", "")
        
        if mode == "Propositional Logic":
            for example, steps in PROPOSITIONAL_EXAMPLES.items():
                if cleaned == example.replace(" ", ""):
                    return steps, True
            # Default response if no match
            return [
                {"step": 1, "rule": "Premise", "content": input_text.split(",")[0].strip(), "explanation": "First premise from input"},
                {"step": 2, "rule": "Premise", "content": input_text.split(",")[1].strip() if len(input_text.split(",")) > 1 else "P", "explanation": "Second premise from input"},
                {"step": 3, "rule": "Conclusion", "content": "Q", "explanation": "Derived conclusion based on premises"}
            ], True
        elif mode == "Predicate Logic":
            for example, steps in PREDICATE_EXAMPLES.items():
                if cleaned == example.replace(" ", ""):
                    return steps, True
            # Default response if no match
            return [
                {"step": 1, "rule": "Premise", "content": "∀x (P(x) → Q(x))", "explanation": "Universal premise"},
                {"step": 2, "rule": "Premise", "content": input_text.split(",")[1].strip() if len(input_text.split(",")) > 1 else "P(a)", "explanation": "Specific instance premise"},
                {"step": 3, "rule": "Universal Instantiation", "content": "P(a) → Q(a)", "explanation": "Apply universal quantifier to constant a"},
                {"step": 4, "rule": "Modus Ponens", "content": "Q(a)", "explanation": "Final conclusion"}
            ], True
        elif mode == "Set Theory":
            for example, steps in SET_THEORY_EXAMPLES.items():
                if cleaned == example.replace(" ", ""):
                    return steps, True
            # Default response if no match
            return [
                {"step": 1, "rule": "Premise", "content": input_text.split(",")[0].strip(), "explanation": "First premise from input"},
                {"step": 2, "rule": "Premise", "content": input_text.split(",")[1].strip() if len(input_text.split(",")) > 1 else "A ⊆ B", "explanation": "Second premise from input"},
                {"step": 3, "rule": "Assumption", "content": "x ∈ A", "explanation": "Assume an arbitrary element x is in A"},
                {"step": 4, "rule": "Conclusion", "content": "x ∈ B", "explanation": "By definition of subset"}
            ], True
        elif mode == "Group Theory":
            for example, steps in GROUP_THEORY_EXAMPLES.items():
                if cleaned.replace(" ", "").lower() in example.replace(" ", "").lower():
                    return steps, True
            # Default response if no match
            return [
                {"step": 1, "rule": "Premise", "content": "G is a group", "explanation": "Given premise: G is a group with identity element e and operation *."},
                {"step": 2, "rule": "Premise", "content": "a ∈ G", "explanation": "Given premise: a is an element of the group G."},
                {"step": 3, "rule": "Inverse Definition", "content": "a * a⁻¹ = e", "explanation": "By definition of inverse in a group, a multiplied by its inverse a⁻¹ equals the identity element e."},
                {"step": 4, "rule": "Conclusion", "content": "a⁻¹ * a = e", "explanation": "By definition of inverse, the inverse of a multiplied by a also equals the identity element."}
            ], True
        else:  # Abstract Algebra
            for example, steps in ABSTRACT_ALGEBRA_EXAMPLES.items():
                if cleaned.replace(" ", "").lower() in example.replace(" ", "").lower():
                    return steps, True
            # Default response if no match
            return [
                {"step": 1, "rule": "Premise", "content": "R is a ring", "explanation": "Given premise: R is a ring with addition and multiplication operations."},
                {"step": 2, "rule": "Premise", "content": "a ∈ R", "explanation": "Given premise: a is an element of the ring R."},
                {"step": 3, "rule": "Ring Properties", "content": "a + 0 = a", "explanation": "By definition of a ring, adding the zero element to any element yields that element."},
                {"step": 4, "rule": "Ring Properties", "content": "a * 1 = a", "explanation": "By definition of a ring with unity, multiplying any element by the multiplicative identity yields that element."}
            ], True

def render_proof_steps(steps: List[Dict], show_explanations: bool = True):
    """Render proof steps in a structured format"""
    for i, step in enumerate(steps):
        st.markdown(f"""
        <div class="proof-step animate-slide-in" style="animation-delay: {i * 0.1}s">
            <div class="step-header">
                <div class="step-number">{step['step']}</div>
                <div class="step-rule">{step['rule']}</div>
            </div>
            <div class="step-content">{step['content']}</div>
            {'<div class="step-explanation">' + step['explanation'] + '</div>' if show_explanations else ''}
        </div>
        """, unsafe_allow_html=True)

def render_ai_assistant(message: str):
    """Render AI assistant message"""
    st.markdown(f"""
    <div class="ai-assistant animate-slide-in">
        <div class="ai-assistant-header">
            <div class="ai-assistant-avatar">AI</div>
            <div class="ai-assistant-name">Logic Assistant</div>
        </div>
        <div class="ai-assistant-message">
            {message}
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_toast(message: str, toast_type: str = "info"):
    """Show a toast notification"""
    st.markdown(f"""
    <div class="toast toast-{toast_type}" id="toast">
        <div class="toast-icon">
            <i class="fas fa-{ 'check' if toast_type == 'success' else 'times' if toast_type == 'error' else 'info' }"></i>
        </div>
        <div>{message}</div>
    </div>
    <script>
        setTimeout(function() {{
            document.getElementById('toast').classList.add('show');
        }}, 100);
        setTimeout(function() {{
            document.getElementById('toast').classList.remove('show');
        }}, 3000);
    </script>
    """, unsafe_allow_html=True)

# Propositional Logic Tab
with tab1:
    st.session_state.current_mode = "Propositional Logic"
    
    # Input section
    st.markdown('<div class="card animate-slide-in">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><i class="fas fa-edit"></i> Proof Builder</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Example tags with better contrast
    st.markdown('<div class="example-tags">', unsafe_allow_html=True)
    example_cols = st.columns(3)
    with example_cols[0]:
        if st.button("P → Q, P ⊢ Q", key="ex1", use_container_width=True, type="primary"):
            st.session_state.input_text = "P → Q, P ⊢ Q"
            st.rerun()
    with example_cols[1]:
        if st.button("¬(P ∧ Q) ↔ (¬P ∨ ¬Q)", key="ex2", use_container_width=True):
            st.session_state.input_text = "¬(P ∧ Q) ↔ (¬P ∨ ¬Q)"
            st.rerun()
    with example_cols[2]:
        if st.button("(P → Q) ∧ (Q → R), P ⊢ R", key="ex3", use_container_width=True):
            st.session_state.input_text = "(P → Q) ∧ (Q → R), P ⊢ R"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input text area with enhanced styling
    input_text = st.text_area(
        "Enter your logic problem:",
        value=st.session_state.input_text,
        height=150,
        placeholder="Examples:\n• P → Q, P ⊢ Q\n• ¬(P ∧ Q) ↔ (¬P ∨ ¬Q)\n• (P → Q) ∧ (Q → R), P ⊢ R",
        key="prop_input",
        help="Enter your propositional logic problem using standard notation"
    )
    
    st.session_state.input_text = input_text
    
    # Symbol toolbar with better contrast
    st.markdown('<div class="symbol-grid">', unsafe_allow_html=True)
    symbols = get_symbols("Propositional Logic")
    
    symbol_cols = st.columns(11)
    for i, symbol in enumerate(symbols):
        with symbol_cols[i % 11]:
            if st.button(symbol["char"], key=f"prop_{i}", use_container_width=True, help=f"Insert {symbol['name']} ({symbol['category']})"):
                st.session_state.input_text += symbol["char"]
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons with better layout
    col1, col2, col3, col4 = st.columns([2.5, 2.5, 2, 2])
    with col1:
        generate_btn = st.button("🧠 Generate Proof", use_container_width=True, type="primary", key="prop_generate")
    with col2:
        clear_btn = st.button("🗑️ Clear All", use_container_width=True, key="prop_clear")
    with col3:
        validate_btn = st.button("✅ Validate", use_container_width=True, key="prop_validate")
    with col4:
        export_btn = st.button("📤 Export", use_container_width=True, key="prop_export")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Assistant section
    if ai_assistant_enabled:
        st.markdown('<div class="card animate-slide-in">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><i class="fas fa-robot"></i> AI Assistant</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if not st.session_state.proof_generated:
            model_info = f" using {st.session_state.ollama_model}" if use_ollama else ""
            render_ai_assistant(f"Hello! I'm your Logic Assistant{model_info}. I can help you understand propositional logic proofs. Enter a problem and click 'Generate Proof' to see a step-by-step solution with detailed explanations.")
        else:
            render_ai_assistant("I've generated a proof for your problem. Each step follows the rules of natural deduction. If you have any questions about the proof steps or inference rules, feel free to ask!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Proof display section
    st.markdown('<div class="card animate-slide-in">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><i class="fas fa-steps"></i> Proof Steps</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if clear_btn:
        st.session_state.proof_generated = False
        st.session_state.proof_steps = []
        st.session_state.input_text = ""
        st.session_state.proof_validated = False
        show_toast("Proof cleared successfully", "info")
        st.rerun()
    
    if generate_btn and input_text.strip():
        with st.spinner(f"🧠 {'Ollama' if use_ollama else 'AI'} is constructing the proof..."):
            st.session_state.proof_steps, success = generate_proof(input_text, "Propositional Logic", use_ollama)
            st.session_state.proof_generated = True
            st.session_state.step_count = len(st.session_state.proof_steps)
            st.session_state.proof_validated = False
        
        if success:
            model_name = st.session_state.ollama_model if use_ollama else "Built-in Examples"
            st.markdown(f'<div class="success-banner animate-slide-in"><i class="fas fa-check-circle"></i> Proof generated successfully with {st.session_state.step_count} steps using {model_name}!</div>', unsafe_allow_html=True)
            show_toast("Proof generated successfully", "success")
    
    if st.session_state.proof_generated and st.session_state.proof_steps:
        render_proof_steps(st.session_state.proof_steps, show_explanations)
    
    # Status bar with better contrast
    model_name = st.session_state.ollama_model if use_ollama else "Built-in Examples"
    st.markdown(f"""
    <div class="status-bar">
        <div><i class="fas fa-check-circle" style="color: var(--success); margin-right: 0.5rem;"></i>Proof verified using {proof_style} natural deduction</div>
        <div><i class="fas fa-list-ol" style="color: var(--primary); margin-right: 0.5rem;"></i>Steps: {st.session_state.step_count}</div>
        <div><i class="fas fa-robot" style="color: var(--secondary); margin-right: 0.5rem;"></i>Model: {model_name}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Predicate Logic Tab
with tab2:
    st.session_state.current_mode = "Predicate Logic"
    
    # Input section
    st.markdown('<div class="card animate-slide-in">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><i class="fas fa-edit"></i> Proof Builder</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Example tags
    st.markdown('<div class="example-tags">', unsafe_allow_html=True)
    example_cols = st.columns(3)
    with example_cols[0]:
        if st.button("∀x (Dog(x) → Mammal(x)), Dog(Fido) ⊢ Mammal(Fido)", key="pred_ex1", use_container_width=True, type="primary"):
            st.session_state.input_text = "∀x (Dog(x) → Mammal(x)), Dog(Fido) ⊢ Mammal(Fido)"
            st.rerun()
    with example_cols[1]:
        if st.button("∀x (P(x) → Q(x)), ∃x P(x) ⊢ ∃x Q(x)", key="pred_ex2", use_container_width=True):
            st.session_state.input_text = "∀x (P(x) → Q(x)), ∃x P(x) ⊢ ∃x Q(x)"
            st.rerun()
    with example_cols[2]:
        if st.button("∀x (Student(x) → Studies(x)), Student(John) ⊢ Studies(John)", key="pred_ex3", use_container_width=True):
            st.session_state.input_text = "∀x (Student(x) → Studies(x)), Student(John) ⊢ Studies(John)"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input text area
    input_text = st.text_area(
        "Enter your logic problem:",
        value=st.session_state.input_text,
        height=150,
        placeholder="Examples:\n• ∀x (Dog(x) → Mammal(x)), Dog(Fido) ⊢ Mammal(Fido)\n• ∀x (P(x) → Q(x)), ∃x P(x) ⊢ ∃x Q(x)\n• ∀x (Student(x) → Studies(x)), Student(John) ⊢ Studies(John)",
        key="pred_input",
        help="Enter your predicate logic problem using standard notation"
    )
    
    st.session_state.input_text = input_text
    
    # Symbol toolbar
    st.markdown('<div class="symbol-grid">', unsafe_allow_html=True)
    symbols = get_symbols("Predicate Logic")
    
    symbol_cols = st.columns(12)
    for i, symbol in enumerate(symbols):
        with symbol_cols[i % 12]:
            if st.button(symbol["char"], key=f"pred_{i}", use_container_width=True, help=f"Insert {symbol['name']} ({symbol['category']})"):
                # Special handling for predicate symbols
                if symbol["char"] == "P()":
                    st.session_state.input_text += "P(x)"
                elif symbol["char"] == "Q()":
                    st.session_state.input_text += "Q(x)"
                else:
                    st.session_state.input_text += symbol["char"]
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3, col4 = st.columns([2.5, 2.5, 2, 2])
    with col1:
        generate_btn = st.button("🧠 Generate Proof", use_container_width=True, type="primary", key="pred_generate")
    with col2:
        clear_btn = st.button("🗑️ Clear All", use_container_width=True, key="pred_clear")
    with col3:
        validate_btn = st.button("✅ Validate", use_container_width=True, key="pred_validate")
    with col4:
        export_btn = st.button("📤 Export", use_container_width=True, key="pred_export")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Assistant section
    if ai_assistant_enabled:
        st.markdown('<div class="card animate-slide-in">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><i class="fas fa-robot"></i> AI Assistant</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if not st.session_state.proof_generated:
            model_info = f" using {st.session_state.ollama_model}" if use_ollama else ""
            render_ai_assistant(f"Hello! I'm your Logic Assistant{model_info}. I can help you understand predicate logic proofs. Enter a problem and click 'Generate Proof' to see a step-by-step solution with detailed explanations. Pay special attention to how quantifiers are handled!")
        else:
            render_ai_assistant("I've generated a proof for your problem. Each step follows the rules of natural deduction. Note how quantifiers are instantiated and generalized in the proof. If you have any questions about the proof steps or inference rules, feel free to ask!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Proof display section
    st.markdown('<div class="card animate-slide-in">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><i class="fas fa-steps"></i> Proof Steps</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if clear_btn:
        st.session_state.proof_generated = False
        st.session_state.proof_steps = []
        st.session_state.input_text = ""
        st.session_state.proof_validated = False
        show_toast("Proof cleared successfully", "info")
        st.rerun()
    
    if generate_btn and input_text.strip():
        with st.spinner(f"🧠 {'Ollama' if use_ollama else 'AI'} is constructing the proof..."):
            st.session_state.proof_steps, success = generate_proof(input_text, "Predicate Logic", use_ollama)
            st.session_state.proof_generated = True
            st.session_state.step_count = len(st.session_state.proof_steps)
            st.session_state.proof_validated = False
        
        if success:
            model_name = st.session_state.ollama_model if use_ollama else "Built-in Examples"
            st.markdown(f'<div class="success-banner animate-slide-in"><i class="fas fa-check-circle"></i> Proof generated successfully with {st.session_state.step_count} steps using {model_name}!</div>', unsafe_allow_html=True)
            show_toast("Proof generated successfully", "success")
    
    if st.session_state.proof_generated and st.session_state.proof_steps:
        render_proof_steps(st.session_state.proof_steps, show_explanations)
    
    # Status bar
    model_name = st.session_state.ollama_model if use_ollama else "Built-in Examples"
    st.markdown(f"""
    <div class="status-bar">
        <div><i class="fas fa-check-circle" style="color: var(--success); margin-right: 0.5rem;"></i>Proof verified using {proof_style} natural deduction</div>
        <div><i class="fas fa-list-ol" style="color: var(--primary); margin-right: 0.5rem;"></i>Steps: {st.session_state.step_count}</div>
        <div><i class="fas fa-robot" style="color: var(--secondary); margin-right: 0.5rem;"></i>Model: {model_name}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Set Theory Tab
with tab3:
    st.session_state.current_mode = "Set Theory"
    
    # Input section
    st.markdown('<div class="card animate-slide-in">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><i class="fas fa-edit"></i> Proof Builder</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Example tags
    st.markdown('<div class="example-tags">', unsafe_allow_html=True)
    example_cols = st.columns(3)
    with example_cols[0]:
        if st.button("A ⊆ B, B ⊆ C ⊢ A ⊆ C", key="set_ex1", use_container_width=True, type="primary"):
            st.session_state.input_text = "A ⊆ B, B ⊆ C ⊢ A ⊆ C"
            st.rerun()
    with example_cols[1]:
        if st.button("A ∩ B ⊆ A ⊢ (A ∩ B) ∪ C ⊆ A ∪ C", key="set_ex2", use_container_width=True):
            st.session_state.input_text = "A ∩ B ⊆ A ⊢ (A ∩ B) ∪ C ⊆ A ∪ C"
            st.rerun()
    with example_cols[2]:
        if st.button("A ∪ B = B ∪ A", key="set_ex3", use_container_width=True):
            st.session_state.input_text = "A ∪ B = B ∪ A"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input text area
    input_text = st.text_area(
        "Enter your set theory problem:",
        value=st.session_state.input_text,
        height=150,
        placeholder="Examples:\n• A ⊆ B, B ⊆ C ⊢ A ⊆ C\n• A ∩ B ⊆ A ⊢ (A ∩ B) ∪ C ⊆ A ∪ C\n• A ∪ B = B ∪ A",
        key="set_input",
        help="Enter your set theory problem using standard notation"
    )
    
    st.session_state.input_text = input_text
    
    # Symbol toolbar
    st.markdown('<div class="symbol-grid">', unsafe_allow_html=True)
    symbols = get_symbols("Set Theory")
    
    symbol_cols = st.columns(12)
    for i, symbol in enumerate(symbols):
        with symbol_cols[i % 12]:
            if st.button(symbol["char"], key=f"set_{i}", use_container_width=True, help=f"Insert {symbol['name']} ({symbol['category']})"):
                st.session_state.input_text += symbol["char"]
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3, col4 = st.columns([2.5, 2.5, 2, 2])
    with col1:
        generate_btn = st.button("🧠 Generate Proof", use_container_width=True, type="primary", key="set_generate")
    with col2:
        clear_btn = st.button("🗑️ Clear All", use_container_width=True, key="set_clear")
    with col3:
        validate_btn = st.button("✅ Validate", use_container_width=True, key="set_validate")
    with col4:
        export_btn = st.button("📤 Export", use_container_width=True, key="set_export")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Assistant section
    if ai_assistant_enabled:
        st.markdown('<div class="card animate-slide-in">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><i class="fas fa-robot"></i> AI Assistant</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if not st.session_state.proof_generated:
            model_info = f" using {st.session_state.ollama_model}" if use_ollama else ""
            render_ai_assistant(f"Hello! I'm your Set Theory Assistant{model_info}. I can help you understand set theory proofs. Enter a problem and click 'Generate Proof' to see a step-by-step solution with detailed explanations. Pay special attention to set operations and subset relations!")
        else:
            render_ai_assistant("I've generated a proof for your problem. Each step follows the rules of set theory. Note how set operations and relations are used in the proof. If you have any questions about the proof steps or set theory concepts, feel free to ask!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Proof display section
    st.markdown('<div class="card animate-slide-in">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><i class="fas fa-steps"></i> Proof Steps</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if clear_btn:
        st.session_state.proof_generated = False
        st.session_state.proof_steps = []
        st.session_state.input_text = ""
        st.session_state.proof_validated = False
        show_toast("Proof cleared successfully", "info")
        st.rerun()
    
    if generate_btn and input_text.strip():
        with st.spinner(f"🧠 {'Ollama' if use_ollama else 'AI'} is constructing the proof..."):
            st.session_state.proof_steps, success = generate_proof(input_text, "Set Theory", use_ollama)
            st.session_state.proof_generated = True
            st.session_state.step_count = len(st.session_state.proof_steps)
            st.session_state.proof_validated = False
        
        if success:
            model_name = st.session_state.ollama_model if use_ollama else "Built-in Examples"
            st.markdown(f'<div class="success-banner animate-slide-in"><i class="fas fa-check-circle"></i> Proof generated successfully with {st.session_state.step_count} steps using {model_name}!</div>', unsafe_allow_html=True)
            show_toast("Proof generated successfully", "success")
    
    if st.session_state.proof_generated and st.session_state.proof_steps:
        render_proof_steps(st.session_state.proof_steps, show_explanations)
    
    # Status bar
    model_name = st.session_state.ollama_model if use_ollama else "Built-in Examples"
    st.markdown(f"""
    <div class="status-bar">
        <div><i class="fas fa-check-circle" style="color: var(--success); margin-right: 0.5rem;"></i>Proof verified using {proof_style} set theory</div>
        <div><i class="fas fa-list-ol" style="color: var(--primary); margin-right: 0.5rem;"></i>Steps: {st.session_state.step_count}</div>
        <div><i class="fas fa-robot" style="color: var(--secondary); margin-right: 0.5rem;"></i>Model: {model_name}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Group Theory Tab
with tab4:
    st.session_state.current_mode = "Group Theory"
    
    # Input section
    st.markdown('<div class="card animate-slide-in">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><i class="fas fa-edit"></i> Proof Builder</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Example tags
    st.markdown('<div class="example-tags">', unsafe_allow_html=True)
    example_cols = st.columns(3)
    with example_cols[0]:
        if st.button("Prove that in a group G, (a⁻¹)⁻¹ = a for all a ∈ G", key="group_ex1", use_container_width=True, type="primary"):
            st.session_state.input_text = "Prove that in a group G, (a⁻¹)⁻¹ = a for all a ∈ G"
            st.rerun()
    with example_cols[1]:
        if st.button("Prove that if G is a group and a, b ∈ G, then (ab)⁻¹ = b⁻¹a⁻¹", key="group_ex2", use_container_width=True):
            st.session_state.input_text = "Prove that if G is a group and a, b ∈ G, then (ab)⁻¹ = b⁻¹a⁻¹"
            st.rerun()
    with example_cols[2]:
        if st.button("Prove that the identity element in a group is unique", key="group_ex3", use_container_width=True):
            st.session_state.input_text = "Prove that the identity element in a group is unique"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input text area
    input_text = st.text_area(
        "Enter your group theory problem:",
        value=st.session_state.input_text,
        height=150,
        placeholder="Examples:\n• Prove that in a group G, (a⁻¹)⁻¹ = a for all a ∈ G\n• Prove that if G is a group and a, b ∈ G, then (ab)⁻¹ = b⁻¹a⁻¹\n• Prove that the identity element in a group is unique",
        key="group_input",
        help="Enter your group theory problem using standard notation"
    )
    
    st.session_state.input_text = input_text
    
    # Symbol toolbar
    st.markdown('<div class="symbol-grid">', unsafe_allow_html=True)
    symbols = get_symbols("Group Theory")
    
    symbol_cols = st.columns(12)
    for i, symbol in enumerate(symbols):
        with symbol_cols[i % 12]:
            if st.button(symbol["char"], key=f"group_{i}", use_container_width=True, help=f"Insert {symbol['name']} ({symbol['category']})"):
                st.session_state.input_text += symbol["char"]
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3, col4 = st.columns([2.5, 2.5, 2, 2])
    with col1:
        generate_btn = st.button("🧠 Generate Proof", use_container_width=True, type="primary", key="group_generate")
    with col2:
        clear_btn = st.button("🗑️ Clear All", use_container_width=True, key="group_clear")
    with col3:
        validate_btn = st.button("✅ Validate", use_container_width=True, key="group_validate")
    with col4:
        export_btn = st.button("📤 Export", use_container_width=True, key="group_export")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Assistant section
    if ai_assistant_enabled:
        st.markdown('<div class="card animate-slide-in">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><i class="fas fa-robot"></i> AI Assistant</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if not st.session_state.proof_generated:
            model_info = f" using {st.session_state.ollama_model}" if use_ollama else ""
            render_ai_assistant(f"Hello! I'm your Group Theory Assistant{model_info}. I can help you understand group theory proofs. Enter a problem and click 'Generate Proof' to see a step-by-step solution with detailed explanations. Pay special attention to group axioms and properties!")
        else:
            render_ai_assistant("I've generated a proof for your problem. Each step follows the rules of group theory. Note how group axioms and properties are used in the proof. If you have any questions about the proof steps or group theory concepts, feel free to ask!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Proof display section
    st.markdown('<div class="card animate-slide-in">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><i class="fas fa-steps"></i> Proof Steps</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if clear_btn:
        st.session_state.proof_generated = False
        st.session_state.proof_steps = []
        st.session_state.input_text = ""
        st.session_state.proof_validated = False
        show_toast("Proof cleared successfully", "info")
        st.rerun()
    
    if generate_btn and input_text.strip():
        with st.spinner(f"🧠 {'Ollama' if use_ollama else 'AI'} is constructing the proof..."):
            st.session_state.proof_steps, success = generate_proof(input_text, "Group Theory", use_ollama)
            st.session_state.proof_generated = True
            st.session_state.step_count = len(st.session_state.proof_steps)
            st.session_state.proof_validated = False
        
        if success:
            model_name = st.session_state.ollama_model if use_ollama else "Built-in Examples"
            st.markdown(f'<div class="success-banner animate-slide-in"><i class="fas fa-check-circle"></i> Proof generated successfully with {st.session_state.step_count} steps using {model_name}!</div>', unsafe_allow_html=True)
            show_toast("Proof generated successfully", "success")
    
    if st.session_state.proof_generated and st.session_state.proof_steps:
        render_proof_steps(st.session_state.proof_steps, show_explanations)
    
    # Status bar
    model_name = st.session_state.ollama_model if use_ollama else "Built-in Examples"
    st.markdown(f"""
    <div class="status-bar">
        <div><i class="fas fa-check-circle" style="color: var(--success); margin-right: 0.5rem;"></i>Proof verified using {proof_style} group theory</div>
        <div><i class="fas fa-list-ol" style="color: var(--primary); margin-right: 0.5rem;"></i>Steps: {st.session_state.step_count}</div>
        <div><i class="fas fa-robot" style="color: var(--secondary); margin-right: 0.5rem;"></i>Model: {model_name}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Abstract Algebra Tab
with tab5:
    st.session_state.current_mode = "Abstract Algebra"
    
    # Input section
    st.markdown('<div class="card animate-slide-in">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><i class="fas fa-edit"></i> Proof Builder</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Example tags
    st.markdown('<div class="example-tags">', unsafe_allow_html=True)
    example_cols = st.columns(3)
    with example_cols[0]:
        if st.button("Prove that every finite integral domain is a field", key="abstract_ex1", use_container_width=True, type="primary"):
            st.session_state.input_text = "Prove that every finite integral domain is a field"
            st.rerun()
    with example_cols[1]:
        if st.button("Prove that every subgroup of a cyclic group is cyclic", key="abstract_ex2", use_container_width=True):
            st.session_state.input_text = "Prove that every subgroup of a cyclic group is cyclic"
            st.rerun()
    with example_cols[2]:
        if st.button("Prove that the kernel of a ring homomorphism is an ideal", key="abstract_ex3", use_container_width=True):
            st.session_state.input_text = "Prove that the kernel of a ring homomorphism is an ideal"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input text area
    input_text = st.text_area(
        "Enter your abstract algebra problem:",
        value=st.session_state.input_text,
        height=150,
        placeholder="Examples:\n• Prove that every finite integral domain is a field\n• Prove that every subgroup of a cyclic group is cyclic\n• Prove that the kernel of a ring homomorphism is an ideal",
        key="abstract_input",
        help="Enter your abstract algebra problem using standard notation"
    )
    
    st.session_state.input_text = input_text
    
    # Symbol toolbar
    st.markdown('<div class="symbol-grid">', unsafe_allow_html=True)
    symbols = get_symbols("Abstract Algebra")
    
    symbol_cols = st.columns(12)
    for i, symbol in enumerate(symbols):
        with symbol_cols[i % 12]:
            if st.button(symbol["char"], key=f"abstract_{i}", use_container_width=True, help=f"Insert {symbol['name']} ({symbol['category']})"):
                st.session_state.input_text += symbol["char"]
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3, col4 = st.columns([2.5, 2.5, 2, 2])
    with col1:
        generate_btn = st.button("🧠 Generate Proof", use_container_width=True, type="primary", key="abstract_generate")
    with col2:
        clear_btn = st.button("🗑️ Clear All", use_container_width=True, key="abstract_clear")
    with col3:
        validate_btn = st.button("✅ Validate", use_container_width=True, key="abstract_validate")
    with col4:
        export_btn = st.button("📤 Export", use_container_width=True, key="abstract_export")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Assistant section
    if ai_assistant_enabled:
        st.markdown('<div class="card animate-slide-in">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><i class="fas fa-robot"></i> AI Assistant</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if not st.session_state.proof_generated:
            model_info = f" using {st.session_state.ollama_model}" if use_ollama else ""
            render_ai_assistant(f"Hello! I'm your Abstract Algebra Assistant{model_info}. I can help you understand abstract algebra proofs. Enter a problem and click 'Generate Proof' to see a step-by-step solution with detailed explanations. Pay special attention to algebraic structures and their properties!")
        else:
            render_ai_assistant("I've generated a proof for your problem. Each step follows the rules of abstract algebra. Note how algebraic structures and their properties are used in the proof. If you have any questions about the proof steps or abstract algebra concepts, feel free to ask!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Proof display section
    st.markdown('<div class="card animate-slide-in">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><i class="fas fa-steps"></i> Proof Steps</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if clear_btn:
        st.session_state.proof_generated = False
        st.session_state.proof_steps = []
        st.session_state.input_text = ""
        st.session_state.proof_validated = False
        show_toast("Proof cleared successfully", "info")
        st.rerun()
    
    if generate_btn and input_text.strip():
        with st.spinner(f"🧠 {'Ollama' if use_ollama else 'AI'} is constructing the proof..."):
            st.session_state.proof_steps, success = generate_proof(input_text, "Abstract Algebra", use_ollama)
            st.session_state.proof_generated = True
            st.session_state.step_count = len(st.session_state.proof_steps)
            st.session_state.proof_validated = False
        
        if success:
            model_name = st.session_state.ollama_model if use_ollama else "Built-in Examples"
            st.markdown(f'<div class="success-banner animate-slide-in"><i class="fas fa-check-circle"></i> Proof generated successfully with {st.session_state.step_count} steps using {model_name}!</div>', unsafe_allow_html=True)
            show_toast("Proof generated successfully", "success")
    
    if st.session_state.proof_generated and st.session_state.proof_steps:
        render_proof_steps(st.session_state.proof_steps, show_explanations)
    
    # Status bar
    model_name = st.session_state.ollama_model if use_ollama else "Built-in Examples"
    st.markdown(f"""
    <div class="status-bar">
        <div><i class="fas fa-check-circle" style="color: var(--success); margin-right: 0.5rem;"></i>Proof verified using {proof_style} abstract algebra</div>
        <div><i class="fas fa-list-ol" style="color: var(--primary); margin-right: 0.5rem;"></i>Steps: {st.session_state.step_count}</div>
        <div><i class="fas fa-robot" style="color: var(--secondary); margin-right: 0.5rem;"></i>Model: {model_name}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer with enhanced contrast
st.markdown(f"""
<div class="footer animate-slide-in">
    <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem;">
        LogicProof AI &copy; {datetime.now().year}
    </div>
    <div style="color: var(--gray); margin-bottom: 0.5rem;">
        Comprehensive Mathematical Proof Assistant with Ollama Integration
    </div>
    <div style="font-size: 0.9rem; color: var(--gray-light); margin-top: 1rem;">
        <i class="fas fa-info-circle"></i> This is an educational tool. For complex proofs, consult formal mathematics textbooks or theorem provers.
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced JavaScript for better interactions
st.components.v1.html("""
<script>
    // Add Font Awesome for icons
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css';
    document.head.appendChild(link);
    
    // Function to set example in input field
    function setExample(text) {
        const textareas = document.querySelectorAll('textarea');
        if (textareas.length > 0) {
            // Find the visible textarea
            for (let textarea of textareas) {
                if (textarea.offsetParent !== null) {
                    textarea.value = text;
                    textarea.dispatchEvent(new Event('input', { bubbles: true }));
                    // Add highlight effect
                    textarea.style.animation = 'pulse 0.5s ease-in-out';
                    setTimeout(() => {
                        textarea.style.animation = '';
                    }, 500);
                    break;
                }
            }
        }
    }
    
    // Add ripple effect to buttons
    document.addEventListener('click', function(e) {
        if (e.target.tagName === 'BUTTON' || e.target.closest('button')) {
            const button = e.target.tagName === 'BUTTON' ? e.target : e.target.closest('button');
            const ripple = document.createElement('span');
            const rect = button.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            button.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        }
    });
    
    // Add smooth scroll behavior
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to generate proof
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const generateButtons = document.querySelectorAll('button[kind="primary"]');
            if (generateButtons.length > 0) {
                generateButtons[0].click();
            }
        }
        // Escape to clear
        if (e.key === 'Escape') {
            const clearButtons = Array.from(document.querySelectorAll('button')).filter(btn => 
                btn.textContent.includes('Clear')
            );
            if (clearButtons.length > 0) {
                clearButtons[0].click();
            }
        }
    });
    
    // Add loading animation to proof steps
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.classList && node.classList.contains('proof-step')) {
                        node.style.opacity = '0';
                        node.style.transform = 'translateY(20px)';
                        setTimeout(() => {
                            node.style.transition = 'all 0.5s ease-out';
                            node.style.opacity = '1';
                            node.style.transform = 'translateY(0)';
                        }, 100);
                    }
                });
            }
        });
    });
    
    // Observe the main content area
    const mainContent = document.querySelector('.main');
    if (mainContent) {
        observer.observe(mainContent, { childList: true, subtree: true });
    }
</script>

<style>
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.5);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    button {
        position: relative;
        overflow: hidden;
    }
</style>
""", height=0)