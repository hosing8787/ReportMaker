# Deep Agents - 범용 에이전트 하네스 기획서

- 작성 배경
  - Deep Agents 프로젝트는 범용 Agent 하네스를 제공하여 계획 수립, 파일 시스템 조작, 쉘 명령 실행, 서브에이전트 위임 등의 기능을 포함합니다.
  - 오픈소스 Python monorepo 형태로 SDK, CLI, 평가툴(evals), ACP 지원, 파트너 샌드박스 통합 등 다양한 컴포넌트로 구성되어 있습니다.
  - LangChain 생태계 내에서 Model Agent 개발과 운영을 위한 표준화된 인터페이스와 프로토콜(AGENTS.md, MCP, A2A, Agent Protocol)을 지원합니다.
- 목적
  - 개발 편의성을 위해 구성된 완성형 Agent 하네스를 제공하여 빠르게 커스터마이징 가능한 기반을 마련한다.
  - CLI 및 SDK 형태로 에이전트를 사용할 수 있도록 문서화하여 내·외부 활용성을 극대화한다.
  - 오픈 표준과 다양한 모델/샌드박스 지원으로 유연한 AI Agent 생태계 구축을 목표로 한다.
- 비고
  - 기획서는 사내 공유 목적의 제출용 초안으로 작성되었으며, 외부 공개 오픈소스 내용을 바탕으로 하였습니다.
  - 불명확한 내용은 '확인 필요'로 표기하여 추후 검토를 용이하게 합니다.
  - 분류 항목 및 도구 매트릭스에 실제 적용되는 항목만 체크하여 명확한 상태 구분을 제공합니다.
  - 개요는 핵심 정보를 간결한 문장으로 전달하며, 문서 내외부 링크는 가능하면 명확하게 기재하고 불분명 시 '확인 필요'로 표기합니다.

## 문서 목차

1. 개요 (Overview)
2. Agent 유형 분류 (Classification)
3. 업무 Flow 변화 & 구현 방안 (Work Process)
4. 운영 Tool 리스트 (Tool List)
5. Agent 동작 필수 파라미터 (Parameters)
6. 기타 참고사항 및 제약조건

## 1. 개요 (Overview)

| 항목 | 내용 |
|---|---|
| Agent 명 | Deep Agents |
| Agent 설명 | 계획 수립, 파일 시스템 및 쉘 명령 관리, 서브에이전트 위임 기능을 갖춘 범용 AI Agent 하네스 |
| Agent 개발목적 | 범용적이고 확장 가능한 AI 에이전트를 쉽게 생성 및 운영할 수 있는 기반 제공 |
| 주요 업무 범위 | - 계획 수립 및 작업 분할<br>- 파일 읽기/쓰기/수정/목록화<br>- 쉘 명령 실행 및 제한된 명령어 집합 허용<br>- 서브에이전트 관리 및 위임<br>- 컨텍스트 자동 요약 및 관리 |
| 개발 인원 산정 | 확인 필요 |
| Agent E2E | 로컬 개발 환경부터 CLI/SDK 인터페이스, 서브에이전트 호출, 파일 및 쉘 도구 통합, 최종 응답 생성까지 포함 |
| 개발 방식 | Python monorepo 기반 모듈화 개발, GitHub Actions CI/CD 파이프라인 통합 |
| Main Workflow 링크 | 확인 필요 |
| 산출물/참조 링크 | - AGENTS.md (프로젝트 개발 가이드)<br>- README.md (프로젝트 개요)<br>- 공식 문서 링크: https://docs.langchain.com/oss/python/deepagents/overview#deep-agents-overview (추정) |

## 2. Agent 유형 분류 (Classification)

| 구분 | 선택 항목 |
|---|---|
| Agent 주요 기능 | [x] 계획 수립(Planning) - 작업 분할 및 TODO 관리<br>[x] 파일 시스템 조작(Filesystem) - 파일 읽기, 쓰기, 수정, 검색 등<br>[x] 쉘 명령 실행(Shell Execution) - 안전한 샌드박스 내 쉘 명령 수행<br>[x] 서브에이전트 위임(Sub-agent Delegation) - 작업 위임 및 독립 컨텍스트 처리<br>[x] 컨텍스트 관리(Context Management) - 자동 요약 및 긴 대화 처리 |
| 개발 언어 및 프레임워크 | [x] Python - 메인 언어, monorepo 구조<br>[ ] TypeScript/JS - JS/TS 버전(deepagents.js) 별도 존재<br>[x] LangChain SDK - LangChain 연동 및 프레임워크 활용 |
| 배포 및 환경 | [x] 로컬 개발 - Editable install 및 유닛 테스트 환경 제공<br>[x] GitHub Actions CI/CD - 빌드, 린트, 테스트, 릴리즈 자동화<br>[x] Self-hosted Deploy - LangSmith 기반 자가 호스팅 배포 지원<br>[ ] 클라우드 배포 - 확인 필요 |
| 통합 및 표준화 | [x] AGENTS.md 문서 표준 - Agent 명세 포맷 준수<br>[x] MCP, A2A, Agent Protocol - 다양한 에이전트 프로토콜 지원<br>[x] Skill 지원 - Agent 기능재사용 및 확장성 확보 |

