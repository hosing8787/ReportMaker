# Deep Agents Agent 기획서 초안

- 작성 배경
  - Deep Agents는 계획 수립, 파일 시스템 조작, 쉘 실행, 서브 에이전트 위임 등 범용 에이전트 하네스를 제공하는 오픈소스 Python 프로젝트입니다.
  - 모노레포 구조로 여러 패키지(SDK, CLI, 평가 도구, 파트너 통합 등)로 구성되어 있어 확장성과 관리가 용이합니다.
  - LangChain 에코시스템과 통합되며, 다양한 모델 공급자와 샌드박스 환경에서 사용 가능합니다.
- 목적
  - 다양한 AI 모델 프로바이더에 독립적인 에이전트 실행 환경을 제공하여 신속한 에이전트 개발과 배포 지원.
  - 에이전트가 사용하는 기본 도구(계획, 파일 입출력, 쉘 명령어 실행, 서브 에이전트 위임)와 컨텍스트 관리 기능 통합.
  - CLI 및 SDK 형태로 문서화되어 개발과 운영 편의성 제공.
- 비고
  - Agent 유형 분류 및 Tool List 항목은 고정 양식 유지, 체크박스로 사용 여부 표시.
  - AS-IS 와 TO-BE 워크플로우는 명확한 텍스트 기반 프로세스로 정리.
  - 구현 단계는 단계명과 상세 설명으로 분리 작성.
  - Secure 환경 제약, 권한 설정, 메모리 관리 등 운영상 유의事项은 비고에 포함.

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
| 비즈니스 목적 | 범용 AI 에이전트 하네스 제공 및 CLI/SDK 형태로 지원 |
| 주요 기능 | 계획 수립, 파일 시스템 조작, 쉘 실행, 서브 에이전트 위임, 자동 컨텍스트 관리 |
| 지원 환경 | Python 모노레포, 다양한 AI 모델 및 샌드박스 환경 |
| 버전 | libs/deepagents 0.5.3 (2024년 기준) |
| 주요 패키지 | deepagents SDK, CLI, ACP(Agent Context Protocol), 평가툴, 파트너 통합 |
| 개발 도구 | uv (패키지 관리), make (빌드/테스트), ruff(린트), ty(타입체크) |
| 문서 링크 | https://docs.langchain.com/oss/python/deepagents/overview, https://reference.langchain.com/mcp |
| 배포 체계 | LangSmith Deployment 기반 독립적 에이전트 배포 도구 제공 |

## 2. Agent 유형 분류 (Classification)

| 구분 | 유형 |
|---|---|
| 행동 방식 | [ ] 자율형 (Autonomy) : 외부의 지시 없이 스스로 동작 (Event 발생 시 수행 등) |
|  | [x] 계획형 (Planning) : 정해진 스케줄에 따라 동작 (Daily, Monthly 등) |
|  | [ ] 확장형 (Tool Use) : 외부 Tool 활용 |
|  | [ ] 학습형 (Memory) : 데이터 수집 및 VectorDB 저장, Report 작성 |
| 목적 | [ ] 단순 반사 (Simple) : 하나의 Event 발생 시 동작 |
|  | [ ] 복합 반사 (Complex) : 두 개 이상의 Event 발생 시 동작 |
|  | [ ] 수집/분석 (Memory) : 데이터 패턴 비교 및 이상 징후 감지 시 동작 |
|  | [ ] 자가복구 (Self Healing) : 정의된 정상 상태가 아닐 경우 복구 동작 수행 |
| 협력 방식 | [ ] 단독 수행 (Single) : Agent 혼자 동작 |
|  | [ ] 협력 수행 (Multi) : Agent 간 호출 및 결과 활용 (A -> B 호출) |

## 3. 업무 Flow 변화 & 구현 방안 (Work Process)

- 샘플 Flow 문서 : https://docs.langchain.com/oss/python/deepagents/overview#deep-agents-overview
- Sharepoint 링크 : 확인 필요
- 파일 네이밍
  - deepagents_main.py
  - agent_config.yaml
  - tasks_schedule.json

