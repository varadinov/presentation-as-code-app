FROM python:3.11-slim AS builder

RUN pip install uv

WORKDIR /app

COPY pyproject.toml ./

RUN uv sync

COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx nodejs npm\
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /app/presentations \
    && touch /app/presentations/index.html

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 8000

# Start both Nginx and the Streamlit app
CMD ["sh", "-c", ".venv/bin/streamlit run main.py & nginx -g 'daemon off;'"]