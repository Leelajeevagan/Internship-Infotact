"""
CareFlow™ Authentication & User Management Module
Provides secure multi-user credential verification, role-based profiles,
demo staff accounts, user registration, and session lifecycle management.
"""

import json
import hashlib
import secrets
from pathlib import Path
from datetime import datetime
import streamlit as st

AUTH_FILE = Path(__file__).parent / "users.json"

DEFAULT_USERS = [
    {
        "username": "doctor",
        "full_name": "Dr. Sarah Jenkins, MD",
        "role": "Attending Physician",
        "department": "Emergency & Internal Medicine",
        "avatar": "👨‍⚕️",
        "badge_color": "#0284C7",
        "salt": "careflow_salt_doctor_2026",
        # Default password: "doctor123"
        "password_hash": hashlib.pbkdf2_hmac("sha256", b"doctor123", b"careflow_salt_doctor_2026", 100000).hex()
    },
    {
        "username": "nurse",
        "full_name": "Elena Vance, BSN, RN",
        "role": "Triage & Care Coordinator",
        "department": "Clinical Operations & Triage",
        "avatar": "👩‍⚕️",
        "badge_color": "#059669",
        "salt": "careflow_salt_nurse_2026",
        # Default password: "nurse123"
        "password_hash": hashlib.pbkdf2_hmac("sha256", b"nurse123", b"careflow_salt_nurse_2026", 100000).hex()
    },
    {
        "username": "admin",
        "full_name": "Marcus Sterling",
        "role": "Clinical Systems Administrator",
        "department": "Hospital IT & Governance",
        "avatar": "🛡️",
        "badge_color": "#4F46E5",
        "salt": "careflow_salt_admin_2026",
        # Default password: "admin123"
        "password_hash": hashlib.pbkdf2_hmac("sha256", b"admin123", b"careflow_salt_admin_2026", 100000).hex()
    },
    {
        "username": "analyst",
        "full_name": "Alex Rivera",
        "role": "Healthcare Quality Analyst",
        "department": "Operations & Performance",
        "avatar": "📊",
        "badge_color": "#D97706",
        "salt": "careflow_salt_analyst_2026",
        # Default password: "analyst123"
        "password_hash": hashlib.pbkdf2_hmac("sha256", b"analyst123", b"careflow_salt_analyst_2026", 100000).hex()
    }
]


def _hash_password(password: str, salt: str) -> str:
    """Hash password using PBKDF2 HMAC SHA-256."""
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000).hex()


def load_users() -> dict:
    """Load users from json file; initialize with defaults if not present."""
    if not AUTH_FILE.exists():
        save_users(DEFAULT_USERS)
        return {u["username"].lower(): u for u in DEFAULT_USERS}
    
    try:
        with open(AUTH_FILE, "r", encoding="utf-8") as f:
            user_list = json.load(f)
            return {u["username"].lower(): u for u in user_list}
    except Exception:
        save_users(DEFAULT_USERS)
        return {u["username"].lower(): u for u in DEFAULT_USERS}


def save_users(users):
    """Save user list or dict to json file."""
    if isinstance(users, dict):
        users_to_save = list(users.values())
    else:
        users_to_save = users
    with open(AUTH_FILE, "w", encoding="utf-8") as f:
        json.dump(users_to_save, f, indent=2)


def authenticate(username: str, password: str):
    """Verify credentials and return user object if valid, else None."""
    users = load_users()
    key = username.strip().lower()
    if key in users:
        user = users[key]
        salt = user.get("salt", "")
        expected_hash = user.get("password_hash", "")
        if _hash_password(password, salt) == expected_hash:
            return user
    return None


