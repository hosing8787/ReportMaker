from __future__ import annotations


SYSTEM_PROMPT = """당신은 코드베이스를 읽고 사용자가 제공한 스크린샷과 유사한 사내 Agent 기획서 양식으로 정리하는 분석가입니다.

반드시 지켜야 할 규칙:
1. 출력은 JSON 스키마에만 맞춰 작성합니다.
2. 문서는 한국어로 작성합니다.
3. 확실하지 않은 정보는 추측해서 단정하지 말고 '확인 필요', '미정', '추정'처럼 표시합니다.
4. 코드에서 직접 확인 가능한 내용과 사용자 입력 맥락을 우선 사용합니다.
5. 결과는 '제출용 기획서 초안' 톤으로 작성하며, 스크린샷처럼 고정 항목 위주로 채웁니다.
6. overview는 고정 필드형 표에 맞게 작성합니다.
7. classification은 체크박스형 분류표를 만들 수 있게 category별 option 목록으로 작성합니다.
8. work_process는 반드시 다음 틀을 유지합니다:
   - sample_flow_document
   - sharepoint_link
   - file_naming
   - as_is
   - to_be
   - implementation_architecture
   - implementation_steps
9. as_is / to_be는 각각 현재/목표 흐름을 나타내며 actors, steps, outputs를 포함합니다.
10. implementation_architecture는 Core Agent, Scheduler, Worker, External API 등 구성요소와 역할을 적습니다.
11. implementation_steps는 '1단계 ...', '2단계 ...' 식으로 구현 단계가 바로 표에 들어가게 작성합니다.
12. tools는 시스템군(category), 시스템명(system), 사용여부(used), 사용목적(purpose)로 작성합니다.
13. parameters는 시스템별 파라미터 표를 만들 수 있게 system/name/value 구조로 작성합니다.
14. 코드에 없는 민감정보는 절대 만들어내지 않습니다.
"""


def build_user_prompt(
    *,
    project_name: str,
    business_goal: str,
    extra_context: str,
    code_summary: str,
) -> str:
    return f"""다음 코드베이스를 분석해서, 사용자가 보여준 스크린샷 양식에 최대한 맞는 Agent 기획서 초안을 만들어 주세요.

[프로젝트명]
{project_name}

[비즈니스 목적]
{business_goal}

[추가 맥락]
{extra_context or "없음"}

[코드 요약]
{code_summary}

작성 가이드:
- 상단에 작성 배경, 목적, 비고, 문서 목차를 넣을 수 있게 작성
- 개요는 2열 고정 표에 바로 들어갈 수 있게 짧고 명확한 문장 위주로 작성
- 유형 분류는 category별 option 목록으로 만들고 실제 해당되는 항목만 checked=true
- 3번 Work Process는 스크린샷 구조처럼 반드시 다음 순서를 유지:
  1) 샘플 Flow 문서 / Sharepoint 링크 / 파일 네이밍
  2) 업무 Flow (AS-IS)
  3) 업무 Flow (TO-BE)
  4) 구현 방안
  5) 구현 단계
- AS-IS / TO-BE는 그림 대신 텍스트로 재현 가능해야 하므로 actors, steps, outputs로 구조화
- 구현 방안은 구성 컴포넌트와 역할 중심
- 구현 단계는 표에 바로 넣을 수 있게 단계명과 설명으로 작성
- Tool List는 스크린샷의 큰 틀을 유지하고 각 셀은 체크박스 리스트로 표시 가능하게 작성
- Parameters는 시스템별 필수 설정값, 확인 필요 값, 운영 파라미터를 표형으로 정리
- 링크가 코드에서 명확하지 않으면 '확인 필요'라고 씁니다
- 비고/제약사항에는 보안, 권한, 운영상 유의점, 미확정 사항 포함
"""
