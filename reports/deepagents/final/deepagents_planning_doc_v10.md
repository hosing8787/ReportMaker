# Deep Agents 프로젝트 Agent 기획서

- 작성 배경
  - Deep Agents는 범용 에이전트 하네스 제공을 목표로 하며 계획 수립, 파일 시스템 조작, 쉘 실행, 서브에이전트 위임 기능을 포함한다.
  - Python 모노레포 구조로 SDK, CLI, 평가, 에이전트 프로토콜 연동 및 다양한 샌드박스 통합을 포함하는 복합 프로젝트임.
  - 사용자가 별도 설정 없이 즉시 사용 가능한 완전 작동형 에이전트를 제공하고 필요한 도구와 모델 교체를 제공한다.
- 목적
  - 범용 AI 에이전트를 CLI 및 SDK 형태로 활용 가능하게 구현.
  - 에이전트가 자체적으로 플래닝, 파일 입출력, 쉘 명령 실행과 서브에이전트 관리 기능을 갖추도록 함.
  - 오픈소스 및 표준 프로토콜(MCP, A2A 등) 기반으로 확장성과 자율성을 확보.
- 비고
  - Agent 유형 분류와 Tool 리스트는 고정된 체크박스 폼으로 작성하며, 체크 유무는 전체 문맥 기반으로 설정.
  - 개요는 2열 표 형식에 맞도록 간결 문장 위주 작성.
  - 업무 프로세스는 AS-IS, TO-BE 2단계로 actors, steps, outputs 명확히 구분하여 텍스트 형태로 표현.
  - 구현 단계는 ‘1단계 ...’ 형식으로 바로 표에 들어가도록 작성.
  - 확실치 않은 부분은 '확인 필요', '미정'으로 표시.
  - 민감정보 임의 생성 금지.

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
| 프로젝트명 | Deep Agents |
| 비즈니스 목적 | 범용 AI 에이전트 하네스 제공, CLI/SDK 형태로 활용 가능 |
| SDK 언어 | Python (모노레포) / 참고용 JS/TS 존재 |
| 주요 기능 | 계획 수립, 파일 시스템 조작, 쉘 실행, 서브에이전트 위임 |
| 버전관리 | 각 패키지별 독립 버전 (deepagents 0.5.3, cli 0.0.40 등) |
| 개발/배포 도구 | uv 패키지 관리자, make 기반 자동화, GitHub Actions CI/CD |
| 샌드박스 통합 | Daytona, Modal, Runloop, QuickJS 등 다중 샌드박스 |
| 사용 모델 | Anthropic, OpenAI, Google, Bedrock, Baseten 등 다수 지원 |
| 문서 링크 | https://docs.langchain.com/oss/python/deepagents/overview (확인 필요) |
| 오픈소스 라이선스 | MIT 라이선스 |

## 2. Agent 유형 분류 (Classification)

| 구분 | 유형 |
|---|---|
| 행동 방식 | [x] 자율형 (Autonomy) : 외부의 지시 없이 스스로 동작 (Event 발생 시 수행 등) |
|  | [x] 계획형 (Planning) : 정해진 스케줄에 따라 동작 (Daily, Monthly 등) |
|  | [x] 확장형 (Tool Use) : 외부 Tool 활용 |
|  | [x] 학습형 (Memory) : 데이터 수집 및 VectorDB 저장, Report 작성 |
| 목적 | [ ] 단순 반사 (Simple) : 하나의 Event 발생 시 동작 |
|  | [x] 복합 반사 (Complex) : 두 개 이상의 Event 발생 시 동작 |
|  | [x] 수집/분석 (Memory) : 데이터 패턴 비교 및 이상 징후 감지 시 동작 |
|  | [ ] 자가복구 (Self Healing) : 정의된 정상 상태가 아닐 경우 복구 동작 수행 |
| 협력 방식 | [ ] 단독 수행 (Single) : Agent 혼자 동작 |
|  | [x] 협력 수행 (Multi) : Agent 간 호출 및 결과 활용 (A -> B 호출) |

## 3. 업무 Flow 변화 & 구현 방안 (Work Process)