| 구분 | 내용 |
|---|---|
| 업무 Flow (AS-IS) | 제목: 현재 에이전트 실행 및 작업 처리 흐름 (AS-IS)<br>참여자: 사용자, 에이전트 SDK, 로컬 파일 시스템, 쉘 환경<br>흐름: 사용자 요청 입력 -> 에이전트가 계획 수립 및 작업 분할 -> 파일 시스템에 작업 결과 기록 및 읽기 -> 필요시 쉘 명령 실행 -> 서브 에이전트에게 일부 작업 위임 -> 최종 결과 반환 및 로그 저장<br>출력: 계획된 작업 목록, 수행된 파일 읽기/쓰기 로그, 쉘 명령 실행 결과, 서브 에이전트 응답, 최종 작업 결과 |
| 업무 Flow (TO-BE) | 제목: 목표 에이전트 실행 및 작업 처리 흐름 (TO-BE)<br>참여자: 사용자, Deep Agents 에이전트, 분산 샌드박스 환경, 외부 API 및 서브 에이전트<br>흐름: 사용자 입력 기반 스마트 계획 수립 -> 자동 샌드박스 내 안전한 파일 및 명령 실행 -> 서브 에이전트와 병렬 및 독립 작업 처리 -> 작업 중 자동 컨텍스트 요약과 저장 -> 실시간 작업 진행 및 상태 모니터링 -> 결과 통합 후 사용자에게 응답<br>출력: 동적 계획 및 작업 분해, 보안 강화된 쉘 및 파일 작업 로그, 서브 에이전트 실행 결과, 자동 요약 기록, 상태 대시보드 데이터, 최종 완성된 결과 |
| 구현 방안 | Core Agent: 에이전트 코어 로직 실행, 요청 처리 및 계획 수립, 도구 호출 및 컨텍스트 관리<br>Scheduler: 작업 스케줄링 및 병렬 처리 관리, 서브 에이전트 할당 및 상태 모니터링<br>Worker: 파일 시스템 조작 및 쉘 명령 실행, 서브 에이전트 작업 수행<br>External API: 외부 모델 및 도구 연동, LangChain, MCP, A2A 프로토콜 인터페이스 |

| 구현 단계 | 내용 |
|---|---|
| 1단계 - 기본 에이전트 기능 구현 | 계획, 파일 조작, 쉘 명령 수행 도구 개발<br>기본 컨텍스트 관리 및 요약 기능 구현<br>SDK 및 CLI 형태 프로토타입 작성 |
| 2단계 - 서브 에이전트 및 병렬 처리 | 서브 에이전트 위임 기능 개발<br>병렬 작업 스케줄러 제작 및 테스트<br>작업 상태 모니터링 및 오류 처리 체계 구축 |
| 3단계 - 샌드박스 및 보안 강화 | 다양한 샌드박스 연동 모듈 구현<br>명령어 및 파일 IO 제한 정책 확립<br>운영 환경에서 권한 및 접근 제어 강화 |
| 4단계 - 배포 자동화 및 문서화 | LangSmith 배포 연동<br>배포 CLI 자동화 절차 구축<br>개발자 및 사용자용 상세 문서 작성 및 관리 |

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
| Deep Agents CLI | agent_name | 기본 에이전트 ID 네임스페이스 (기본값 'agent') |
| Deep Agents CLI | timeout | 에이전트 최대 실행 시간 분 단위 (기본값 30분) |
| Deep Agents CLI | shell_allow_list | 허용된 쉘 명령어 목록 (기본 'recommended,git,gh') |
| Deep Agents CLI | enable_memory | 에이전트 메모리 지속 사용 여부 (기본 'true') |
| Deep Agents CLI | memory_scope | 메모리 캐시 공유 범위 (pr, branch, repo 중 선택, 기본 'repo') |
| Deep Agents Deploy | model | 사용할 LLM 모델 지정 (OpenAI, Anthropic, Google 등) - 필수 |
| Deep Agents Deploy | working_directory | 작업 디렉토리 경로 (기본값 현재 디렉토리 '.') |

## 6. 기타 참고사항 및 제약조건

- 에이전트 쉘 실행은 샌드박스 환경에서 안전하게 제한적으로 운영 필요
- 파일 시스템 조작은 권한과 경로 통제 필수
- 에이전트 메모리 영속성 기능은 저장공간과 개인정보 보호 정책에 준수해야 함
- 다양한 LLM 모델 지원으로 모델별 특징 및 제한사항 인지 필요
- 배포 자동화 기능은 현재 베타 단계로 API 변경 가능성 있음
- 운영 시 에이전트 실행 시간과 리소스 모니터링 필요
- 다중 서브 에이전트 실행 시 병목 및 동기화 이슈 대비 필요

## Assumptions

- 사용자는 Python 환경에서 Deep Agents SDK 및 CLI를 통한 에이전트 운영이 가능함
- LLM 모델 API 키 및 인증 정보는 별도 환경변수 또는 설정으로 관리됨
- 샌드박스 서비스 인프라가 별도로 확보되어 있음
- 메모리 기능 사용 시 적절한 캐시 설정과 권한 관리가 마련됨
- AGENTS.md 및 공식 문서 참조를 통한 개발 가이드라인을 준수
- 배포 및 CI/CD 환경은 LangSmith와 GitHub Actions 기반으로 운영
