# Deep Agents 사내 Agent 기획서 초안

- 작성 배경
  - Deep Agents는 오픈소스 모델-비종속(agent harness) 에이전트 프레임워크로, 계획 수립, 파일 시스템 조작, 쉘 실행, 서브에이전트 위임 등 범용적인 Agent 기능을 제공함.
  - Python Monorepo 구조로 SDK, CLI, ACP, 평가(evals), 파트너 통합(libs/partners) 등의 패키지들로 구성되어 있음.
  - LangChain 에이전트 생태계와 연계하며 MCP, A2A, Agent Protocol 등 오픈 표준을 지원함.
  - CI/CD, 린트, 테스트 자동화, 버전 관리 체계가 잘 갖추어져 있어 안정적 개발 환경 제공.
- 목적
  - 범용 에이전트 하네스로서 빠른 개발 및 커스터마이징 제공.
  - CLI 및 SDK 형태로 Agent를 손쉽게 활용할 수 있도록 전반적인 설계 및 문서화.
  - 에이전트 계획, 파일 입출력, 쉘 명령 실행, 서브 에이전트 위임 등 핵심 기능 통합 제공.
  - 오픈소스 기반으로 다양한 LLM과 샌드박스 시스템 연동 가능하도록 확장성 확보.
- 비고
  - 작성 내용은 오픈소스 Deep Agents 저장소(GitHub)를 기반으로 함.
  - 불확실하거나 명시적이지 않은 내용은 '확인 필요'로 표기함.
  - 스크린샷 양식에 맞추어 배경, 목적, 개요, 분류, 업무 프로세스, 도구, 파라미터, 고려사항, 가정으로 구성.
  - 기술적 상세 코드는 분량과 가독성 고려해 요약 제시.

## 문서 목차

1. 1. 작성 배경
2. 2. 목적
3. 3. 문서 목차
4. 4. Agent 개요
5. 5. 분류 사항
6. 6. 업무 프로세스
7. 7. 도구 및 시스템
8. 8. 주요 파라미터
9. 9. 고려사항 및 비고
10. 10. 가정 및 미결 사항

## 1. 개요 (Overview)

| 항목 | 내용 |
|---|---|
| Agent 명 | Deep Agents |
| Agent 설명 | 모델-비종속 범용 에이전트 하네스로, 계획 수립, 파일 및 쉘 조작, 서브 에이전트 위임 등을 지원하는 Python SDK 및 CLI 툴킷 |
| Agent 개발목적 | 즉시 사용 가능한 에이전트 환경 제공 및 다중 LLM 연동과 오픈 표준 지원을 통한 유연한 확장성 확보 |
| 주요 업무 범위 | 작업 계획, 파일 시스템 액세스 및 편집, 쉘 명령 실행, 서브 에이전트 관리 및 위임, 메모리 관리, 대화 및 컨텍스트 요약 |
| 개발 인원 산정 | 확인 필요 |
| Agent E2E | 로컬 개발환경 구축 - 계획 및 작업 지시 - 도구 활용 (파일, 쉘, 서브에이전트) - 결과 반환 - 메모리 및 컨텍스트 관리 |
| 개발 방식 | Python Monorepo 기반 모듈화, CI/CD 기반 린트 및 테스트, 릴리즈 자동화 |
| Main Workflow 링크 | 확인 필요 (GitHub Actions 워크플로우 참조) |
| 산출물/참조 링크 | https://github.com/langchain-ai/deepagents, https://docs.langchain.com/oss/python/deepagents/overview |

## 2. Agent 유형 분류 (Classification)

| 구분 | 선택 항목 |
|---|---|
| 개발 범위 | [x] SDK - Core SDK 및 API 제공<br>[x] CLI - 대화형 커맨드라인 인터페이스 제공<br>[x] ACP - Agent Context Protocol 지원<br>[x] Evals - 평가 및 성능 테스트 포함<br>[x] Partners(샌드박스) - Daytona, Modal, QuickJS, Runloop 등 샌드박스 연동 |
| 지원 모델 | [x] OpenAI GPT - API 키 지원 및 기본 LLM<br>[x] Anthropic Claude - CLI 입력값 및 환경변수 지원<br>[x] Google PaLM - API 연동 확인 필요<br>[x] 기타 LLM - Bedrock, Azure, Fireworks 등 다양한 제공자 호환 |
| 운영 환경 | [x] 로컬 개발 - Makefile, uv 패키지 매니저 사용<br>[x] CI/CD - GitHub Actions 워크플로우 자동화<br>[x] 배포(심플) - Deep Agents Deploy 베타 제공<br>[ ] 클라우드 연동 - 별도 구성 필요 |

## 3. 업무 Flow 변화 & 구현 방안 (Work Process)

