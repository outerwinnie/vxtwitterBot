FROM python:3.9-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV DISCORD_TOKEN="<TOKEN_HERE>"
ENV REPLY_TO=0
ENV DELETE_OP=1
ENV PREAMBLE="escribio:\n"
ENV MATCH1="https://twitter.com"
ENV MATCH2="https://x.com"
ENV MATCH3="https://instagram.com"
ENV REPLACE="https://vxtwitter.com"
ENV REPLACE="https://ddinstagram.com"

COPY . .
CMD ["python", "./main.py"]