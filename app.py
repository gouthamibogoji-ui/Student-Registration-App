import streamlit as st  # type: ignore
import mysql.connector  # type: ignore
import pandas as pd  # type: ignore
import bcrypt  # type: ignore

# ---------------- DATABASE CONNECTION ----------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="S4499",
        database="webgui"
    )

# ---------------- PASSWORD FUNCTIONS ----------------
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# ---------------- AUTH FUNCTIONS ----------------
def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return False, "Username not found"
    if not verify_password(password, row[0]):
        return False, "Invalid password"
    return True, "Login successful"

def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
    if cursor.fetchone():
        conn.close()
        return False, "Username already exists"

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s,%s)",
        (username, hash_password(password))
    )
    conn.commit()
    conn.close()
    return True, "Account created successfully"

def reset_password(username, new_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
    if not cursor.fetchone():
        conn.close()
        return False, "Username not found"

    cursor.execute(
        "UPDATE users SET password=%s WHERE username=%s",
        (hash_password(new_password), username)
    )
    conn.commit()
    conn.close()
    return True, "Password reset successful"

# ---------------- CRUD FUNCTIONS ----------------
def load_students():
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM registration ORDER BY id", conn)
    conn.close()
    return df

def add_student(name, course, fee):
    if not name or not course:
        st.error("All fields required")
        return
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO registration (name, course, fee) VALUES (%s,%s,%s)",
        (str(name), str(course), int(fee))
    )
    conn.commit()
    conn.close()
    st.success("Student added successfully")

def update_student(sid, name, course, fee):
    if sid is None:
        st.error("Select a student first")
        return
    if not name or not course:
        st.error("Name and Course cannot be empty")
        return
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE registration SET name=%s, course=%s, fee=%s WHERE id=%s",
        (str(name), str(course), int(fee), int(sid))
    )
    conn.commit()
    conn.close()
    st.success("Student updated successfully")

def delete_student(sid):
    if sid is None:
        st.error("Select a student first")
        return
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM registration WHERE id=%s", [int(sid)])
    conn.commit()
    conn.close()
    st.success("Student deleted successfully")

# ---------------- SESSION STATE INIT ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "login"
if "username" not in st.session_state:
    st.session_state.username = ""
if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = False

# ---------------- AUTH UI ----------------
if not st.session_state.logged_in:
    st.title("🔐 Authentication")

    cols = st.columns(3)
    if cols[0].button("Login"):
        st.session_state.page = "login"
    if cols[1].button("Register"):
        st.session_state.page = "register"
    if cols[2].button("Forgot Password"):
        st.session_state.page = "reset"

    st.divider()

    # ---------- LOGIN ----------
    if st.session_state.page == "login":
        st.subheader("Login")

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login Now")

        if submit:
            ok, msg = login_user(username.strip(), password.strip())
            if ok:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    # ---------- REGISTER ----------
    elif st.session_state.page == "register":
        st.subheader("Register")

        user = st.text_input("New Username")
        pwd = st.text_input("New Password", type="password")
        cpwd = st.text_input("Confirm Password", type="password")

        if st.button("Create Account"):
            if not user or not pwd:
                st.error("All fields required")
            elif pwd != cpwd:
                st.error("Passwords do not match")
            elif len(pwd) < 6:
                st.error("Minimum 6 characters")
            else:
                ok, msg = register_user(user.strip(), pwd)
                if ok: 
                    st.success(msg) 
                else:
                    st.error(msg)

    # ---------- RESET ----------
    elif st.session_state.page == "reset":
        st.subheader("Reset Password")

        user = st.text_input("Username")
        pwd = st.text_input("New Password", type="password")

        if st.button("Reset Password"):
            ok, msg = reset_password(user.strip(), pwd)
            if ok: 
                st.success(msg)
            else:
                st.error(msg)

    st.stop()

# ---------------- MAIN APP ----------------
st.title("🎓 Student Registration System")
st.write(f"👤 Logged in as **{st.session_state.username}**")

df = load_students()

choice = st.selectbox(
    "Select Student",
    ["New Student"] + df["id"].astype(str).tolist()
)

if choice != "New Student":
    row = df[df["id"] == int(choice)].iloc[0]
    sid = row["id"]
    name = row["name"]
    course = row["course"]
    fee = row["fee"]
else:
    sid=None
    name=""
    course="" 
    fee =0

name = st.text_input("Name", name)
course = st.text_input("Course", course)
fee = st.number_input("Fee",
                    min_value=0,
                    value=int(fee),
                    step=1000
)

c1, c2, c3 = st.columns(3)
if c1.button("Add"):
    add_student(name, course, fee)
if c2.button("Update") and sid is not None:
    update_student(sid, name, course, fee)
if c3.button("Delete") and sid is not None:
    st.session_state.confirm_delete = True
if st.session_state.confirm_delete and sid:
    st.warning(f"⚠️ Are you sure you want to delete student ID {sid}?")

    y, n = st.columns(2)
    if y.button("Yes, Delete"):
        delete_student(sid)
        st.session_state.confirm_delete = False

    if n.button("Cancel"):
        st.session_state.confirm_delete = False

st.dataframe(df, use_container_width=True)

if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()
