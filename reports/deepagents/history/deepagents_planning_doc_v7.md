# Deep Agents 기획서 초안

- 작성 배경
  - Deep Agents 프로젝트는 범용 에이전트 하네스를 목표로 하는 오픈소스 Python 모노레포 프로젝트입니다.
  - 에이전트는 자체 계획 수립, 파일 시스템 조작, 쉘 명령 실행, 서브에이전트 위임 기능을 제공합니다.
  - SDK와 CLI 형태 모두 지원하며, 다양한 샌드박스 통합과 모델 프로바이더 호환성을 갖추고 있습니다.
  - 문서와 개발 가이드, 린트 및 테스트 자동화 환경도 구성되어 있어 협업 및 확장에 용이합니다.
- 목적
  - 범용 AI 에이전트 하네스를 개발하고 이를 SDK 및 CLI 형태로 활용할 수 있도록 함.
  - 자동화된 작업 계획, 파일 조작, 쉘 실행, 서브에이전트 기능을 갖춘 에이전트 플랫폼 제공.
  - 오픈소스 정책으로 모델과 샌드박스 프로바이더 독립적이며 확장 가능한 구조 마련.
  - 내부 및 외부 개발자가 에이전트 개발 및 확장 시 참고할 수 있는 표준 문서 및 코드베이스 제공.
- 비고
  - 사용자 요구에 맞게 오픈소스 코드베이스와 문서 중심으로 작성.
  - 스크린샷 양식에 맞게 정형화된 항목과 체크박스 형식 분류로 표현.
  - 불확실하거나 명확하지 않은 부분은 '확인 필요' 표기.
  - 기술적용 용어는 가능한 한 공식 용어 및 코드상 용어 일치.
  - 문서 목차와 각 항목 간 일관성 유지.
  - 링크는 코드 및 문서 내 URL 우선 활용, 미확인 시 '확인 필요' 처리.

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
| Agent 설명 | 플래닝, 파일 시스템 조작, 쉘 실행, 서브에이전트 위임이 가능한 범용 AI 에이전트 하네스 |
| Agent 개발목적 | 다양한 모델 및 샌드박스 환경에서 즉시 활용 가능한 오픈소스 에이전트 플랫폼 제공 |
| 주요 업무 범위 | 계획 수립, 파일 입출력, 쉘 접근성, 서브에이전트 관리, 자동 컨텍스트 요약 및 관리 |
| 개발 인원 산정 | 확인 필요 (오픈소스 다수 기여 중, 메인 유지관리자 수 미확인) |
| Agent E2E | 로컬에서 SDK/CLI 사용 → 작업 계획 → 파일/쉘/서브에이전트 호출 → 결과 처리 및 컨텍스트 관리 → 대화/작업 반복 |
| 개발 방식 | MIT 라이선스 오픈 소스 모노레포, 유닛테스트·린트·자동 릴리즈 프로세스(Release-please) 적용 |
| Main Workflow 링크 | 확인 필요 (CI/CD 및 릴리즈 관련 링크는 .github 폴더 내 확인 가능) |
| 산출물/참조 링크 | https://github.com/langchain-ai/deepagents (GitHub), https://docs.langchain.com/oss/python/deepagents/overview (공식문서) |

## 2. Agent 유형 분류 (Classification)

| 구분 | 유형 |
|---|---|
| 에이전트 유형 | [x] 범용 에이전트 - 코어 기능 집중 |
|  | [ ] 특화 에이전트 - 확인 필요 |
|  | [x] 서브에이전트 지원 - 서브에이전트 위임 기능 탑재 |
| 주요 기능 | [x] 계획 수립(Planning) - 업무 단계를 자동으로 분할 및 관리 |
|  | [x] 파일 시스템 조작 - 읽기, 쓰기, 편집, 검색 지원 |
|  | [x] 쉘 명령 실행 - 명령어 실행 및 제한된 허용 목록 적용 |
|  | [x] 컨텍스트 관리 - 자동 요약 및 컨텍스트 윈도우 관리 |
|  | [x] 메모리 사용 - 워크플로우 간 메모리 영속화 옵션 있음 |
| 개발 환경 | [x] Python 모노레포 |
|  | [x] 오픈소스 라이선스(MIT) |
|  | [x] 자동 린트 및 포맷 - ruff, makefile 활용 |
|  | [x] 테스트 자동화 - pytest 기반 유닛 테스트 |
|  | [x] CI/CD - .github/workflows 내 정의 |
| 통합 샌드박스/프로바이더 | [x] Daytona - Sandbox provider |
|  | [x] Modal - Sandbox provider |
|  | [x] Runloop - Sandbox provider |
|  | [x] QuickJS - Sandbox provider |
|  | [x] LangSmith - 자체 Sandbox 환경 |
|  | [x] 커스텀 샌드박스 - 사용자 정의 지원 |

## 3. 업무 Flow 변화 & 구현 방안 (Work Process)