- 샘플 Flow 문서 : AGENTS.md (GitHub / 리포지토리 내 위치) / 확인 필요
- Sharepoint 링크 : 확인 필요
- 파일 네이밍
  - agent_config.yaml
  - flow_diagram.drawio
  - README.md
  - scripts/*.py

| 구분 | 내용 |
|---|---|
| 업무 Flow (AS-IS) | 제목: 기존 Deep Agents 에이전트 적용 및 개발 과정<br>참여자: Agent 개발자, 사용자, LLM 모델, 로컬 파일 시스템<br>흐름: 사용자가 CLI 또는 SDK로 에이전트 호출 -> 에이전트가 계획 수립 및 작업 분할 -> 필요 시 파일 시스템에서 파일 읽기/쓰기 수행 -> 쉘 명령을 안전 모드에서 실행 -> 하위 에이전트(task) 생성하여 작업 위임 -> 응답을 사용자에게 반환<br>출력: 최종 명령 수행 결과, 파일시스템 변경 내용, 로그 및 상태 추적 |
| 업무 Flow (TO-BE) | 제목: 확장형 Deep Agents 운영 환경<br>참여자: Agent 개발자, 사용자, 멀티 모델 서비스, 분산 샌드박스, 서브에이전트 관리 서비스<br>흐름: 사용자가 CLI/SDK/API 통해 에이전트 호출 -> 에이전트가 자동 플래닝 및 동적 컨텍스트 관리 -> 멀티 샌드박스 환경에서 쉘 및 코드 실행 -> 서브에이전트 간 비동기 통신 및 협업 -> LangSmith 배포 통해 배포 및 상태 관리 -> 운영 중 지속적 모니터링과 퍼포먼스 개선<br>출력: 서비스화된 에이전트 응답, 멀티 샌드박스 결과, 배포 상태 리포트 |
| 구현 방안 | Core Agent: 플래닝, 작업 분할, 도구 호출 및 컨텍스트 관리<br>Scheduler: 작업 스케줄링 및 서브에이전트 할당<br>Worker / Sub-agent: 분리된 컨텍스트에서 개별 작업 실행<br>External API: MCP, A2A, GitHub, Google API 등 외부 서비스 연동<br>Sandbox Providers: Daytona, Modal, Runloop, QuickJS를 이용한 안전 실행 환경 |

| 구현 단계 | 내용 |
|---|---|
| 1단계 기본 에이전트 실행 환경 구축 | Python SDK 설치 및 초기화<br>기본 플래너 및 파일/쉘 도구 통합 |
| 2단계 CLI 인터페이스 및 평가 도구 통합 | CLI 툴 설치<br>자동 테스트 및 평가 프레임워크 연결 |
| 3단계 샌드박스 연동 | Daytona 및 Modal 샌드박스 통합<br>쉘 및 코드 실행 안전성 강화 |
| 4단계 서브에이전트 및 프로토콜 구현 | Agent Protocol(A2A) 기반 서브에이전트 관리 구현<br>비동기 통신 및 작업 위임 기능 구현 |
| 5단계 배포 및 운영 자동화 | LangSmith 배포 스크립트 활용<br>메모리 캐시 및 상태 지속성 구현 |

## 4. 운영 Tool 리스트 (Tool List)

- 추가가 필요한 경우 자유롭게 추가

| 구분 | 관리 시스템 | 사내 시스템 | 고객사 시스템 | Message | KM | ... |
|---|---|---|---|---|---|---|
| 사내/고객사의 운영 관리 시스템 |  | [ ] Work Portal<br>[ ] 통풍감<br>[ ] MCMP<br>[ ] OPMATE<br>[ ] ServiceFlow<br>[ ] ... | [ ] ServiceNow<br>[ ] Jira<br>[ ] Confluence<br>[ ] ... | [ ] Slack<br>[ ] Email<br>[ ] SMS<br>[ ] ... | [ ] AirTable<br>[ ] Confluence<br>[ ] Jira<br>[ ] GitLab<br>[ ] ... | [ ] ...<br>[ ] ... |

| 구분 | Log | Cloud | 서버(OS) | DB | MW | Kubernetes | Network | AI DC |
|---|---|---|---|---|---|---|---|---|
| Tower별 운영 솔루션 | [ ] Splunk<br>[ ] AMON<br>[ ] 통풍감<br>[ ] ... | [ ] Datadog<br>[ ] ... | [ ] AnyCatcher (On-Prem)<br>[ ] Ontune (On-Prem)<br>[ ] Ontune (k8s)<br>[ ] ... | [ ] Prometheus<br>[ ] Grafana<br>[ ] Sherpa<br>[ ] ... | [ ] Pinpoint<br>[ ] EnPharos<br>[ ] ... | [ ] Prometheus<br>[ ] Grafana<br>[ ] ... | [ ] NMS<br>[ ] Telenet Center<br>[ ] ... | [ ] DCIM<br>[ ] ... |


## 5. Agent 동작 필수 파라미터 (Parameters)

| 시스템 | 파라미터 | 값 / 설명 |
|---|---|---|
| deepagents deploy | model | 사용자 지정 가능 (예: OpenAI, Anthropic 등) - 상세 모델명 확인 필요 |
| deepagents deploy | timeout | 최대 실행 시간, 기본 30분 |
| deepagents.deploy | agent_name | 에이전트 아이덴티티 이름, 메모리 네임스페이스 용 |
| Shell | shell_allow_list | 허용된 쉘 명령어 목록 (기본: recommended,git,gh) |
| memory cache | enable_memory | 에이전트 메모리 지속 여부 (default: true) |
| memory cache | memory_scope | 캐시 범위 (pr, branch, repo) - 운영 정책에 따라 설정 |
| CI/CD | pyproject version | 프로젝트 버전 일치가 필수 |
| Linting | ruff 규칙 suppress | 필요 시 인라인 #noqa 사용 권장, 전체 파일 무시 지양 |

## 6. 기타 참고사항 및 제약조건

- 운영 시 에이전트의 쉘 실행으로 인한 보안 이슈에 유의해야 함
- 에이전트 메모리 캐시 관리는 workflow 환경 별 차이에 따른 관리 정책 필요
- 서브에이전트 간 통신 시 비동기 프로토콜 호환성 유지 및 에러 핸들링 요구
- 외부 API 키(Anthropic, OpenAI, Google 등) 보안 관리 필요
- 베타 단계 배포 기능으로 구성 및 API 변경 가능성 있음
- 릴리즈 프로세스 자동화로 버전 관리와 호환성 확인 자동화 권장

## Assumptions

- 사용자는 Python 및 CLI 환경에 익숙함
- SDK와 CLI가 동일 레포지토리에 존재하며 버전 일치 필수
- Agent 시스템은 오픈 소스 기반으로 자유롭게 확장 가능
- MCP, A2A, Agent Protocol 등 표준 프로토콜을 따른다
- 샌드박스 제공자 통합 모듈은 별도 패키지로 관리됨
- 고급 사용자는 샌드박스나 모델을 교체 및 커스텀 가능
