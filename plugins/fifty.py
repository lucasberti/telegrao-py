import praw
from random import choice
from api import send_message


def on_msg_received(msg, matches):
    chat = msg["chat"]["id"]

    try:
        reddit = praw.Reddit(client_id="aEURITEt-YUgBQ", client_secret="Bd1cZ0OaS15znwNwKSCDtWH2-pg", user_agent="ed_reborn")

        entries = []
        for submission in reddit.subreddit('FiftyFifty').hot(limit=1000):
            entries.append({"title": submission.title, "url": submission.url})

        chosen = choice(entries)
        print(f"[{chosen['title']}]({chosen['url']})")

        title = chosen['title'].replace("(", "{").replace(")", "}").replace("[", "{").replace("]", "}")
        url = chosen['url']

        with open("/var/www/html/fiftyfifty", "w") as f:
            f.write(f"""<script language="JavaScript"> 
window.location="{url}"; 
</script>""")

        send_message(chat, f"[{title}](https://lucasberti.me/fiftyfifty", disable_web_page_preview="true")
    except:
        send_message(chat, "ops deu mreda....")