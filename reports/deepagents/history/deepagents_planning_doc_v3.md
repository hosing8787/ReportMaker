# Deep Agents 기획서

- 작성 배경
  - Open source Deep Agents 프로젝트는 범용 에이전트 하네스를 제공하여 계획 수립, 파일 시스템 조작, 쉘 실행, 서브에이전트 위임 등 에이전트 운영에 필요한 기능을 통합
  - Python 기반 Monorepo 구조로 SDK, CLI, ACP, 평가 도구, 파트너 통합 등 여러 컴포넌트 포함
  - 에이전트의 신속한 사용 및 커스터마이징 지원을 목적으로 하며, 다양한 LLM 제공자와 모듈식 샌드박스 환경 지원
- 목적
  - 범용 에이전트 하네스 구현 및 제공
  - CLI 및 SDK 형태로 손쉬운 접근 및 활용 지원
  - 모델 독립적 설계로 다양한 LLM과 샌드박스 통합 가능하게 설계
  - 에이전트 컨텍스트 관리 및 자동 요약 기능 제공
  - 서브 에이전트 및 작업 위임 기능 지원
- 비고
  - 각 항목은 코드 내 문서와 구성파일에서 확인된 내용을 바탕으로 작성
  - 미확인 내용은 '확인 필요'로 명시하여 추측 방지
  - 스크린샷 양식에 맞추어 JSON 스키마 형식에 최적화된 형식으로 기술

## 문서 목차

1. 1. 작성 배경 및 목적
2. 2. 개요
3. 3. 분류표
4. 4. 업무 프로세스
5. 5. Tool Matrix
6. 6. 파라미터
7. 7. 고려사항 및 비고

## 1. 개요 (Overview)

| 항목 | 내용 |
|---|---|
| Agent 명 | Deep Agents |
| Agent 설명 | 범용 에이전트 하네스로, 계획 수립, 파일 읽기/쓰기, 쉘 명령 실행, 서브 에이전트 위임 등을 지원하는 에이전트 개발 및 운영 프레임워크 |
| Agent 개발목적 | 신속하게 사용 가능한 오픈소스 에이전트 플랫폼 제공 및 다양한 LLM과 샌드박스 환경 통합 지원 |
| 주요 업무 범위 | 작업계획, 파일 시스템 조작, 커맨드 실행, 서브 에이전트 관리, 컨텍스트 자동 요약 및 관리 |
| 개발 인원 산정 | 확인 필요 |
| Agent E2E | 로컬 개발환경(uv, make 기반) -> SDK/CLI 개발 -> 에이전트 실행 및 평가 -> (옵션) LangSmith Deploy를 통한 배포 및 운영 |
| 개발 방식 | 모듈화된 Monorepo 구조로 Python 패키지별 독립 버전 관리, CI/CD 및 린트, 테스트 자동화 |
| Main Workflow 링크 | 확인 필요 |
| 산출물/참조 링크 | https://github.com/langchain-ai/deepagents , https://docs.langchain.com/oss/python/deepagents/overview#deep-agents-overview |

## 2. Agent 유형 분류 (Classification)

| 구분 | 선택 항목 |
|---|---|
| 기능 분류 | [x] 계획 수립 (Planning) - 작업 분해 및 진행 추적<br>[x] 파일 시스템 조작 - read_file, write_file, edit_file, ls, glob, grep 등 지원<br>[x] 쉘 실행 - execute 명령으로 제한적 샌드박스 내 커맨드 실행<br>[x] 서브 에이전트 위임 - isolated context 윈도우로 작업 위임<br>[x] 컨텍스트 자동 요약 - 대화가 길어지면 자동 요약 저장<br>[x] 기본 커스터마이징 지원 - 스마트 프롬프트, 툴 조합 커스터마이징 가능<br>[x] 메모리 지속성 - actions/cache 기반 메모리 지속 기능<br>[x] 멀티 제공자 모델 지원 - OpenAI, Anthropic, Google, 기타 다수 모델 지원 |

## 3. 업무 Flow 변화 & 구현 방안 (Work Process)

### 에이전트 초기화 및 구성
- 유저가 SDK/CLI를 통해 에이전트 생성 (create_deep_agent 등)
- 모델, 스킬, 메모리 옵션 설정 및 커스터마이징 가능

### 프롬프트 입력 및 계획 수립
- 유저 입력 기반으로 작업 분해 및 todo 리스트 생성
- 각 작업별 실행 전략 내부 생성

### 파일 시스템 접근 및 편집
- 지정된 경로 내 파일 읽기, 쓰기, 편집 수행
- 상황에 따라 필요 정보 저장 또는 참조

### 쉘 명령 실행
- 허용된 쉘 명령 리스트에 따라 안전하게 명령 실행
- 결과를 받아 후속 작업에 반영

