# 1. 빌드 스테이지
FROM python:3.12-slim AS builder

WORKDIR /app

# 빌드 필수 도구 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 가상환경 생성 및 의존성 설치
COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# 2. 실행 스테이지
FROM python:3.9-slim

WORKDIR /app

# 빌드 스테이지에서 가상환경만 복사
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 파이썬 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 프로젝트 전체 복사
COPY . .

# FastAPI 실행 포트
EXPOSE 8000

# 프로젝트 구조에 맞춘 실행 명령어
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]