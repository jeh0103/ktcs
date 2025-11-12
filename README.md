고객 이탈 위험 대시보드 (Customer Churn Risk Dashboard)

고객의 행동·만족 데이터를 기반으로 이탈 위험도를 실시간 분석하고,
관리자가 즉시 대응할 수 있도록 돕는 Streamlit 기반 대시보드입니다.

⸻

프로젝트 개요
	•	목적:
기계학습 기반 이탈 예측 모델(IF, AE)을 활용해 이탈 위험 고객을 조기에 탐지하고
고객별 위험 요인과 대응 지침을 제공합니다.
	•	기능:
	•	전역 필터(나이·성별·프리미엄 여부)
	•	동적 임계값 튜닝(IF/AE 기준 조정)
	•	위험도 그라데이션 시각화
	•	고객 상세 페이지(활동·만족 지표 비교, Top 위험 요인, 권장 액션)
	•	SQLite 기반 액션 로그 기록

⸻

📁 폴더 구조

 project-root
├── app_enhanced.py                # 메인 대시보드
├── pages/
│   └── 01_Customer_Detail.py      # 고객 상세 페이지
├── ecommerce_customer_data.csv    # 원본 고객 데이터 (성별 문자열 포함)
├── ecommerce_customer_data_featured.csv
├── ecommerce_customer_churn_hybrid_with_id.csv
├── gender_code_map.json           # (선택) 성별 코드→라벨 매핑 저장 파일
├── gender_label_map.json          # (선택) 라벨 커스터마이징 저장 파일
└── README.md                      # 현재 문서


⸻

실행 방법

(1) 권장: 가상환경 생성

python3 -m venv .venv
source .venv/bin/activate

(2) 필수 패키지 설치

python -m pip install --upgrade pip
python -m pip install "streamlit>=1.30" pandas numpy

(3) (선택) 리스트 위험도 그라데이션용 Matplotlib 설치
(Matplotlib이 없으면 CSS 그라데이션으로 자동 대체됩니다.)

python -m pip install matplotlib

(4) 앱 실행

python -m streamlit run app_enhanced.py

💡 실행 후 브라우저에서 http://localhost:8501 로 접속하세요.
pages/01_Customer_Detail.py가 자동 인식되어 멀티페이지 구조로 표시됩니다.

⸻

 주요 기능 화면

구분	설명
📊 대시보드 홈	전역 필터 + 이탈 위험 고객 리스트(빨강 그라데이션 시각화)
👤 고객 상세 페이지	활동·만족 지표 비교, 전체 대비 분위(%) 및 리스크(%) 시각화
🔥 Top 리스크 요인 카드	z-score 상위 3개 요인 + 즉시 실행 가능한 권장 액션
📌 액션 로그	콜백·쿠폰·케어 등 실제 대응 이력 기록/조회 (SQLite)


⸻

 데이터 처리 요약
	•	원본(ecommerce_customer_data.csv)의 문자열 성별을 표준화(남성/여성/기타/응답거부/미상)
	•	하이브리드(_hybrid_with_id.csv)와 CustomerID 기준으로 조인
	•	일관된 GenderLabel 컬럼 생성 → 필터/시각화/상세 페이지 모두 동일 기준 사용

⸻

🧱 기술 스택

구분	사용 기술
Frontend/UI	Streamlit 1.30+, CSS Gradient, Markdown Components
Backend/Data	Python 3.10+, Pandas, NumPy
Visualization	Matplotlib (optional), CSS heatmap
Storage	SQLite (액션 로그), JSON (라벨 매핑)


⸻

✍️ 작성자 & 라이선스
	•	Author: 조은형￼
	•	License: MIT
	•	Last Updated: 2025-11-12


추가할까요?
