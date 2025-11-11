import streamlit as st
import pandas as pd

# -------------------------------
# 📂 데이터 로드
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("ecommerce_customer_churn_hybrid_with_id.csv")

df = load_data()

# -------------------------------
# 📌 URL 파라미터에서 고객 ID 가져오기 (문자 단위 버그 해결)
# -------------------------------
params = st.query_params

if "customer_id" in params:
    value = params["customer_id"]
    # Streamlit이 list나 문자열로 반환하므로 둘 다 처리
    if isinstance(value, list):
        customer_id = "".join(value)
    else:
        customer_id = str(value)
else:
    customer_id = None

# -------------------------------
# 고객 상세 페이지
# -------------------------------
if not customer_id:
    st.warning("❗ 고객 ID가 선택되지 않았습니다. 메인 페이지에서 고객을 클릭하세요.")
    st.page_link("app.py", label="⬅️ 대시보드로 돌아가기", icon="🏠")
else:
    st.page_link("app.py", label="🏠 ⬅️ 대시보드로 돌아가기")
    st.title(f"📋 고객 맞춤 관리 전략 - {customer_id}")

    # 데이터 조회
    customer = df[df["CustomerID"] == customer_id]
    if customer.empty:
        st.error(f"❌ '{customer_id}' 고객 데이터를 찾을 수 없습니다.")
    else:
        row = customer.iloc[0]

        # -------------------------------
        # 이탈 유형 판별
        # -------------------------------
        churn_type = "공통 이탈" if row["Both_ChurnFlag"] == 1 else \
                     "불만형 이탈(IF)" if row["IF_ChurnFlag"] == 1 else \
                     "조용한 이탈(AE)" if row["AE_ChurnFlag"] == 1 else "정상"

        # -------------------------------
        # 🚨 이탈 위험도 시각화
        # -------------------------------
        st.markdown("### 🚨 이탈 위험도")

        risk_score = row['ChurnRiskScore']
        risk_level = min(risk_score / 2.5, 1.0)

        # 게이지 표시
        st.progress(risk_level)

        # 텍스트 단계 표시
        if risk_level >= 0.8:
            level_text = f"🔴 매우 높음 ({risk_score:.2f})"
            badge_color = "rgba(255,76,76,0.2)"
        elif risk_level >= 0.5:
            level_text = f"🟠 중간 ({risk_score:.2f})"
            badge_color = "rgba(255,180,76,0.2)"
        else:
            level_text = f"🟢 낮음 ({risk_score:.2f})"
            badge_color = "rgba(76,255,100,0.2)"

        # 등급 배지 시각화
        st.markdown(
            f"""
            <div style='display:inline-block;
                        background-color:{badge_color};
                        padding:6px 12px;
                        border-radius:8px;
                        font-weight:bold;
                        font-size:14px;
                        margin-bottom:10px;'>
                {level_text}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        # -------------------------------
        # 📊 고객 기본 지표
        # -------------------------------
        st.markdown(f"### 📊 이탈 유형: **{churn_type}**")
        st.write(f"- **ChurnRiskScore:** {row['ChurnRiskScore']:.2f}")
        st.write(f"- **PurchaseFrequency:** {row['PurchaseFrequency']:.2f}")
        st.write(f"- **CSFrequency:** {row['CSFrequency']:.2f}")
        st.write(f"- **RecencyProxy:** {row['RecencyProxy']:.2f}")
        st.markdown("---")

        # -------------------------------
        # 🎯 맞춤 관리 전략
        # -------------------------------
        if churn_type == "공통 이탈":
            st.error("🚨 **핵심 고객 유지 필요:** VIP 케어, 프리미엄 혜택 제공")
            st.info("- 최근 불만 사항 점검 및 해결")
            st.info("- 이탈 방지용 전담 CS 배정, 보상 쿠폰 발송")
        elif churn_type == "불만형 이탈(IF)":
            st.warning("⚠️ **불만 해소형 고객:** 상담 품질 개선 필요")
            st.info("- 고객 CS 기록 검토, 응대 개선 피드백 실행")
            st.info("- 사후 만족도 조사 진행")
        elif churn_type == "조용한 이탈(AE)":
            st.info("💤 **비활성 고객:** 재참여 유도 전략 필요")
            st.info("- 리마케팅 이메일, 할인 쿠폰 발송")
            st.info("- 앱 재방문 유도 알림")
        else:
            st.success("✅ **정상 고객:** 장기 유지 중심 전략")
            st.info("- 추천 프로그램 참여 유도")
            st.info("- 멤버십 혜택 확대")