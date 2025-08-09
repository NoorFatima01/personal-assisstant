def weekly_goal_email(user_name: str, upload_link: str):
    subject = "🌟 Time to Upload Your Weekly Goals!"
    body = f"""
    Hi {user_name},

    A brand new week is here — and with it, a fresh opportunity to stay on track with your goals! 🚀

    Your progress matters, and your weekly schedule documents help you stay organized, motivated, and moving forward.

    📅 Action Step: Please upload your new documents for this week.
    💡 Pro Tip: Consistency builds momentum — and momentum builds success.

    Let's make this week your best one yet!
    You've got this. 💪

    Upload now: {upload_link}

    —
    Your Weekly Goals Assistant
    Helping you stay on track, one week at a time.
    """
    return subject, body
