# opsagent-ai-hackathon-2025
## Setup
- Clone the repo
- With python installed run `python3 -m venv envi`
- Activate virtual environment using `source envi/bin/activate`
- Install dependency `pip install -r requirements.txt`
- Get API key of Gemini from [Google AI studio](https://aistudio.google.com/). If account is not there signup.
- Add .env file with `GITHUB_TOKEN=xx`,`GOOGLE_API_KEY=xxx` and `GOOGLE_GENAI_USE_VERTEXAI=0`
- Install [kubectl-ai](https://github.com/GoogleCloudPlatform/kubectl-ai/tree/main)
- Install npm using `brew install npm node`
- Run `adk web` you can access UI from localhost:8000
## Links
- Google ADK - [Github](https://github.com/google/adk-python), [Documentation](https://google.github.io/adk-docs/)
- [kubectl-ai](https://github.com/GoogleCloudPlatform/kubectl-ai/tree/main)