| 구분 | 내용 |
|---|---|
| 1. 초기화 및 환경 설정 | Python 환경에서 UV 패키지 매니저로 의존성 설치<br>로컬 개발 모드로 editable install 구성<br>Makefile 명령어로 코드 포매팅 및 린트 수행 |
| 2. 에이전트 생성 및 명령 입력 | `create_deep_agent()` 함수로 기본 에이전트 인스턴스 생성<br>사용자 입력 메시지를 포함한 명령 전달 (예: 연구, 요약 등) |
| 3. 계획 수립 및 업무 분할 | 내장된 계획 수립 도구로 작업을 세분화 및 진행 상태 추적<br>`write_todos` 기능 활용 |
| 4. 파일 시스템 연동 | 파일 읽기, 쓰기, 편집, 탐색 등 파일 시스템 관련 명령 실행<br>컨텍스트 정보를 파일 기반으로 관리 |
| 5. 쉘 명령 실행 | 제한된 셸 명령 실행 가능<br>커맨드 샌드박스 내에서 안전성 확보 |
| 6. 서브에이전트 위임 | 별도 컨텍스트 윈도우에서 서브에이전트 생성 및 작업 위임<br>병렬 처리 및 분산 작업 가능 |
| 7. 컨텍스트 관리 및 자동 요약 | 장기 대화나 출력에 대해 요약 자동 수행<br>컨텍스트 윈도우 크기 최적화 |
| 8. 결과 반환 및 반복 수행 | 최종 결과를 사용자에게 반환<br>필요 시 반복하여 작업 수행 |

## 4. 운영 Tool 리스트 (Tool List)

- 추가가 필요한 경우 자유롭게 추가

| 구분 | 관리 시스템 | 사내 시스템 | 고객사 시스템 | Message | KM | ... |
|---|---|---|---|---|---|---|
| 사내/고객사의 운영 관리 시스템 |  | [x] deepagents-sdk, deepagents-cli - 에이전트 생성, 실행, 커맨드 인터페이스 제공<br>[x] uv, make, ruff, pytest - 패키지 관리, 빌드, 린트, 테스트 자동화<br>[x] deepagents-deploy - 오픈소스 에이전트 배포 자동화 |  |  |  | [x] 모델-agnostic - 다양한 LLM 프로바이더 지원(OpenAI, Anthropic, Google 등)<br>[x] .github/workflows - CI/CD, 린트, 테스트, 릴리즈 자동화 |

| 구분 | Log | Cloud | 서버(OS) | DB | MW | Kubernetes | Network | AI DC |
|---|---|---|---|---|---|---|---|---|
| Tower별 운영 솔루션 |  | [x] Daytona, Modal, Runloop, QuickJS, LangSmith - 코드 실행 및 안전한 쉘 환경 제공 |  |  |  |  |  |  |


## 5. Agent 동작 필수 파라미터 (Parameters)

| 시스템 | 파라미터 | 값 / 설명 |
|---|---|---|
| GitHub Action (deepagents CLI) | prompt | 실행할 명령어 또는 지시문 (필수) |
| GitHub Action (deepagents CLI) | model | 사용할 모델 지정 (미지정 시 자동 감지) |
| GitHub Action (deepagents CLI) | working_directory | 에이전트 작업 디렉토리 (기본값 '.') |
| GitHub Action (deepagents CLI) | cli_version | CLI 버전 (빈 값이면 최신) |
| GitHub Action (deepagents CLI) | enable_memory | 메모리 영속화 활성화 여부 (true/false, 기본 true) |
| GitHub Action (deepagents CLI) | memory_scope | 캐시 범위: pr, branch, repo (기본 repo) |
| GitHub Action (deepagents CLI) | agent_name | 에이전트 식별명 (기본 agent) |
| GitHub Action (deepagents CLI) | shell_allow_list | 허용 셸 명령 목록 (기본 recommended,git,gh) |
| GitHub Action (deepagents CLI) | timeout | 최대 실행 시간(분, 기본 30) |

## 6. 기타 참고사항 및 제약조건

- 오픈소스이므로 보안 취약성 대응 및 권한 관리를 철저히 할 것
- 쉘 명령 실행 시 샌드박스 및 허용목록 활용으로 안전성 확보 필요
- 메모리 영속화 기능은 캐시 키 관리와 적절한 스코프 지정 중요
- CLI 및 SDK 버전 관리 연동 필요 (release-please 자동 릴리즈 로직 참고)
- 커밋 및 PR 작성 시 컨벤셔널 커밋 규칙 준수 권고
- 테스트 자동화와 린트 체크를 CI 파이프라인에 필수 포함
- 문서 및 코드 주석으로 예외 처리 근거 명확히 기록할 것
- 서브에이전트 간 컨텍스트 격리 및 데이터 유출 방지
- 릴리즈 버전 관리는 pyproject.toml과 _version.py 간 일치 필요 (자동 검사 스크립트 존재)
- Model 및 Sandbox Provider 선택은 운영 환경 및 정책에 따라 조정

## Assumptions

- 개발 및 배포 환경은 Python 3+ 지원
- 사용자 및 개발자는 기본적인 GitHub 환경과 빌드 도구 사용 숙련도 보유
- API 키 및 민감 정보는 별도 보안 정책에 따라 관리됨(코드베이스 내 민감정보 없음)
- 에이전트 운영에 필요한 기본 리소스(서버, 네트워크 등) 확보됨
- 외부 모델 및 샌드박스 연동 시 별도 인증 및 권한 승인 필요
- CLI 및 SDK는 서로 호환되는 버전으로 구성됨을 가정
- 문서 내 링크는 개발 중 변동 가능하므로 실제 운영 시 재확인 권장
