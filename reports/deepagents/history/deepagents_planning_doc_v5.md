# Deep Agents 기획서 초안

- 작성 배경
  - Deep Agents 프로젝트는 범용 에이전트 하네스를 제공하는 오픈소스 Python 모노레포 프로젝트입니다.
  - 계획 수립, 파일 시스템 조작, 쉘 실행, 서브에이전트 위임 기능을 포함하며 CLI와 SDK 형태로 사용할 수 있습니다.
  - 다양한 샌드박스 환경과 모델 공급자들을 지원하도록 설계되었습니다.
  - 프로젝트 구조가 libs 내 여러 패키지로 모듈화되어 있고, 뛰어난 확장성과 관리 편의성을 보장합니다.
- 목적
  - 범용적으로 사용 가능한 에이전트 하네스를 개발하여 LLM 기반 작업 자동화 지원.
  - 개발자와 조직이 쉽게 커스터마이징하고 확장할 수 있는 오픈소스 솔루션 제공.
  - 안정적인 CI/CD와 린팅, 포맷팅, 테스트 워크플로우 구축으로 고품질 코드 유지.
  - 다양한 모델과 샌드박스 환경과 연동 가능한 개방형 프로토콜 적용.
  - 문서화 및 예제 제공을 통해 개발 입문 장벽 최소화.
- 비고
  - 문서는 사내 표준 에이전트 기획서 양식에 최대한 부합하도록 기술적 내용을 요약하였음.
  - 불확실하거나 코드에서 명확하지 않은 정보는 '확인 필요'로 표기함.
  - 분류 부분은 코드 내 명확한 체크리스트를 그대로 반영함.
  - 툴 목록과 파라미터 표는 현재 저장소 구조와 설정 파일 기반으로 작성하였음.
  - 목차는 필요한 주요 섹션 위주로 구성함.

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
| Agent 설명 | 모델-불가지론적, 범용 AI 에이전트 하네스. 계획, 파일/쉘 조작, 서브에이전트 위임 지원. |
| Agent 개발목적 | 다양한 모델 및 샌드박스에서 즉시 실행 가능한 범용 agent 프레임워크 제공. |
| 주요 업무 범위 | 작업 계획 수립, 파일 시스템 작업, 쉘 커맨드 실행, 서브에이전트 관리. |
| 개발 인원 산정 | 확인 필요 |
| Agent E2E | SDK/CLI를 통한 호출, 내부 미들웨어 및 툴체인, 샌드박스 환경 통합, MCP/A2A 프로토콜 지원. |
| 개발 방식 | 모노레포 구조, Python, uv 패키지 관리, Makefile 기반 명령어, 린팅/포맷팅/테스트 자동화. |
| Main Workflow 링크 | 확인 필요 |
| 산출물/참조 링크 | https://github.com/langchain-ai/deepagents, https://docs.langchain.com/oss/python/deepagents/overview |

## 2. Agent 유형 분류 (Classification)

| 구분 | 선택 항목 |
|---|---|
| Agent 유형 | [x] 범용 에이전트 - 기본 유형<br>[ ] 특화 에이전트 - 현재 없음<br>[x] 서브 에이전트 - 서브에이전트 위임 기능 포함 |
| 개발 언어 및 환경 | [x] Python - 메인 구현 언어<br>[ ] TypeScript / JS - 참고용 deepagents.js 별도 존재<br>[ ] Other - 없음 |
| 배포 및 실행 환경 | [x] 로컬 - 개발 및 테스트 중심<br>[x] 클라우드 - LangSmith, Modal, Daytona 등 샌드박스 연동 가능<br>[ ] 컨테이너 - 확인 필요 |
| 인터페이스 | [x] CLI - deepagents-cli<br>[x] SDK (Python) - libs/deepagents SDK 제공<br>[ ] 웹 UI - 확인 필요 |

## 3. 업무 Flow 변화 & 구현 방안 (Work Process)