### 개발 및 빌드 준비
- uv, make, ruff, ty 등 개발 도구 설치 및 환경 구성
- 편집 가능 설치(Editable install) 및 의존성 관리

### 에이전트 초기화 및 실행
- create_deep_agent() 호출로 에이전트 생성
- 프롬프트 전달해 작업 명령 수행
- 내장 플래닝, 파일 I/O, 쉘 명령, 서브 에이전트 호출

### 환경 설정 및 보안 관리
- 쉘 명령 허용 리스트 설정
- 환경변수(API 키 등) 및 작업 디렉토리 지정
- 타임아웃, 메모리 지속성 옵션 적용

### 서브 에이전트 및 컨텍스트 관리
- 서브 에이전트 task 명령을 통한 작업 위임
- 대화 컨텍스트 자동 요약 및 대용량 출력 파일 저장
- 메모리 캐시를 통해 상태 지속 및 공유

### 평가 및 린트 자동화
- pytest 기반 유닛 테스트 및 벤치마킹
- ruff 린터, 포맷터 자동화
- release-please 기반 패키지 자동 배포

## 4. 운영 Tool 리스트 (Tool List)

| 분류 | 시스템 | 사용 여부 | 사용 목적 |
|---|---|---|---|
| 개발 도구 | uv | O | 패키지 설치 및 의존성 관리 |
| 개발 도구 | make | O | 빌드, 린트, 테스트 작업 실행 |
| 개발 도구 | ruff | O | 코드 린트 및 포맷팅 |
| 개발 도구 | pytest | O | 단위 테스트 및 벤치마크 |
| 에이전트 실행 | Deep Agents SDK | O | Agent 객체 생성 및 실행 |
| 에이전트 실행 | Deep Agents CLI | O | 터미널 상호작용 및 명령 실행 |
| 샌드박스 | Daytona | O | 안전한 코드 및 명령 실행 환경 제공 |
| 샌드박스 | Modal | O | 서버리스 함수 및 에이전트 배포 지원 |
| 샌드박스 | QuickJS | O | JavaScript 코드 실행 환경 |
| 샌드박스 | Runloop | O | 반복 작업 자동화 및 이벤트 처리 |

## 5. Agent 동작 필수 파라미터 (Parameters)

| 시스템 | 파라미터 | 값 / 설명 |
|---|---|---|
| CLI Action Inputs | prompt | 에이전트에 전달할 텍스트 프롬프트 (필수) |
| CLI Action Inputs | model | 사용할 LLM 모델 (선택, 자동감지 가능) |
| CLI Action Inputs | anthropic_api_key | Anthropic API 키 (선택) |
| CLI Action Inputs | openai_api_key | OpenAI API 키 (선택) |
| CLI Action Inputs | google_api_key | Google API 키 (선택) |
| CLI Action Inputs | github_token | GitHub API 토큰 (기본: `${{ github.token }}`) |
| CLI Action Inputs | working_directory | 작업 디렉토리 (기본: '.') |
| CLI Action Inputs | cli_version | deepagents-cli 버전 (기본 최신) |
| CLI Action Inputs | skills_repo | 스킬 저장소 GitHub 경로 (선택) |
| CLI Action Inputs | enable_memory | 메모리 캐시 활성화 여부 (기본 true) |
| CLI Action Inputs | memory_scope | 메모리 캐시 범위 (pr, branch, repo; 기본 repo) |
| CLI Action Inputs | agent_name | 에이전트 이름(메모리 네임스페이스에 사용, 기본 agent) |
| CLI Action Inputs | shell_allow_list | 허용 쉘 명령 리스트 (기본: recommended,git,gh) |
| CLI Action Inputs | timeout | 최대 실행 시간(분, 기본 30) |

## 6. 기타 참고사항 및 제약조건

- GitHub API 토큰 사용 시 권한 범위 및 보안 유의
- 실행 가능한 쉘 명령 허용 리스트 관리로 보안 강화
- 메모리 캐시는 Actions/cache 기반으로 PR, 브랜치, 저장소 범위 선택 가능
- Deep Agents Deploy 기능은 베타 상태로 API 및 구성 변경 가능성 있음
- LLM 모델별 API 키와 연결 정보는 환경변수 또는 입력값으로 관리
- Opaque 라이브러리 간 중복 규칙 무시 가능, 단내부 정책 준수

## Assumptions

- 개발 인원은 별도 산정 필요
- Main Workflow 및 산출물 링크는 내부 GitHub 참조 필요
- MS Windows 기반 경로 예시가 있으나 크로스플랫폼 지원 가능
- agent_name, shell_allow_list 등 일부 파라미터는 기본값 사용 전제
- Deep Agents CLI 사용 시 최신 버전 기준 작성
- 평가 및 코딩 에이전트는 예시 수준, 직접 테스트 환경 참고