### 서브 에이전트 작업 위임
- 신규 환경 분리된 서브 에이전트 생성 및 할당
- 대규모 분산 작업 및 병렬 처리 지원

### 컨텍스트 관리 및 자동 요약
- 대화 이력이 길어지면 자동 요약 생성 및 보관
- 장기 컨텍스트 관리 및 메모리 영속화 지원

### 응답 생성 및 반환
- 에이전트가 최종 응답 텍스트 또는 상태 코드 반환
- 콘솔 출력 또는 API 호출 결과로 활용

## 4. 운영 Tool 리스트 (Tool List)

| 운영 분류 | 관리 시스템 | 사내 시스템 | 고객사 시스템 | Message | KM | Log | Cloud | 서버(OS) | DB | MW | Kubernetes | Network | AT DC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SDK 및 CLI |  | O deepagents SDK / CLI (에이전트 생성, 관리, 명령어 처리) |  |  |  |  |  |  |  |  |  |  |  |
| 패키지 관리 |  | O uv (pip 대체) (의존성 설치 및 관리) |  |  |  |  |  |  |  |  |  |  |  |
| 형상 관리 및 린트 |  | O ruff, ty (타입체크) (코드 품질 보장 및 스타일 관리) |  |  |  |  |  |  |  |  |  |  |  |
| 테스트 및 CI | O pytest, GitHub Actions (단위테스트 및 자동 배포 전 검증) |  |  |  |  |  |  |  |  |  |  |  |  |
| 샌드박스 통합 |  |  |  |  |  |  | O Daytona, Modal, Runloop, QuickJS 등 (코드 실행 및 안정적 환경 제공) |  |  |  |  |  |  |
| 배포 도구 |  | O LangSmith Deploy (에이전트 배포 및 운영 환경 제공) |  |  |  |  |  |  |  |  |  |  |  |
| 모델 제공자 |  | O OpenAI, Anthropic, Google 외 다수 (LLM API 연동 및 대화 생성) |  |  |  |  |  |  |  |  |  |  |  |
| 문서화 | O Markdown, GitHub Wiki (개발 가이드 및 사용법 문서화) |  |  |  |  |  |  |  |  |  |  |  |  |

## 5. Agent 동작 필수 파라미터 (Parameters)

| 시스템 | 파라미터 | 값 / 설명 |
|---|---|---|
| deepagents deploy | model | 사용할 LLM 지정 (ex. gpt-*, claude-*, gemini-* 등) - 확인 필요 |
| deepagents deploy | timeout | 최대 실행 시간 분 단위 (기본 30분) |
| deepagents deploy | enable_memory | 메모리 지속 옵션, true/false (기본 true) |
| deepagents deploy | memory_scope | 메모리 저장 범위 (pr, branch, repo) - 기본 repo |
| GitHub Actions | github_token | GitHub API 접근 토큰 (기본: ${{ github.token }}) |
| 프롬프트 입력 | prompt | 에이전트에 전달할 실행 명령 또는 질의 |
| CLI | cli_version | deepagents-cli 버전 (빈값 시 최신) - 확인 필요 |
| Shell Allow List | shell_allow_list | 허용 쉘 명령 리스트 (기본 recommended,git,gh) |
| API 키 | openai_api_key | OpenAI API 키 - 필요 시 설정 |
| API 키 | anthropic_api_key | Anthropic API 키 - 필요 시 설정 |
| API 키 | google_api_key | Google API 키 - 필요 시 설정 |

## 6. 기타 참고사항 및 제약조건

- 배포 시 API 키 및 토큰 관리에 주의 필요, 보안상 외부 노출 금지
- 직접 쉘 실행 허용 범위 제한(shell_allow_list 기본값 이용 권장)
- 메모리 지속 기능 활성화 시 저장소 캐시 용량 및 만료 정책 고려
- 다양한 LLM 호환성은 있으나, 각각의 모델 별 성능 차이 및 API 제한에 유의
- 자동 요약 및 컨텍스트 관리가 복잡한 시나리오에서 정확도 영향 가능성 존재
- 서브 에이전트 위임은 리소스 소모가 크므로 운영 환경에서 모니터링 필요
- 베타 기능(Deep Agents Deploy) 사용 시 API, 구성 포맷 변경 가능성 있음
- 각 패키지 및 모듈은 독립적 버전 관리 및 릴리즈 프로세스 엄수 필요

## Assumptions

- 개발 인원 수는 공식 문서에 미명기되어 있어 추후 확인 필요
- Main Workflow 및 상세 산출물 링크는 공개된 문서 내 명확 진술 없어 내부 확인 필요
- 운영 환경에 따라 샌드박스 및 배포 옵션 선택 유연성 제공, 구체 정책은 운영 주체별 결정
