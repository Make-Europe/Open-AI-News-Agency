# 📰 AI News Email Summarizer

This script fetches your latest Gmail message and summarizes it using Google Cloud Vertex AI (Gemini).

## ✅ Requirements

- Python 3.9 or newer
- Google Cloud project with:
  - Vertex AI API enabled
  - Gmail API enabled

## 🛠 Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install google-auth google-auth-oauthlib google-api-python-client google-cloud-aiplatform
```

1. Place `main.py` in your project folder.
2. Download `client_secret.json` from Google Cloud Console.
3. Enable the Gmail API for your project.
4. Run the script:

```bash
python3 main.py
```

## 📄 Files

| File | Description |
|------|-------------|
| main.py | Main script |
| client_secret.json | OAuth credentials (keep private) |
| token.json | Auto-generated after authentication |

## 🧠 Workflow

1. Authenticates with Gmail.
2. Fetches the latest email.
3. Sends content to Vertex AI (Gemini).
4. Outputs a concise news-style summary.

## 📌 Notes

- Do not share `client_secret.json` or `token.json`.
- Ensure the Gemini model is available in your region (e.g., `us-central1`).
- Customize the prompt in `main.py` as needed.

## 🛑 Troubleshooting

- Ensure billing is enabled on your Google Cloud project.
- Use a supported model name and region.

## 📜 License

MIT License © [MAKE Europe GmbH](https://make-europe.com)