def register_user(username: str, full_name: str, role: str, department: str, password: str):
    """Register a new staff member."""
    users = load_users()
    key = username.strip().lower()
    if key in users:
        return False, "Username already exists. Please choose a different username."
    
    salt = secrets.token_hex(16)
    pw_hash = _hash_password(password, salt)
    
    # Assign icon based on role
    role_icons = {
        "Attending Physician": ("👨‍⚕️", "#0284C7"),
        "Triage & Care Coordinator": ("👩‍⚕️", "#059669"),
        "Clinical Systems Administrator": ("🛡️", "#4F46E5"),
        "Healthcare Quality Analyst": ("📊", "#D97706"),
        "Medical Resident": ("🩺", "#0284C7"),
        "Staff Nurse": ("💉", "#059669")
    }
    avatar, badge_color = role_icons.get(role, ("👤", "#64748B"))
    
    new_user = {
        "username": key,
        "full_name": full_name.strip(),
        "role": role,
        "department": department.strip() if department else "Clinical Care",
        "avatar": avatar,
        "badge_color": badge_color,
        "salt": salt,
        "password_hash": pw_hash,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    users[key] = new_user
    save_users(users)
    return True, new_user


def init_session_state():
    """Ensure session state variables for authentication are set."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "login_time" not in st.session_state:
        st.session_state["login_time"] = None


def login(user_info):
    """Set user session and trigger rerun."""
    st.session_state["authenticated"] = True
    st.session_state["user"] = user_info
    st.session_state["login_time"] = datetime.now().strftime("%I:%M %p")
    st.rerun()


def logout():
    """Clear session state and return to login screen."""
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.session_state["login_time"] = None
    st.rerun()


def render_login_page():
    """Render the full clinical portal sign-in experience."""
    # Hide sidebar, header, stop & deploy buttons on login page
    st.markdown("""
    <style>
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"],
        [data-testid="stAppDeployButton"],
        .stDeployButton,
        [data-testid="stStatusWidget"],
        .stStatusWidget,
        [data-testid="stToolbarActions"],
        [data-testid="stToolbar"],
        [data-testid="StyledFullScreenButton"],
        button[title="View fullscreen"],
        #MainMenu,
        [data-testid="stDecoration"],
        footer {
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
            height: 0 !important;
            opacity: 0 !important;
        }
        header[data-testid="stHeader"],
        .stAppHeader {
            background: transparent !important;
            height: 0px !important;
            min-height: 0px !important;
            padding: 0 !important;
            border: none !important;
        }
        .block-container {
            padding-top: 2rem !important;
        }
        .login-wrapper {
            max-width: 520px;
            margin: 20px auto 40px auto;
        }
        .login-header-card {
            background: linear-gradient(135deg, #0284C7 0%, #4F46E5 100%);
            border-radius: 20px 20px 0 0;
            padding: 32px 28px 28px 28px;
            text-align: center;
            color: #FFFFFF;
            box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.35);
        }
        .login-body-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-top: none;
            border-radius: 0 0 20px 20px;
            padding: 28px 28px 24px 28px;
            box-shadow: 0 16px 32px -8px rgba(15, 23, 42, 0.08);
        }
        .demo-pill-card {
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 12px 14px;
            margin-bottom: 10px;
            transition: all 0.2s ease;
        }
        .demo-pill-card:hover {
            border-color: #38BDF8;
            background: #F0F9FF;
            transform: translateY(-1px);
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2.2, 1])
    with col2:
        st.markdown("""
        <div class="login-wrapper">
            <div class="login-header-card">
                <div style="background: rgba(255,255,255,0.2); width: 56px; height: 56px; border-radius: 16px; margin: 0 auto 14px auto; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(8px);">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                    </svg>
                </div>
                <div style="font-weight: 800; font-size: 1.6rem; letter-spacing: -0.02em; margin-bottom: 4px;">CareFlow™</div>
                <div style="font-size: 0.88rem; opacity: 0.9; font-weight: 500;">Clinical Pathway Intelligence & Operations Portal</div>
                <div style="display: inline-flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.18); padding: 4px 12px; border-radius: 9999px; font-size: 0.72rem; margin-top: 14px; font-weight: 600;">
                    <span style="width: 6px; height: 6px; background: #34D399; border-radius: 50%; display: inline-block;"></span>
                    HIPAA & Clinical Governance Secured
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        tab_signin, tab_quick, tab_register = st.tabs([
            "🔐 Staff Sign In",
            "⚡ 1-Click Demo Profiles",
            "✨ Register Account"
        ])

        with tab_signin:
            st.markdown("<p style='font-size: 0.85rem; color: #64748B; margin-bottom: 16px;'>Enter your clinical credentials to access patient pathway analytics.</p>", unsafe_allow_html=True)
            with st.form("signin_form", clear_on_submit=False):
                username_input = st.text_input("Username or Staff ID", placeholder="e.g. doctor, nurse, or admin")
                password_input = st.text_input("Password", type="password", placeholder="Enter your password")
                submit_login = st.form_submit_button("Sign In to Portal", type="primary", use_container_width=True)

                if submit_login:
                    if not username_input or not password_input:
                        st.error("Please enter both username and password.")
                    else:
                        user = authenticate(username_input, password_input)
                        if user:
                            st.success(f"Welcome back, {user['full_name']}!")
                            login(user)
                        else:
                            st.error("Invalid credentials. Try a demo account from the '1-Click Demo Profiles' tab.")

        with tab_quick:
            st.markdown("<p style='font-size: 0.82rem; color: #64748B; margin-bottom: 12px;'>Select a pre-configured clinical profile for instantaneous evaluation:</p>", unsafe_allow_html=True)
            
            users = load_users()
            preset_keys = ["doctor", "nurse", "admin", "analyst"]
            
            for key in preset_keys:
                if key in users:
                    u = users[key]
                    c_info, c_btn = st.columns([3, 1.2])
                    with c_info:
                        st.markdown(f"""
                        <div class="demo-pill-card">
                            <div style="font-weight: 700; font-size: 0.88rem; color: #0F172A;">
                                {u['avatar']} {u['full_name']}
                            </div>
                            <div style="font-size: 0.75rem; color: {u['badge_color']}; font-weight: 600;">
                                {u['role']}
                            </div>
                            <div style="font-size: 0.7rem; color: #94A3B8;">
                                User: <code>{u['username']}</code> | Pass: <code>{key}123</code>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    with c_btn:
                        st.write("")
                        if st.button(f"Sign In", key=f"quick_{key}", use_container_width=True, type="secondary"):
                            login(u)

        with tab_register:
            st.markdown("<p style='font-size: 0.85rem; color: #64748B; margin-bottom: 16px;'>Register a new clinical staff account with role permissions.</p>", unsafe_allow_html=True)
            with st.form("register_form", clear_on_submit=False):
                reg_name = st.text_input("Full Name & Credentials", placeholder="e.g. Dr. Emily Chen, MD")
                reg_role = st.selectbox("Clinical Role", [
                    "Attending Physician",
                    "Triage & Care Coordinator",
                    "Staff Nurse",
                    "Medical Resident",
                    "Healthcare Quality Analyst",
                    "Clinical Systems Administrator"
                ])
                reg_dept = st.text_input("Department / Unit", placeholder="e.g. Emergency Department, Cardiology")
                reg_user = st.text_input("Desired Username", placeholder="e.g. echen")
                reg_pass = st.text_input("Create Password", type="password", placeholder="Min 6 characters")
                reg_pass2 = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
                
                submit_register = st.form_submit_button("Register & Sign In", type="primary", use_container_width=True)

                if submit_register:
                    if not reg_name.strip() or not reg_user.strip() or not reg_pass:
                        st.error("Please fill in all required fields.")
                    elif len(reg_pass) < 6:
                        st.error("Password must be at least 6 characters long.")
                    elif reg_pass != reg_pass2:
                        st.error("Passwords do not match.")
                    else:
                        success, res = register_user(reg_user, reg_name, reg_role, reg_dept, reg_pass)
                        if success:
                            st.success(f"Account created successfully for {reg_name}!")
                            login(res)
                        else:
                            st.error(res)

        st.markdown("""
        <div style="text-align: center; margin-top: 24px; font-size: 0.75rem; color: #94A3B8;">
            Protected Clinical System • CareFlow™ v2.6 • Authorized Personnel Only
        </div>
        """, unsafe_allow_html=True)


def render_user_sidebar():
    """Render the active user profile widget and sign-out controls in the sidebar."""
    user = st.session_state.get("user")
    if not user:
        return

    st.sidebar.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 14px; padding: 14px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 40px; height: 40px; border-radius: 10px; background: {user.get('badge_color', '#0284C7')}15; border: 1px solid {user.get('badge_color', '#0284C7')}30; display: flex; align-items: center; justify-content: center; font-size: 1.3rem;">
                {user.get('avatar', '👤')}
            </div>
            <div style="flex: 1; min-width: 0;">
                <div style="font-weight: 700; font-size: 0.88rem; color: #0F172A; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    {user.get('full_name', 'Staff Member')}
                </div>
                <div style="font-size: 0.72rem; color: {user.get('badge_color', '#0284C7')}; font-weight: 600;">
                    {user.get('role', 'Clinical Staff')}
                </div>
            </div>
        </div>
        <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid #F1F5F9; display: flex; justify-content: space-between; align-items: center; font-size: 0.7rem; color: #94A3B8;">
            <span>Unit: {user.get('department', 'Care Unit')}</span>
            <span style="color: #10B981; font-weight: 600;">● Active</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_user_header():
    """Render a clean top profile status chip with single sign-out button in the main container."""
    user = st.session_state.get("user")
    if not user:
        return

    col_brand, col_user = st.columns([2.0, 2.0])
    with col_brand:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px; margin-top: 8px;">
            <span style="display: inline-block; width: 8px; height: 8px; background: #10B981; border-radius: 50%;"></span>
            <span style="font-size: 0.82rem; font-weight: 700; color: #0284C7; letter-spacing: 0.02em;">CAREFLOW INTELLIGENCE PORTAL</span>
            <span style="font-size: 0.75rem; color: #CBD5E1;">•</span>
            <span style="font-size: 0.75rem; color: #64748B;">Clinical Operations & Intelligence</span>
        </div>
        """, unsafe_allow_html=True)

    with col_user:
        c_prof, c_btn = st.columns([2.3, 1.0])
        with c_prof:
            st.markdown(f"""
            <div style="text-align: right; line-height: 1.25; margin-top: 4px;">
                <span style="font-size: 0.84rem; font-weight: 700; color: #0F172A;">{user.get('avatar', '👤')} {user.get('full_name')}</span><br>
                <span style="font-size: 0.72rem; color: {user.get('badge_color', '#0284C7')}; font-weight: 600;">{user.get('role')}</span>
            </div>
            """, unsafe_allow_html=True)
        with c_btn:
            if st.button("Sign Out", key="single_signout_btn", use_container_width=True, type="secondary"):
                logout()