| 구분 | 내용 |
|---|---|
| 1. 사용자 입력 | 사용자는 CLI 혹은 SDK를 통해 작업 명령, 메시지 입력.<br>입력은 내부 agent로 전달됨. |
| 2. 작업 계획 수립 | 에이전트가 작업 목표를 분해하여 '할 일' 목록 작성.<br>계획 작성에 write_todos 활용. |
| 3. 도구 및 리소스 사용 | 파일 시스템 도구(ls, read_file, write_file 등) 사용하여 컨텍스트 읽고 쓰기.<br>쉘 실행(execute)으로 외부 명령 수행(샌드박스(strict) 내). |
| 4. 서브에이전트 위임 | 복잡한 작업은 독립된 서브에이전트에게 위임 가능.<br>서브에이전트는 자체 컨텍스트와 토이 관리. |
| 5. 결과 통합 및 응답 | 에이전트가 작업 결과 취합 및 정리.<br>사용자에게 최종 응답 반환. |
| 6. 컨텍스트 및 메모리 관리 | 대화와 작업 기록 자동 요약.<br>장기 컨텍스트 저장 및 관리 가능(메모리 지속화). |

## 4. 운영 Tool 리스트 (Tool List)

| 구분 | 선택 항목 |
|---|---|
| Sandbox Integrations | [x] Daytona - 샌드박스 제공 및 격리된 쉘 환경 실행<br>[x] Modal - 서버리스 샌드박스 및 함수 실행<br>[x] Runloop - 반복 실행 샌드박스 환경<br>[x] QuickJS - JS 샌드박스 엔진 |
| Agent Clients & Protocols | [x] Agent Protocol (A2A) - 에이전트 상호운용성 프로토콜<br>[x] Model Context Protocol (MCP) - 모델과 에이전트 간 컨텍스트 표준화 |
| Agent SDK & CLI | [x] deepagents SDK - 에이전트 생성, 커스터마이징, 호출<br>[x] deepagents-cli - 커맨드라인 인터페이스로 에이전트 활용 |
| Lint, Format, Test | [x] ruff, make, pytest - 코드 품질 관리 및 테스트 자동화 |
| Package Manager | [x] uv - 패키지 의존성 설치 및 관리 |

## 5. Agent 동작 필수 파라미터 (Parameters)

| 시스템 | 파라미터 | 값 / 설명 |
|---|---|---|
| Agent CLI Workflow | working_directory | 기본 '.' (현재 경로)로 셋업 |
| Agent CLI Workflow | agent_name | 기본값 'agent' (메모리 네임스페이스 지정) |
| Agent CLI Workflow | enable_memory | true (에이전트 메모리 지속화, 캐시 활용) |
| Agent CLI Workflow | memory_scope | 'repo' (캐시 범위: PR, branch, repo 중 선택) |
| Agent CLI Workflow | timeout | 30 (최대 실행 시간 분 단위, 기본값 30분) |
| Agent CLI Workflow | shell_allow_list | 'recommended,git,gh' (허용된 쉘 커맨드 리스트) |

## 6. 기타 참고사항 및 제약조건

- 실행 환경에서 외부 명령어 실행 시 샌드박스 엄격 제어 필요 (보안 위험 대비).
- Agent 메모리 저장 및 복원 시 권한 및 데이터 민감도 관리 중요.
- 오픈소스 특성상 버전 업그레이드 시 호환성 및 API 변경 감지 필요.
- 자동 린팅과 테스트 프로세스 준수해야 안정적 운영 가능.
- Beta 상태인 배포 기능은 변경 가능성이 있으니 운영 전 신중한 검토 요망.
- 외부 API 키 (OpenAI, Anthropic, Google 등) 취급 시 별도 보안 관리 필요.
- 다양한 샌드박스(Modal, Daytona 등) 연동 설정 및 상태 모니터링 필요.
- 모델 공급자별 차이에 따라 설정 파라미터 조정 가능성이 있음.

## Assumptions

- 개발 인원 산정은 내부 미정, 추후 확인 필요.
- Main Workflow 및 산출물 링크는 공식 문서 및 저장소 링크 외 명확한 경로 확인 필요.
- 웹 UI는 공식적으로 제공하지 않는 것으로 추정되나 변경 가능성 있음.
- Agent 사용자는 Python 3.11+ 및 uv 환경에 익숙하다고 가정.
- 에이전트 구성과 확장 시 MCP, A2A, Agent Protocol 표준 사용을 전제로 함.
