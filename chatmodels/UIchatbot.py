import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

load_dotenv()

st.set_page_config(page_title="Mood AI Chatbot", page_icon="🤖", layout="centered")

# ---------- Modes (same choices and system prompts as the original script) ----------
MODES = {
    1: {
        "name": "Angry AI",
        "emoji": "😡",
        "tagline": "Aggressive and impatient. Don't waste its time.",
        "prompt": "You are an angry AI agent. You respond aggressively and impatiently.",
        "c1": "#ff5f6d",
        "c2": "#ffc371",
    },
    2: {
        "name": "Funny AI",
        "emoji": "😂",
        "tagline": "Humor and jokes in every single reply.",
        "prompt": "You are a very funny  AI agent. You respond with humor and jokes.",
        "c1": "#f7971e",
        "c2": "#ffd200",
    },
    3: {
        "name": "Sad AI",
        "emoji": "😢",
        "tagline": "A heartbroken soul who needs to talk.",
        "prompt": "You are an sad AI agent. you respond with heartborken person",
        "c1": "#4776e6",
        "c2": "#8e54e9",
    },
}

# ---------- Styling ----------
st.markdown(
    """
    <style>
    #MainMenu, footer {visibility: hidden;}
    .stApp {
        background: radial-gradient(circle at 20% 0%, #1b1f3a 0%, #0e1117 55%);
    }
    .hero {
        text-align: center;
        padding: 1.5rem 0 1rem 0;
    }
    .hero h1 {
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: .2rem;
        background: linear-gradient(90deg, #ff5f6d, #ffc371, #8e54e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero p { color: #9aa0b4; font-size: 1.05rem; }

    .mode-card {
        border-radius: 18px;
        padding: 1.6rem 1rem 1.2rem 1rem;
        text-align: center;
        color: white;
        min-height: 190px;
        box-shadow: 0 10px 30px rgba(0,0,0,.35);
        transition: transform .2s ease;
    }
    .mode-card:hover { transform: translateY(-4px); }
    .mode-card .emoji { font-size: 3rem; }
    .mode-card .title { font-size: 1.25rem; font-weight: 700; margin-top: .3rem; }
    .mode-card .desc { font-size: .88rem; opacity: .92; margin-top: .3rem; }

    .chat-header {
        border-radius: 18px;
        padding: 1rem 1.4rem;
        color: white;
        display: flex;
        align-items: center;
        gap: 1rem;
        box-shadow: 0 8px 24px rgba(0,0,0,.35);
        margin-bottom: 1.2rem;
    }
    .chat-header .emoji { font-size: 2.4rem; }
    .chat-header .title { font-size: 1.4rem; font-weight: 700; line-height: 1.1; }
    .chat-header .sub { font-size: .85rem; opacity: .9; }

    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,.04);
        border: 1px solid rgba(255,255,255,.06);
        border-radius: 16px;
        padding: .8rem 1rem;
    }
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Session state ----------
if "model" not in st.session_state:
    st.session_state.model = ChatGroq(model="openai/gpt-oss-120b", temperature=0.9)
if "choice" not in st.session_state:
    st.session_state.choice = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "ended" not in st.session_state:
    st.session_state.ended = False


def select_mode(choice: int):
    st.session_state.choice = choice
    st.session_state.messages = [SystemMessage(content=MODES[choice]["prompt"])]
    st.session_state.ended = False


def reset_chat():
    st.session_state.choice = None
    st.session_state.messages = []
    st.session_state.ended = False


# ---------- Screen 1: choose a mode ----------
if st.session_state.choice is None:
    st.markdown(
        """
        <div class="hero">
            <h1>🤖 Mood AI Chatbot</h1>
            <p>Choose your model to get started</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(3, gap="medium")
    for col, (key, mode) in zip(cols, MODES.items()):
        with col:
            st.markdown(
                f"""
                <div class="mode-card"
                     style="background: linear-gradient(135deg, {mode['c1']}, {mode['c2']});">
                    <div class="emoji">{mode['emoji']}</div>
                    <div class="title">{mode['name']}</div>
                    <div class="desc">{mode['tagline']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.button(
                f"Choose {mode['name']}",
                key=f"choose_{key}",
                on_click=select_mode,
                args=(key,),
            )

# ---------- Screen 2: chat ----------
else:
    mode = MODES[st.session_state.choice]

    with st.sidebar:
        st.markdown(f"### {mode['emoji']} {mode['name']}")
        st.caption("Type **0** in the chat to exit the chatbot.")
        st.button("🔄 New chat / change model", on_click=reset_chat)

    st.markdown(
        f"""
        <div class="chat-header"
             style="background: linear-gradient(135deg, {mode['c1']}, {mode['c2']});">
            <div class="emoji">{mode['emoji']}</div>
            <div>
                <div class="title">{mode['name']}</div>
                <div class="sub">{mode['tagline']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Chat history
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user", avatar="🧑"):
                st.write(msg.content)
        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant", avatar=mode["emoji"]):
                st.write(msg.content)

    if st.session_state.ended:
        st.info("Chat ended. Use **New chat / change model** in the sidebar to start again.")

    prompt = st.chat_input("You: ", disabled=st.session_state.ended)

    if prompt:
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("user", avatar="🧑"):
            st.write(prompt)

        if prompt == "0":
            st.session_state.ended = True
            st.info("Chat ended. Use **New chat / change model** in the sidebar to start again.")
            st.stop()

        with st.chat_message("assistant", avatar=mode["emoji"]):
            with st.spinner("Thinking..."):
                response = st.session_state.model.invoke(st.session_state.messages)
            st.write(response.content)

        st.session_state.messages.append(AIMessage(content=response.content))