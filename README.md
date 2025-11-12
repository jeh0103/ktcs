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

⸻

 주요 기능 화면

구분	설명

📊 대시보드 홈	전역 필터 + 이탈 위험 고객 리스트(빨강 그라데이션 시각화)

👤 고객 상세 페이지	활동·만족 지표 비교, 전체 대비 분위(%) 및 리스크(%) 시각화

🔥 Top 리스크 요인 카드	z-score 상위 3개 요인 + 즉시 실행 가능한 권장 액션

📌 액션 로그	콜백·쿠폰·케어 등 실제 대응 이력 기록/조회 (SQLite)


