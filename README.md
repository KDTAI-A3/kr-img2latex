# KR-IMG2LATEX

## Summary(Our Function)
- 수식이 포함된 이미지를 텍스트 및 Latex 형태로 변환 (한국어 지원)
- 텍스트 및 Latex 변환 결과물을 바탕으로 `ChatGPT-API`를 통해 해당 수식의 다양한 정보 제공
- 해당 수식의 수준 분류 (초4 ~ 고3)

## A3 - Caffeine-Holic
![Alt text](image.png)
- 전현욱 : 팀장, 프로젝트 관리
- 왕준호 : 부팀장, Main Model 개발, 데이터 전처리
- 박동수 : Main Model 개발, 학습 전략 구성
- 장유림 : 서브 모델 개발, 데이터 전처리
- 박재현 : 서브 모델 개발, ChatGPT-API 기능 구현
- 박영규 : 서버 관리, 백엔드 개발, 모델 개발 보조
- 송승헌 : 서버 관리, 프론트엔드 개발, 모델 개발 보조

## Our Model Score
- F1
- MSE
- Levenshtein

## Model Building Process
![Alt text](image-1.png)

## Training Data
- 출처: [AIHub 수식, 도형, 낙서기호 OCR 데이터](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=479)
- Token Vocabulary 출처: Notepad++ - Latex AutoComplete XML File

## References
- DONUT(naver/clova)
- openai-api
- easyocr
- kaggle
