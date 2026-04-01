FROM anasty17/mltb:dev

WORKDIR /mltb
RUN chmod 777 /mltb

COPY requirements.txt .
RUN python3 -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash", "start.sh"]