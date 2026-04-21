# Deep Agents Agent 기획서 초안

- 작성 배경
  - Deep Agents는 범용 AI 에이전트 하네스를 제공하는 오픈소스 프로젝트입니다.
  - 계획 수립, 파일 시스템 조작, 쉘 명령 실행, 서브에이전트 위임 등 다양한 기능을 포함합니다.
  - Python 모노레포 구조로 여러 패키지(lib/deepagents, cli, acp 등)로 구성되어 있습니다.
  - CLI 및 SDK 형태로 활용 가능하며 문서화가 잘 되어 있어 배터리 탑재형 에이전트를 손쉽게 사용할 수 있습니다.
- 목적
  - 범용 에이전트 플랫폼 제공으로 개발 생산성 향상.
  - 다양한 업무(Task Planning, 파일/쉘 조작, 서브에이전트 관리) 자동화 지원.
  - 기존 코드, 도구 연결을 일원화하여 일관된 에이전트 개발 환경 제공.
  - 오픈소스 기반으로 커스터마이징 및 확장 용이성 보장.
- 비고
  - 공식 문서와 코드를 기준으로 작성, 미확인 내용은 확인 필요 표기.
  - 스크린샷 양식에 맞추어 고정 항목 우선 작성.
  - 분류표는 범주별 옵션으로 줄 단위 체크박스 형태.
  - 링크는 코드에서 확인된 부분만 기재하고, 불분명한 경우 '확인 필요'로 기재.
  - parameters는 주요 설정과 운영 파라미터 위주로 정리.

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
| Agent 설명 | 범용 AI 에이전트 하네스, 계획 수립부터 파일 및 쉘 조작, 서브에이전트 위임까지 지원하는 Python 기반 오픈소스 SDK 및 CLI 툴 |
| Agent 개발목적 | 자동화된 범용 에이전트 플랫폼 제공으로 업무 효율성 및 확장성 극대화 |
| 주요 업무 범위 | 작업 계획 작성, 파일시스템 입출력, 셸 명령 실행, 서브에이전트 관리, 컨텍스트 자동 요약 및 관리 |
| 개발 인원 산정 | 확인 필요 (오픈소스 커뮤니티 및 내부 협업) |
| Agent E2E | SDK로 에이전트 생성 → 메시지 기반 호출 → 내부 계획 및 도구 연동 → 파일/쉘 작업 및 서브에이전트 위임 → 결과 반환 |
| 개발 방식 | 모노레포 구조로 독립 패키지 개발 및 버전 관리 (libs/deepagents, cli, acp 등) |
| Main Workflow 링크 | https://github.com/langchain-ai/deepagents/blob/main/AGENTS.md (개발가이드) |
| 산출물/참조 링크 | https://docs.langchain.com/oss/python/deepagents/overview  /  https://github.com/langchain-ai/deepagents |

## 2. Agent 유형 분류 (Classification)

| 구분 | 유형 |
|---|---|
| 기능 분류 | [x] 계획 수립 (Planning) - 작업 분해 및 진행 상황 추적 |
|  | [x] 파일 시스템 조작 (Filesystem) - 파일 읽기, 쓰기, 편집 등 |
|  | [x] 쉘 명령 실행 (Shell Access) - 명령어 실행, 샌드박스 포함 |
|  | [x] 서브에이전트 위임 (Sub-agents) - 격리된 컨텍스트 하위 에이전트 관리 |
|  | [x] 스마트 기본값 (Smart Defaults) - 사용자 프롬프트, 툴 사용법 제공 |
|  | [x] 컨텍스트 관리 (Context Management) - 대화 요약 자동화, 대용량 출력 파일 관리 |
|  | [ ] 기타 (Other) - 확인 필요 |
| 개발 형태 | [x] SDK 제공 - Python API |
|  | [x] CLI 도구 제공 - 터미널 기반 |
|  | [x] 오픈소스 라이선스 - MIT 라이선스 |
|  | [x] 모델 독립적 (Model-agnostic) - 여러 LLM 지원 |
|  | [x] 모노레포 관리 - 독립 패키지 버전 관리 |
| 운영 환경 | [x] 로컬 개발 - editable install via uv |
|  | [x] CI/CD 연동 - GitHub Actions 워크플로우 기반 |
|  | [x] 샌드박스 통합 - Modal, Daytona, Runloop, QuickJS 지원 |
|  | [x] 배포 지원 - LangSmith Deploy, 자체호스팅 가능 |
|  | [x] 문서화 및 예제 - 공식 문서와 다수 예제 샘플 포함 |

## 3. 업무 Flow 변화 & 구현 방안 (Work Process)