## 3. 업무 Flow 변화 & 구현 방안 (Work Process)

| 구분 | 내용 |
|---|---|
| Agent 초기화 및 구성 | SDK 및 CLI 설치 후, 기본 agent 인스턴스 생성<br>기본 도구(계획, 파일, 쉘, 서브에이전트)를 포함하는 하네스 구성 |
| Agent 명령 및 계획 수행 | 사용자 메시지 수신<br>내부적으로 작업 분할 및 TODO 생성<br>필요시 서브에이전트를 통한 작업 위임 |
| 파일 시스템 작업 | 로컬 또는 샌드박스 내 파일 읽기, 쓰기, 편집<br>중요 데이터는 파일로 저장 및 관리 |
| 쉘 명령 실행 | 허용된 쉘 명령 목록 내에서 명령 실행<br>결과를 Agent 컨텍스트와 연동하여 다음 작업에 반영 |
| 컨텍스트 관리 및 요약 | 대화가 길어지면 자동 요약 수행하여 메모리 최적화<br>기존 컨텍스트 저장 및 재사용 |
| 응답 생성 및 출력 | 모델 응답을 텍스트 형태로 클라이언트에 반환<br>로그 및 메모리에 회수 가능한 산출물 저장 |

## 4. 운영 Tool 리스트 (Tool List)

| 운영 분류 | 관리 시스템 | 사내 시스템 | 고객사 시스템 | Message | KM | Log | Cloud | 서버(OS) | DB | MW | Kubernetes | Network | AT DC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SDK/CLI |  | O deepagents (Agent 하네스 기본 SDK 및 CLI 커맨드 제공) |  |  |  |  |  |  |  |  |  |  |  |
| Agent 지원 라이브러리 |  | O deepagents-acp (Agent Context Protocol 지원) |  |  |  |  |  |  |  |  |  |  |  |
| 평가 도구 |  | O evals (에이전트 성능 평가 및 Harbor 통합) |  |  |  |  |  |  |  |  |  |  |  |
| 파트너 샌드박스 |  |  |  |  |  |  | O daytona (Sandbox 실행 환경 통합)<br>O modal (Sandbox 실행 환경 통합) | O quickjs (Sandbox JS 엔진 통합)<br>O runloop (Sandbox 실행 환경 통합) |  |  |  |  |  |
| 추가 도구 |  | O make, ruff, ty, uv (빌드, 린트, 정적 타입 검사, 패키지 관리) |  |  |  |  |  |  |  |  |  |  |  |

## 5. Agent 동작 필수 파라미터 (Parameters)

| 시스템 | 파라미터 | 값 / 설명 |
|---|---|---|
| GitHub Action Inputs | model | 사용할 LLM 모델; 예: claude-*, gpt-*, gemini-* (미정) |
| GitHub Action Inputs | anthropic_api_key | Anthropic API Key (필요 시) |
| GitHub Action Inputs | openai_api_key | OpenAI API Key (필요 시) |
| GitHub Action Inputs | google_api_key | Google API Key (필요 시) |
| GitHub Action Inputs | github_token | GitHub API 접근 토큰; 기본 ${{ github.token }} |
| GitHub Action Inputs | working_directory | 에이전트 작업 디렉터리; 기본 '.' |
| GitHub Action Inputs | cli_version | deepagents-cli 버전; 공란 시 최신버전 |
| GitHub Action Inputs | skills_repo | 기능 스킬 저장소 GitHub 주소 |
| GitHub Action Inputs | enable_memory | 에이전트 메모리 지속 여부; 기본 true |
| GitHub Action Inputs | memory_scope | 메모리 캐시 범위; pr, branch, repo 중 하나; 기본 repo |
| GitHub Action Inputs | agent_name | 에이전트 네임스페이스; 기본 agent |
| GitHub Action Inputs | shell_allow_list | 허용된 쉘 명령 리스트 (comma-separated); 기본 recommended,git,gh |
| GitHub Action Inputs | timeout | 에이전트 최대 런타임 (분 단위); 기본 30 |

## 6. 기타 참고사항 및 제약조건

- 보안: 쉘 명령어 실행 시 권한 관리 및 허용 리스트를 엄격히 유지해야 함
- 운영: 메모리 지속 기능 활성화 시 캐시 관리 정책 필요
- API 키와 같은 민감정보는 GitHub Actions 시크릿으로 안전하게 관리
- 오픈소스 컴포넌트 기반으로 배포 시 라이선스(MIT) 및 의존성 관리 필수
- 현재 deepagents deploy 기능은 베타 상태로 API와 구성 형식이 변경 가능성 있음
- 개발 인원, 상세 개발 일정, 메인 워크플로우 링크는 별도 확인 필요

## Assumptions

- 개발 인원 수와 배포 운영 환경은 추후 내부 협의를 통해 확정할 예정
- 외부 클라우드 배포 방식 및 구체적 인프라 구성은 미정
- 비즈니스 목적에 따라 커스터마이징 및 스킬 추가가 가능하므로 확장성을 고려한 설계 우선
- Agent E2E 흐름은 로컬에서 CI/CD를 통해 배포까지의 단계를 포함하는 것으로 추정
