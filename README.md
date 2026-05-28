# Banolim AI Engine (반올림 AI 엔진)

> 경계선 지능(BIF) 아동 및 초등학생을 위한 개인화 맞춤형 언어 교육 & 공감 소통 AI 엔진

---

## 목차

1. [프로젝트 소개](#-프로젝트-소개)
2. [팀 소개](#-팀-소개)
3. [사용 기술 스택](#-사용-기술-스택)
4. [기능](#-기능)

---

## 프로젝트 소개

`banolim-ai`는 느린 학습자(경계선 지능 아동, Borderline Intellectual Functioning)와 초등학생의 어휘력, 문해력, 사회적 소통 능력 향상을 돕기 위해 개발되었습니다.

본 엔진은 FastAPI 기반 서비스로 설계되었으며, 메인 백엔드(Spring Boot)와 연동되어 작동합니다. 멀티모달 비전 기술을 통한 교육 데이터 가공 파이프라인부터 LLM(GPT, Claude)과 TTS(ElevenLabs)를 융합하여 아동 인지 발달 단계에 맞춘 교육 콘텐츠를 실시간으로 생성합니다.

---

## 팀 소개

<table>
  <tr>
    <td align="center" width="230px">
      <img src="https://github.com/gimn70009.png" width="120px" alt="gimn70009 Profile"/><br />
      <br />
      <a href="https://github.com/gimn70009"><b>gimn70009</b></a><br />
      Backend Developer
      <br />
      <small>챗봇 / 문장분해 / 데이터 파이프라인</small>
    </td>
    <td align="center" width="230px">
      <img src="https://github.com/youserlol.png" width="120px" alt="youserlol Profile"/><br />
      <br />
      <a href="https://github.com/youserlol"><b>youserlol</b></a><br />
      Backend Developer
      <br />
      <small>챗봇 / 문장분해 / 데이터 파이프라인</small>
    </td>
    <td align="center" width="230px">
      <img src="https://github.com/7hokerz.png" width="120px" alt="7hokerz Profile"/><br />
      <br />
      <a href="https://github.com/7hokerz"><b>7hokerz</b></a><br />
      Backend Developer
      <br />
      <small>단어장 / 예문 생성</small>
    </td>
  </tr>
</table>

---

## 사용 기술 스택

### Backend

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) ![Uvicorn](https://img.shields.io/badge/Uvicorn-4053D6?style=for-the-badge&logo=uvicorn&logoColor=white) ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)

### AI & Speech

![Anthropic Claude](https://img.shields.io/badge/Anthropic%20Claude-191919?style=for-the-badge&logo=anthropic&logoColor=white) ![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white) ![ElevenLabs](https://img.shields.io/badge/ElevenLabs-1A1A1A?style=for-the-badge&logo=elevenlabs&logoColor=white)

### Database

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

### Data Processing & Tools

![PyMuPDF](https://img.shields.io/badge/PyMuPDF-FF6F00?style=for-the-badge&logo=pdf&logoColor=white) ![Tenacity](https://img.shields.io/badge/Tenacity-5A5A5A?style=for-the-badge&logo=python&logoColor=white)

### Collaboration

![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white) ![Notion](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white)

---

## 주요 기능

### 1. 공감형 AI 캐릭터 챗봇

- **4인 4색 캐릭터 페르소나**: 아동이 정서적 유대를 맺을 수 있는 고유한 성격과 목소리를 지닌 4가지 캐릭터 프로필을 지원합니다.
- **실시간 마음 온도 시스템**: 대화 진행 상황에 따라 캐릭터의 감정을 나타내는 마음 온도(0 ~ 100)가 유기적으로 변화하며, 대화 분위기에 맞게 음성 톤과 답변 깊이가 조절됩니다.
- **연령별 어조 최적화**: 대화 상대방(아동)의 나이에 맞추어 자연스럽게 존댓말과 반말을 전환하며 상호작용합니다.
- **TTS 음성 합성**: ElevenLabs와의 연동을 통해 각 캐릭터의 개성을 담은 음성을 제공합니다.

### 2. UDL 기반 문장 분해 학습 생성기

- **보편적 학습 설계(UDL) 적용**: 글을 이해하는 데 어려움을 겪는 아동이 문장의 구조(주어, 목적어, 서술어, 수식어 등)를 파악할 수 있도록 퀴즈를 자동 생성합니다.
- **연령별 레벨링 (Lv 2 ~ Lv 5)**: 7세 단문부터 13세 인과 접속 복합문까지 아동 인지 연령에 맞춰진 규칙을 적용하여 문장 난이도를 제어합니다.
- **RAG(Retrieval-Augmented Generation) 연계**: 실제 교육 교재 및 동화책 데이터베이스로부터 문맥을 참조하여 예문을 추출합니다.
- **슬롯 분석**: 조건절이 포함된 문장의 경우, 규칙에 따라 '경로 A(조건절 분할)' 혹은 '경로 B(조건절 단일)'를 판별하여 슬롯을 추출합니다.

### 3. 초등 맞춤형 단어장

- **어휘 직관화**: 단어와 품사, 사전적 정의를 입력받아 아동의 일상 어휘 범위 내에서 직관적으로 이해할 수 있는 맞춤형 예문과 어휘 설명을 생성합니다.

### 4. 멀티모달 데이터 가공 및 파이프라인

- **Multimodal PDF Extractor**: 교재 PDF를 고해상도 이미지로 변환한 후 비전 LLM을 통해 도표, 깨진 글자 등을 제외하고 깨끗한 교육용 문장만 자동 정제 및 추출합니다.
- **Database Ingestion**: 정제된 텍스트 데이터를 책(Book)의 레벨 단위로 분류하여 PostgreSQL 데이터베이스에 적재합니다.
