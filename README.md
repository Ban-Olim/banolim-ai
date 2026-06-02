# Banolim AI Engine (반올림 AI 엔진)

> 경계선 지능 특성을 가진 아동을 위한 학습 플랫폼 **Banolim**의 FastAPI 기반 AI 엔진 서버입니다.

<br>

## 📚 목차

1. [프로젝트 소개](#-프로젝트-소개)
2. [기술 스택](#️-기술-스택)
3. [주요 기능](#-주요-기능)
4. [AI 서버 역할](#-ai-서버-역할)
5. [서비스 구성](#️-서비스-구성)
6. [CI/CD](#️-cicd)
7. [Team Members](#-team-members)

<br>

## 📌 프로젝트 소개

**Banolim**은 경계선 지능 특성을 가진 아동을 위한 학습 플랫폼입니다.  
문장 이해, 어휘 학습, 감정 표현 및 사회적 상황 이해를 돕기 위해 학습 기능과 게임적 요소를 결합했습니다.

본 레포지토리는 Banolim 서비스의 **FastAPI 기반 AI 엔진 서버**입니다.  
멀티모달 비전 기술을 통한 교육 데이터 가공 파이프라인부터 LLM(GPT, Claude)과 TTS(ElevenLabs)를 융합하여 아동 인지 발달 단계에 맞춘 교육 콘텐츠를 실시간으로 생성합니다.

<br>

## 🛠️ 기술 스택

### Backend

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-4053D6?style=for-the-badge&logo=uvicorn&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)

### AI & Speech

![Anthropic Claude](https://img.shields.io/badge/Anthropic%20Claude-191919?style=for-the-badge&logo=anthropic&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![ElevenLabs](https://img.shields.io/badge/ElevenLabs-1A1A1A?style=for-the-badge&logo=elevenlabs&logoColor=white)

### Database

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

### Data Processing & Tools

![PyMuPDF](https://img.shields.io/badge/PyMuPDF-FF6F00?style=for-the-badge&logo=pdf&logoColor=white)
![Tenacity](https://img.shields.io/badge/Tenacity-5A5A5A?style=for-the-badge&logo=python&logoColor=white)

### Collaboration

![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![Notion](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white)

<br>

## ✨ 주요 기능

| 기능                  | 설명                                                                                                                   |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **문장분해**          | UDL(보편적 학습 설계) 기반 규칙 및 나이별 레벨링에 맞춰 문장을 분해하고 슬롯 퀴즈를 생성하는 기능                      |
| **눈치코치**          | 4인 4색 캐릭터 페르소나 및 실시간 마음 온도(0~100) 조절 로직을 통한 AI 캐릭터 챗봇 대화 기능                           |
| **단어장 예문 생성**  | 표제어 자동 검증 메커니즘을 포함하여 초등학생의 일상 어휘 범위에 적합한 단어 설명 및 예문을 생성하는 기능              |
| **데이터 파이프라인** | 교재 PDF를 고해상도 이미지로 변환한 후 비전 LLM(`gpt-4o-mini`)을 거쳐 교육용 문장만 PostgreSQL DB에 가공 적재하는 기능 |

<br>

## 🧩 AI 서버 역할

Banolim FastAPI 서버는 문장분해 퀴즈 생성, 캐릭터 챗봇, 단어장 예시 등 Banolim 서비스에 필수적인 AI 관련 추론 및 TTS 연동 처리를 담당합니다.

- Spring Boot 백엔드 서버의 AI 기능 호출 요청 처리
- UDL 기반 문장 분해 퀴즈 및 힌트/옵션 자동 설계
- 4인 4색 캐릭터 성격 페르소나 적용 및 실시간 마음 온도 계산
- 아동 나이대별 ElevenLabs TTS 목소리 매핑 및 음성 데이터 합성
- 초등 생활 문맥에 최적화된 단어 설명 및 한국어/영어 예문 생성
- 멀티모달 비전 기술 기반 PDF 교재 문장 정제 배치 스크립트 실행
- PostgreSQL DB에 교육 수준별 문장 데이터 자동 관리 및 RAG 검색 소스 활용

<br>

## 🏗️ 서비스 구성

Banolim 서비스는 기능별로 레포지토리를 분리하여 관리합니다.

```text
Ban-Olim Organization
├─ frontend    # 사용자 화면 및 클라이언트 기능
├─ backend     # Spring Boot 기반 백엔드 API 서버
├─ fastapi     # 문장분해, 챗봇 응답 등 AI 기능 처리 서버 [본 레포지토리]
└─ infra       # 배포 및 인프라 관리
```

<br>

### 요청 흐름

```text
[Frontend]
    ↓
[Spring Boot Backend]
    ↓
[FastAPI Server] ─── (RAG 문장 데이터 조회) ─── [PostgreSQL DB]
    ↓
[OpenAI / Anthropic Claude / ElevenLabs] (AI 및 TTS 처리)
```

- 프론트엔드는 백엔드 서버로 API 요청을 보냅니다.
- 백엔드 서버는 문장분해, 눈치코치(챗봇), 나만의 단어장 예문 생성이 필요한 경우 FastAPI AI 엔진으로 비동기 호출을 전달합니다.
- FastAPI 서버는 PostgreSQL 데이터베이스에서 아동 나이에 부합하는 수준별 문장을 랜덤 추출하여 RAG 컨텍스트로 활용합니다.
- 추출된 문장을 활용하여 OpenAI GPT, Anthropic Claude, ElevenLabs API 호출을 거쳐 최종 퀴즈 및 대화 오디오 데이터를 조립하여 백엔드로 반환합니다.

<br>

## ⚙️ CI/CD

본 프로젝트는 GitHub Actions를 이용하여 AI 서버의 빌드 및 배포 과정을 자동화했습니다.

```text
push to main/develop
        ↓
GitHub Actions
        ↓
Docker Image Build & Push
        ↓
Docker Hub
        ↓
Repository Dispatch to Infra (main branch only)
        ↓
Deploy
```

| Branch    | 동작                                                    |
| --------- | ------------------------------------------------------- |
| `develop` | Docker Image Build & Push                               |
| `main`    | Docker Image Build & Push, Infra Repository 배포 트리거 |

<br>

## 👥 Team Members

<table>
  <tr>
    <td align="center" width="220px">
      <a href="https://github.com/gimn70009">
        <img src="https://github.com/gimn70009.png" width="120px;" alt="gimn70009"/>
      </a>
      <br />
      <a href="https://github.com/gimn70009">
        <b>gimn70009</b>
      </a>
      <br />
      <sub>Backend Developer</sub>
      <br />
      <br />
      <span>챗봇 / 문장분해 / 데이터 파이프라인</span>
    </td>
    <td align="center" width="220px">
      <a href="https://github.com/youserlol">
        <img src="https://github.com/youserlol.png" width="120px;" alt="youserlol"/>
      </a>
      <br />
      <a href="https://github.com/youserlol">
        <b>youserlol</b>
      </a>
      <br />
      <sub>Backend Developer</sub>
      <br />
      <br />
      <span>챗봇 / 문장분해 / 데이터 파이프라인</span>
    </td>
    <td align="center" width="220px">
      <a href="https://github.com/7hokerz">
        <img src="https://github.com/7hokerz.png" width="120px;" alt="7hokerz"/>
      </a>
      <br />
      <a href="https://github.com/7hokerz">
        <b>7hokerz</b>
      </a>
      <br />
      <sub>Backend Developer</sub>
      <br />
      <br />
      <span>단어장 / 예문 생성</span>
    </td>
  </tr>
</table>
