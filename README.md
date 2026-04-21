# 코드 기반 Agent 기획서 생성기

코드나 저장소를 넣으면, Agent 기획서 초안을 Markdown으로 생성합니다.

## 현재 구성

- 코드 수집: 주요 텍스트 파일을 읽어 요약 컨텍스트 생성
- LLM 분석: 구조화 출력(JSON Schema)로 기획서 데이터 생성
- 문서 렌더링: 샘플 양식에 맞춘 Markdown 출력

## Azure OpenAI 설정

이 프로젝트는 `.env` 파일을 자동으로 읽습니다.

필수 환경변수:

- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_MODEL`

현재 `.env`에는 Azure OpenAI 기준 기본 모델이 설정되어 있습니다.

Azure OpenAI Responses API 사용 방식은 Microsoft 공식 문서의 `base_url=https://YOUR-RESOURCE.openai.azure.com/openai/v1/` 패턴을 따랐습니다.

- [Azure OpenAI Responses API](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses)
- [Azure OpenAI Quickstart](https://learn.microsoft.com/en-us/azure/ai-services/openai/quickstart?pivots=programming-language-python&tabs=command-line)
- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses&lang=python)

## 설치

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 실행

```powershell
python run.py `
  --source "C:\path\to\your\repo" `
  --project-name "DB 장애 모니터링 Agent" `
  --purpose "RDS 이상 징후를 감지하고 알림 및 후속 액션을 정리하는 Agent 문서화" `
  --context "운영팀 제출용 초안" `
  --output ".\agent_planning_doc.md" `
  --html-output ".\agent_planning_doc.html"
```

단일 파일도 가능합니다.

```powershell
python run.py --source "C:\path\to\main.py"
```

코드 유사도 비교도 가능합니다.

```powershell
python compare.py `
  --source-a "C:\path\to\original_repo" `
  --source-b "C:\path\to\generated_repo" `
  --output ".\code_similarity_report.md" `
  --json-output ".\code_similarity_report.json"
```

이 비교기는 파일 구조, 토큰, Python 함수/import/call 구조, 전체 텍스트 유사도를 종합해서 기능 유사도를 추정합니다.

Confluence 붙여넣기용 HTML 변환도 가능합니다.

```powershell
python export_html.py `
  --input ".\deepagents_planning_doc_v4.md" `
  --output ".\deepagents_planning_doc_v4_confluence.html"
```

생성된 HTML 파일을 브라우저에서 열어 전체 복사 후 Confluence에 붙여넣으면 표 레이아웃이 Markdown보다 안정적으로 유지됩니다.

기획서 기준 코드 적합도 검증도 가능합니다.

```powershell
python validate_from_plan.py `
  --plan ".\deepagents_planning_doc_v10.md" `
  --source "C:\path\to\generated_repo" `
  --output-md ".\spec_validation_report.md" `
  --output-json ".\spec_validation_report.json" `
  --output-html ".\spec_validation_report.html"
```

이 검증기는 기획서와 코드 요약을 함께 보고 다음을 평가합니다.

- 섹션별 적합도 점수
- 핵심 요구사항 충족 여부
- 주요 리스크
- 권장 보완 작업

## 테스트

별도 테스트 프레임워크 설치 없이 표준 라이브러리로 검증할 수 있습니다.

```powershell
python -m unittest discover -s tests -v
```

검증 범위:

- 코드 수집 로직과 스킵 디렉터리 처리
- 단일 파일/디렉터리 입력 처리
- Markdown 렌더링 결과
- 코드 유사도 비교 리포트
- 기획서 기준 기능 적합도 검증 리포트
- `.env` 로딩
- Azure/OpenAI 클라이언트 분기
- 문서 생성 함수의 구조화 출력 처리

## 보고 자료

현재까지 정리한 보고용 산출물은 `reports/` 아래에 모아두었습니다.

- 전체 인덱스: [reports/README.md](/C:/Users/08871/Documents/기획서%20리버스/reports/README.md)
- 전체 인덱스 HTML: [reports/README.html](/C:/Users/08871/Documents/기획서%20리버스/reports/README.html)
- Deep Agents 보고 패키지: [reports/deepagents/README.md](/C:/Users/08871/Documents/기획서%20리버스/reports/deepagents/README.md)
- Deep Agents 보고 패키지 HTML: [reports/deepagents/README.html](/C:/Users/08871/Documents/기획서%20리버스/reports/deepagents/README.html)

Deep Agents 기준 주요 결과:

- 최종 기획서 HTML: [deepagents_planning_doc_v10_confluence.html](/C:/Users/08871/Documents/기획서%20리버스/reports/deepagents/final/deepagents_planning_doc_v10_confluence.html)
- 기획서 기준 적합도 HTML: [spec_validation_report.html](/C:/Users/08871/Documents/기획서%20리버스/reports/deepagents/final/spec_validation_report.html)
- 자동 테스트: `13 / 13` 통과
- 샘플 적합도 검증: `85%`, 판정 `높음`

보고 시 추천 순서:

1. 최종 기획서 HTML 확인
2. 적합도 검증 HTML 확인
3. Markdown 원문 및 JSON 상세 검토
4. `reports/deepagents/history`에서 형식 보정 이력 확인

## 출력 섹션

- `1. 개요 (Overview)`
- `2. Agent 유형 분류 (Classification)`
- `3. 업무 Flow 및 구현 방식 (Work Process)`
- `4. 운영 Tool 리스트 (Tool List)`
- `5. Agent 동작 필수 파라미터 (Parameters)`
- `6. 기타 참고사항 및 제약조건`

## 다음 확장 아이디어

- Word 또는 HTML 양식 출력
- Confluence 업로드 자동화
- 다이어그램 이미지 자동 생성
- 사내 고정 문구/체크리스트 템플릿 추가
