# 리포트 패키지

현재까지 테스트 및 정리한 산출물을 보고용으로 모아둔 폴더입니다.

## 프로젝트 현황

| 프로젝트 | 원본 경로 | 현재 상태 | 비고 |
|---|---|---|---|
| Deep Agents | [deepagents-main](/C:/Users/08871/Documents/기획서%20리버스/input/original/deepagents-main) | 문서화/검증 완료 | 최종 보고자료 정리 완료 |
| CJH AI MST PRJ | [cjh_ai_mst_prj.egg-info](/C:/Users/08871/Documents/기획서%20리버스/input/original/cjh_ai_mst_prj.egg-info) | 원본 확인 완료 | 후속 문서화 대상 |
| iris | [iris.tar (1)](</C:/Users/08871/Documents/기획서 리버스/input/original/iris.tar (1)>) | 원본 확인 완료 | 후속 문서화 대상 |
| simple_now15_alt_after15_full_msgfix | [simple_now15_alt_after15_full_msgfix](/C:/Users/08871/Documents/기획서%20리버스/input/original/simple_now15_alt_after15_full_msgfix) | 원본 확인 완료 | 후속 문서화 대상 |

## Deep Agents 보고자료

- 보고 인덱스: [reports/deepagents/README.md](/C:/Users/08871/Documents/기획서%20리버스/reports/deepagents/README.md)
- 최종 기획서 Markdown: [deepagents_planning_doc_v10.md](/C:/Users/08871/Documents/기획서%20리버스/reports/deepagents/final/deepagents_planning_doc_v10.md)
- 최종 기획서 HTML: [deepagents_planning_doc_v10_confluence.html](/C:/Users/08871/Documents/기획서%20리버스/reports/deepagents/final/deepagents_planning_doc_v10_confluence.html)
- 기획서 기준 적합도 Markdown: [spec_validation_report.md](/C:/Users/08871/Documents/기획서%20리버스/reports/deepagents/final/spec_validation_report.md)
- 기획서 기준 적합도 HTML: [spec_validation_report.html](/C:/Users/08871/Documents/기획서%20리버스/reports/deepagents/final/spec_validation_report.html)
- 기획서 기준 적합도 JSON: [spec_validation_report.json](/C:/Users/08871/Documents/기획서%20리버스/reports/deepagents/final/spec_validation_report.json)

## 테스트 결과

- 자동 테스트: `13 / 13` 통과
- 실행 명령: `python -m unittest discover -s tests -v`
- 샘플 적합도 검증 결과: `85%`, 판정 `높음`

## 권장 사용 순서

1. 최종 HTML 기획서 확인
2. 적합도 검증 HTML 확인
3. 필요 시 Markdown 원문 및 JSON 상세 검토
4. 수정 이력은 `reports/deepagents/history` 참고
