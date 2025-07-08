# 🗺️ AI News Agency – Roadmap

This roadmap outlines the short-, mid-, and long-term goals for the **AI News Agency**, an automated system that reads Gmail updates and converts them into concise, publishable news summaries using Google Cloud's Vertex AI (Gemini).

---

## ✅ CURRENT STATUS

- [x] ✅ Fetches latest Gmail message via Gmail API
- [x] ✅ Summarizes using Gemini (Vertex AI)
- [x] ✅ Runs manually via `main.py`
- [x] ✅ Local deduplication using `last_id.txt`

---

## 🏁 SHORT-TERM GOALS (MVP)

1. **✅ Cron Automation**
   - Set up a `cron` job on the server to run `main.py` every 10–30 minutes

2. **✅ Log Summaries**
   - Save each summary to `summaries.log` or an SQLite/CSV file for history

3. **🛠️ Refactor main.py**
   - Clean up structure (split into modules)
   - Add logging and error handling
   - Add `--force` CLI flag to bypass `last_id.txt` check

4. **🔒 Hide Secrets**
   - Use `.env` or config parser for `PROJECT_ID`, paths, and sensitive variables
   - Add `.gitignore` for `token.json`, `client_secret.json`, etc.

---

## 🚀 MID-TERM GOALS

5. **🌍 Web Frontend**
   - Lightweight frontend to display latest summaries (Flask, FastAPI, or Node.js)
   - Markdown-to-HTML rendering for formatted summaries
   - Secure dashboard to view/manage summaries

6. **📝 Publish to WordPress**
   - REST integration or plugin-based publishing
   - Button-based or automatic daily post scheduler

7. **📤 Email Digest Option**
   - Optional email out: send daily summaries to subscribers using SMTP or Mailgun

8. **🗃️ Store Metadata**
   - Save subject, sender, date, and category tags with each summary
   - Enable search/filter on frontend

---

## 🌐 LONG-TERM GOALS

9. **📡 Multi-Source Ingestion**
   - Connect to RSS, Twitter/X, LinkedIn, or press APIs
   - Classify and sort by topic: Finance, Sports, Politics, etc.

10. **📊 Analytics Dashboard**
    - Count articles per source
    - Track publishing cadence and Gemini API usage

11. **🤖 Multi-Agent Pipeline**
    - Add a classifier to sort input into categories
    - Different Gemini prompts per topic (Finance, Breaking News, Culture)

12. **🔗 Tokenized Access (optional)**
    - NFT/microcredential for journalist access
    - Private vs public content publishing

---

## 📌 NOTES

- Run `python3 main.py` manually to test Gmail > Gemini flow
- Always check if `gcloud auth application-default login` is still valid
- Use `summaries.log` as a quick output for any web integration

---

## 🧪 TESTED ON

- Python 3.8–3.11
- Vertex AI Gemini 2.5 Pro (us-central1)
- Gmail API + OAuth2 Desktop Flow

---

## 📄 License

MIT – © MAKE Europe GmbH  
https://make-europe.com
