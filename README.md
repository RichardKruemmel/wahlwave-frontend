# Wahlwave Frontend

Welcome to Wahlwave Frontend, a Streamlit-based interface integrated with a FastAPI backend, offering a unique way to explore German election programs using AI technologies like Llama-Index, LangChain, and ChatGPT.

Features at a Glance:

- AI-Driven Insights: Engage with insightful AI interpretations of German election programs.
- Interactive Sidebar: Easily view and access a variety of available election programs.
- In-Depth Analysis with LLama Index: Get detailed answers, including page references and text excerpts from election program PDFs (Llama Index only).
- Downloadable Content: Option to download full election program PDFs for thorough analysis (Llama Index only).
- Comparative Research Tool: Compare responses across different AI agents, offering diverse perspectives on the data.

## Running locally

### Prerequisite

- Python 3.11 or higher installed
- [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) for package management installed

### Clone the Project

Clone the project repository from GitHub:

```bash
git clone https://github.com/RichardKruemmel/wahlwave-frontend
```

### Set Environment Variables

A `sample.secrets.toml` file is included in the project under .streamlit folder repository as a template for your own `secrets.toml` file. Copy the `sample.secrets.toml` file and rename the copy to `secrets.toml`:

```bash
cd .streamlit
cp sample.secrets.toml secrets.toml
```

Edit the secrets.toml file to set your own environment variables.

### Starting the frontend

Follow these commands:

```bash
  # Create a virtual environment
  $ poetry shell
  # Install all packages
  $ poetry install
  # Start frontend on http://localhost:8500
  $ poetry run streamlit run app.py
```

### Connecting to backend

The backend is stored in a separate repository, which you can find [here](https://github.com/RichardKruemmel/chat-your-gesetzentwurf.git).

Please follow the README inside the backend repository to run it locally.

## Deployment

When running the frontend you can see the option to deploy it via Steamlit. For more information visit their [documentation](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app).

This version is currently deployed under [wahlwave.streamlit.app](https://wahlwave.streamlit.app/)
