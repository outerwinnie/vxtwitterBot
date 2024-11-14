FROM python:3.9-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV DISCORD_TOKEN="<TOKEN_HERE>"
ENV REPLY_TO=0
ENV DELETE_OP=1
ENV PREAMBLE="escribio:\n"
ENV MATCH1="https://twitter.com"
ENV MATCH2="https://x.com"
ENV MATCH3="https://www.instagram.com"
ENV MATCH4="https://www.tiktok.com"
ENV MATCH5="https://vm.tiktok.com"
ENV MATCH6="https://bsky.app"
ENV REPLACE="https://vxtwitter.com"
ENV REPLACE2="https://ddinstagram.com"
ENV REPLACE3="https://vxtiktok.com"
ENV REPLACE3="https://cbsky.app"

COPY . .
CMD ["python", "./main.py"]