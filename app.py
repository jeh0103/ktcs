import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# ==============================
# ⚙️ 한글 폰트 설정 (macOS 포함)
# ==============================
if platform.system() == "Darwin":  # macOS
    plt.rcParams['font.family'] = 'AppleGothic'
elif platform.system() == "Windows":
    plt.rcParams['font.family'] = 'Malgun Gothic'
else:
    plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# -------------------------------
# 1️⃣ 데이터 로드
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("ecommerce_customer_churn_hybrid_with_id.csv")

df = load_data()

# -------------------------------
# 2️⃣ 페이지 구조 (탭 구성)
# -------------------------------
st.set_page_config(page_title="E-commerce Churn Dashboard", layout="wide")
st.title("E-commerce 고객 이탈 예측 통합 대시보드")
tabs = st.tabs(["📊 분석용 대시보드", "🔍 고객별 이탈 예측"])

# =========================================================
# 📊 탭1. 분석용 대시보드
# =========================================================
with tabs[0]:
    st.header("📈 전체 고객 분석 대시보드")
    st.markdown("---")

    # -----------------------------
    # 기본 통계
    # -----------------------------
    col1, col2, col3 = st.columns(3)
    total_customers = len(df)
    churn_if = df['IF_ChurnFlag'].sum()
    churn_ae = df['AE_ChurnFlag'].sum()
    churn_both = df['Both_ChurnFlag'].sum()

    col1.metric("전체 고객 수", f"{total_customers:,}")
    col2.metric("Isolation Forest 이탈 고객 수", f"{churn_if:,}")
    col3.metric("Autoencoder 이탈 고객 수", f"{churn_ae:,}")

    st.metric("공통 이탈 고객 (고신뢰군)", f"{churn_both:,}명 ({round(churn_both/total_customers*100, 2)}%)")

    st.markdown("---")

    # ---------------------------------
    # 🚨 이탈 위험 고객 TOP 10 리스트  ← (이 부분을 위로 이동시킴)
    # ---------------------------------
    st.subheader("🚨 이탈 위험 고객 TOP 10")

    # 이탈 위험 고객 필터링 (두 모델 공통 이탈)
    risky_customers = (
        df[df['Both_ChurnFlag'] == 1]
        .dropna(subset=['CustomerID'])
        .sort_values('ChurnRiskScore', ascending=False)
        .head(10)
        [['CustomerID', 'ChurnRiskScore', 'PurchaseFrequency', 'CSFrequency']]
    )

    # 표 스타일
    st.dataframe(
        risky_customers.style.background_gradient(
            cmap="Reds", subset=['ChurnRiskScore']
        ).format({'ChurnRiskScore': '{:.2f}', 'PurchaseFrequency': '{:.2f}', 'CSFrequency': '{:.2f}'})
    )

    st.caption("※ 상위 10명은 Isolation Forest + Autoencoder 공통으로 '이탈 위험'으로 탐지된 고객입니다.")

    st.markdown("---")

    # ---------------------------------
    # 📊 이탈 고객 비율 분포
    # ---------------------------------
    st.subheader("📊 이탈 고객 비율 분포")

    fig, ax = plt.subplots(figsize=(4,2))
    counts = [
        churn_if/total_customers*100,
        churn_ae/total_customers*100,
        churn_both/total_customers*100
    ]
    models = ["Isolation Forest", "Autoencoder", "Both"]
    sns.barplot(x=models, y=counts, palette="coolwarm", ax=ax)
    ax.set_ylabel("이탈 고객 비율 (%)")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("📦 이탈 고객 주요 변수 비교 (Boxplot)")

    fig, axes = plt.subplots(1, 3, figsize=(9,3))
    sns.boxplot(x='IF_ChurnFlag', y='PurchaseFrequency', data=df, ax=axes[0])
    sns.boxplot(x='IF_ChurnFlag', y='CSFrequency', data=df, ax=axes[1])
    sns.boxplot(x='IF_ChurnFlag', y='ChurnRiskScore', data=df, ax=axes[2])
    axes[0].set_title("월평균 구매 빈도")
    axes[1].set_title("상담 빈도")
    axes[2].set_title("종합 이탈 위험 점수")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("🔥 모델별 상관 분석 Heatmap")

    num_cols = ['PurchaseFrequency','CSFrequency','ChurnRiskScore','CLVPerMonth','RecencyProxy']
    corr = df[num_cols + ['IF_ChurnFlag']].corr()
    fig, ax = plt.subplots(figsize=(5,3))
    sns.heatmap(corr, annot=True, cmap="Blues", ax=ax)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

# =========================================================
# 🔍 탭2. 고객별 예측 조회
# =========================================================
with tabs[1]:
    st.header("🔍 고객 ID 기반 이탈 예측")
    st.markdown("---")

    customer_id = st.text_input("고객 ID를 입력하세요 (예: CUST00010):")

    if customer_id:
        customer = df[df["CustomerID"] == customer_id]

        if customer.empty:
            st.warning("❌ 해당 고객 ID를 찾을 수 없습니다.")
        else:
            row = customer.iloc[0]
            st.subheader(f"📊 [고객 ID: {customer_id}] 예측 결과")

            col1, col2, col3 = st.columns(3)
            col1.metric("Isolation Forest", "이탈 의심" if row["IF_ChurnFlag"]==1 else "정상")
            col2.metric("Autoencoder", "이탈 의심" if row["AE_ChurnFlag"]==1 else "정상")
            col3.metric("공통 판단", "이탈 의심" if row["Both_ChurnFlag"]==1 else "정상")

            st.markdown("---")
            st.write("### 주요 지표")
            st.write(f"- **PurchaseFrequency (구매빈도)**: {row['PurchaseFrequency']:.2f}")
            st.write(f"- **CSFrequency (상담빈도)**: {row['CSFrequency']:.2f}")
            st.write(f"- **ChurnRiskScore (위험점수)**: {row['ChurnRiskScore']:.2f}")
            st.write(f"- **RecencyProxy (활동저하지수)**: {row['RecencyProxy']:.2f}")

            st.markdown("### 🚨 이탈 위험도 게이지")
            risk = min(row['ChurnRiskScore']/2, 1.0)
            st.progress(risk)

            # 판단 메시지
            if row["Both_ChurnFlag"] == 1:
                st.error("🚨 **이 고객은 고신뢰 이탈 고객으로 분류되었습니다. 즉시 케어가 필요합니다.**")
            elif row["IF_ChurnFlag"] == 1:
                st.warning("⚠️ **활동은 많지만 불만이 높은 고객입니다. CS 관리 필요.**")
            elif row["AE_ChurnFlag"] == 1:
                st.info("💤 **조용히 이탈 가능성이 있는 고객입니다. 리마케팅이 필요합니다.**")
            else:
                st.success("✅ **정상 고객으로 분류되었습니다. 유지 관리 대상입니다.**")