import re
import streamlit as st
import requests


# Functions
@st.cache_data(ttl=3600)
def get_available_programs():
    try:
        if st.secrets["development_env"] == "production":
            backend_url = st.secrets["backend_url"]
        else:
            backend_url = "http://localhost:8000"
        response = requests.get(backend_url + "/vectorized-programs")
        if response.status_code == 200:
            vectorized_programs = response.json()
            return vectorized_programs
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None


def send_message(agent, message):
    if st.secrets["development_env"] == "production":
        backend_url = st.secrets["backend_url"]
    else:
        backend_url = "http://127.0.0.1:8000"
    if agent == "LLama Index":
        api_url = f"{backend_url}/chat_llama"
    elif agent == "LangChain":
        api_url = f"{backend_url}/chat_langchain"
    else:
        api_url = f"{backend_url}/chat_openai"
    response = requests.post(api_url, json={"question": message})
    response_json = response.json()
    return response_json["reply"]


def remove_line_numbers(text):
    # This regex pattern targets numbers followed by a newline and spaces
    pattern = r"\d+\s*\n"
    cleaned_text = re.sub(pattern, "\n", text)
    return cleaned_text.strip()


def get_election_program(file_name):
    if st.secrets["election_program_url"]:
        election_program_url = st.secrets["election_program_url"]
        url = election_program_url + file_name
        # download the pdf
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            return None
    else:
        return None


# Main
st.set_page_config(
    page_title="Chat Your Election Program", page_icon="💬", layout="centered"
)

with st.sidebar:
    with st.expander("""Disclaimer"""):
        st.write(
            """This chatbot provides general informational content and does not offer political, legal, or professional advice. Responses are algorithmically generated and may not fully capture current political developments. Reliance on the information from this chatbot for decision-making is at your own risk, and the chatbot does not endorse any specific political parties or views."""
        )
    st.title("Available Election Programs")
    vectorized_programs = get_available_programs()
    if vectorized_programs is not None:
        for program in vectorized_programs:
            st.write(f"{program['full_name']} ({program['label']})")
    else:
        st.write("No election programs available.")
    st.markdown("")
    st.markdown("")
    "[View the source code](https://github.com/RichardKruemmel/chat-your-gesetzentwurf)"

st.title("Chat Your Election Program")

agent = st.selectbox("Select your AI", ["LLama Index", "LangChain", "ChatGPT"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": f"Hello! I am your german election program expert. How can I help you?",
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Waiting for a response..."):
        api_response = send_message(agent, prompt)

    st.session_state.messages.append(
        {"role": "assistant", "content": api_response["response"]}
    )
    with st.chat_message("assistant"):
        print(api_response)
        st.markdown(api_response["response"])
    if agent == "LLama Index":
        if api_response["source_nodes"] != []:
            with st.expander("Sources"):
                for source_node in api_response["source_nodes"]:
                    cleaned_text = remove_line_numbers(source_node["node"]["text"])
                    st.write(
                        "Page Number: " + source_node["node"]["metadata"]["page_label"]
                    )
                    st.write("Excerpt: " + cleaned_text)
                    st.markdown("")

                election_id = api_response["source_nodes"][0]["node"]["metadata"][
                    "election_id"
                ]
                program_id = api_response["source_nodes"][0]["node"]["metadata"][
                    "election_program_id"
                ]
                program = get_election_program(f"{election_id}/{program_id}.pdf")

                if program is not None:
                    st.download_button(
                        label="Download Election Program",
                        data=program,
                        mime="application/pdf",
                    )
        else:
            st.warning(
                "No sources found. This answer is not backed by an election program."
            )