| 구분 | 내용 |
|---|---|
| 1. 에이전트 생성 및 초기화 | create_deep_agent() API를 호출하여 에이전트 인스턴스 생성<br>기본 도구(계획, 파일, 쉘, 서브에이전트) 등록<br>사용자 프롬프트 및 스마트 기본값 설정 |
| 2. 작업 지시 및 입력 수신 | 사용자 또는 클라이언트에서 메시지 입력 수신<br>invoke() 메서드로 메시지 전달 |
| 3. 내부 계획 및 작업 분해 | write_todos를 통한 할일 분해 및 단계별 계획 생성<br>진행 상황 및 문제점 추적 |
| 4. 도구별 작업 실행 | 파일시스템 조작: read_file, write_file, edit_file 실행<br>쉘 명령어 실행: execute() 사용, 샌드박스 환경 적용<br>필요시 서브에이전트 위임: task()를 통해 별도 컨텍스트 작업 분배 |
| 5. 컨텍스트 및 상태 관리 | 대화 및 작업 컨텍스트 자동 요약 처리<br>대용량 출력은 파일로 저장하여 관리 |
| 6. 결과 수집 및 응답 반환 | 실행 결과를 수집하여 응답 생성<br>사용자에게 처리 결과 전달 |
| 7. 개발 및 배포 프로세스 | 로컬에서 Makefile 및 uv로 빌드, 테스트, 린트 수행<br>GitHub Actions 기반의 CI/CD 파이프라인 활용<br>LangSmith, 오픈소스 샌드박스 통합 및 LangSmith Deploy로 배포 가능 |

## 4. 운영 Tool 리스트 (Tool List)

| 구분 | 선택 항목 |
|---|---|
| SDK/CLI | [x] deepagents SDK - 에이전트 생성 및 주요 로직 활용<br>[x] deepagents CLI (deepagents-cli) - 터미널 기반 에이전트 인터페이스 |
| 프로토콜 | [x] Agent Context Protocol (acp) - 에이전트 컨텍스트 관리 및 통합 |
| 평가 및 테스트 | [x] evals - 에이전트 평가 및 품질 검증 |
| 파트너 샌드박스 | [x] Daytona - 샌드박스 환경 제공<br>[x] Modal - 샌드박스 환경 제공<br>[x] QuickJS - 경량 샌드박스 JavaScript 환경<br>[x] Runloop - 샌드박스 및 비동기 작업 환경 |
| 배포 | [x] LangSmith Deployment - 에이전트 서비스로 배포 및 운영 |
| 기타 | [x] uv 패키지 관리 - 의존성 관리 및 패키지 빌드 |

## 5. Agent 동작 필수 파라미터 (Parameters)

| 시스템 | 파라미터 | 값 / 설명 |
|---|---|---|
| GitHub Action Inputs / deepagents deploy | prompt | 작업 지시용 프롬프트 (필수) |
| GitHub Action Inputs / deepagents deploy | model | 사용할 AI 모델 (예: claude-*, gpt-*, gemini-*) - 미정 자동 감지 기능 |
| GitHub Action Inputs / deepagents deploy | anthropic_api_key | Anthropic API 키 (선택) |
| GitHub Action Inputs / deepagents deploy | openai_api_key | OpenAI API 키 (선택) |
| GitHub Action Inputs / deepagents deploy | google_api_key | Google API 키 (선택) |
| GitHub Action Inputs / deepagents deploy | github_token | GitHub API 접근 토큰 (기본: ${{ github.token }}) |
| GitHub Action Inputs / deepagents deploy | working_directory | 에이전트 작업 디렉토리 경로 (기본: ".") |
| GitHub Action Inputs / deepagents deploy | cli_version | deepagents-cli 버전 (빈 값 = 최신) |
| GitHub Action Inputs / deepagents deploy | skills_repo | 스킬 클론용 GitHub 레포지토리 (owner/repo@ref 형식) |
| GitHub Action Inputs / deepagents deploy | enable_memory | 워크플로우 간 메모리 지속 여부 (기본: true) |
| GitHub Action Inputs / deepagents deploy | memory_scope | 캐시 범위 (pr, branch, repo 중 선택, 기본: repo) |
| GitHub Action Inputs / deepagents deploy | agent_name | 에이전트 네임스페이스 (기본: agent) |
| GitHub Action Inputs / deepagents deploy | shell_allow_list | 쉘 명령 허용 리스트 (default: recommended,git,gh) |
| GitHub Action Inputs / deepagents deploy | timeout | 최대 실행 시간(분) (기본: 30) |

## 6. 기타 참고사항 및 제약조건

- 에이전트가 파일시스템 및 셸 조작 권한을 갖기에 운영 환경에서 권한 정책과 보안 구성이 필요함.
- 샌드박스 환경과 외부 API 키 설정 시 보안 키 관리 주의.
- 메모리 지속 기능(enabled_memory) 활성화 시 캐시 정책에 따른 데이터 일관성 고려.
- 베타 상태(Deep Agents Deploy)로 API 및 구성 포맷 변경 가능성 있음.
- 오픈소스 기반으로 운영 및 배포 시 자체 커스터마이징 가능하나, 충분한 테스트 권고.
- 로컬 개발 시 Makefile, uv 패키지 관리 활용하여 일관성 있는 빌드 및 린트 환경 유지 필요.

## Assumptions

- 개발자 및 운영자는 Python 환경 및 GitHub Actions 기반 CI/CD 환경에 익숙함.
- 실사용 시 LLM API 키(Anthropic, OpenAI 등)를 별도 준비하여야 함.
- 샌드박스는 Modal, Daytona 등 오픈소스 파트너 툴을 통해 관리됨.
- 프로덕션 배포 시 LangSmith 또는 유사 플랫폼 이용 가능.
- 예제 및 문서가 주로 영어로 되어 있어 다국어 지원 필요 시 별도 로컬라이징 고려
