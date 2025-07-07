from apscheduler.schedulers.blocking import BlockingScheduler
from main import get_latest_email, summarize_email
from datetime import datetime

def run_summary():
    print(f"⏰ Running at {datetime.now()}")
    email_body = get_latest_email()
    if email_body:
        summary = summarize_email(email_body)
        print("\n📰 --- AI-Generated News Summary ---\n")
        print(summary)
        with open("summaries.log", "a") as f:
            f.write(f"{datetime.now()}\n{summary}\n\n")
    else:
        print("❌ No email found.")

sched = BlockingScheduler()
sched.add_job(run_summary, 'interval', minutes=10)

if __name__ == "__main__":
    print("📡 AI News Scheduler started. Checking every 10 minutes.")
    sched.start()

