import streamlit as st

st.set_page_config(
    page_title="Login / Register",
    page_icon="🔑",
    layout="centered"
)

# ---------- Initialise session state ----------
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("🔒 Authentication")
    st.markdown("Use this menu to navigate and manage your account.")

    if st.session_state.logged_in:
        st.success(f"Logged in as **{st.session_state.username}**")
        if st.button("Go to Dashboard"):
            st.switch_page("pages/1_Dashboard.py")
    else:
        st.info("Not logged in.")

    st.divider()

    # Optional theme selector (just demo)
    theme = st.radio("Theme Mode", ["Light", "Dark"], index=0)
    st.caption("This toggle does not change the theme yet—just for demo!")

    st.divider()
    st.markdown("made by raihan")


# ---------- MAIN PAGE ----------
st.title("🔐 Welcome")

# If already logged in, skip login/register
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username}**.")
    if st.button("Go to dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    st.stop()

# ---------- Tabs: Login / Register ----------
tab_login, tab_register = st.tabs(["Login", "Register"])

# ----- LOGIN TAB -----
with tab_login:
    st.subheader("Login")

    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log in", type="primary"):
        users = st.session_state.users

        if login_username in users and users[login_username] == login_password:
            st.session_state.logged_in = True
            st.session_state.username = login_username

            st.success(f"Welcome back, {login_username}! 🎉")
            st.switch_page("pages/1_Dashboard.py")
        else:
            st.error("Invalid username or password.")

# ----- REGISTER TAB -----
with tab_register:
    st.subheader("Register")

    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")

    if st.button("Create account"):
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        elif new_username in st.session_state.users:
            st.error("Username already exists.")
        else:
            st.session_state.users[new_username] = new_password
            st.success("Account created! You can now log in from the Login tab.")
