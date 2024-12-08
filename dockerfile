FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# ENV HOST=127.0.0.1
# ENV PORT=5000
# ENV POSTGRES_URL=postgresql://postgres:1sampai8@127.0.0.1/shopee
# ENV REDIS_URL=redis://127.0.0.1:6379/0
# ENV SHOPEE_PARTNER_ID=your_partner_id
# ENV SHOPEE_PARTNER_KEY=your_partner_key
# ENV SHOPEE_SHOP_ID=your_shop_id

EXPOSE 5000

# CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
CMD ["python", "main.py"]
