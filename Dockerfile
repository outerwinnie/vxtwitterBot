FROM python:3.9-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV DISCORD_TOKEN="<TOKEN_HERE>"
ENV DELETE_OP=1
ENV PREAMBLE="escribio:\n"
ENV TWITTER_MATCH="https://twitter.com"
ENV X_MATCH="https://x.com"
ENV INSTAGRAM_MATCH="https://www.instagram.com"
ENV INSTAGRAM_REEL_MATCH="https://www.instagram.com/reel/"
ENV TIKTOK_MATCH="https://www.tiktok.com"
ENV TIKTOK_VM_MATCH="https://vm.tiktok.com"
ENV BLUESKY_MATCH="https://bsky.app"
ENV YOUTUBE_MATCH_1="https://www.youtube.com/watch"
ENV YOUTUBE_MATCH_2="https://youtube.com/watch"
ENV TWITTER_REPLACE="https://vxtwitter.com"
ENV INSTAGRAM_REPLACE="https://ddinstagram.com"
ENV INSTAGRAM_REEL_REPLACE="https://kkinstagram.com"
ENV TIKTOK_REPLACE="https://vxtiktok.com"
ENV BLUESKY_REPLACE="https://cbsky.app"
ENV YOUTUBE_REPLACE="http://inv.nadeko.net"

COPY . .
CMD ["python", "./main.py"]
