import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title="Supermarket Sales Dashboard", layout="wide")
st.title("🏬 지점별 매출 분석 대시보드")

# 2. 데이터 불러오기
@st.cache_data
def load_data():
    # Sales.xlsx의 supermarket_sales_test 시트 로드 후 결측치 제거
    df = pd.read_excel("Sales.xlsx", sheet_name="supermarket_sales_test")
    df = df.dropna()
    return df

try:
    df = load_data()

    # 3. 사이드바 - 지점(Branch) 선택 필터
    st.sidebar.header("필터 옵션")
    branches = sorted(df["Branch"].unique())
    selected_branch = st.sidebar.selectbox("지점(Branch)을 선택하세요:", branches)

    # 선택한 지점으로 데이터 필터링
    filtered_df = df[df["Branch"] == selected_branch]

    # 4. KPI 지표 (metric) 계산
    total_sales = filtered_df["Total"].sum()
    avg_sales = filtered_df["Total"].mean()
    avg_rating = filtered_df["Rating"].mean()

    # KPI 지표 화면 표시
    col1, col2, col3 = st.columns(3)
    col1.metric(label="총 매출 (Total Sales)", value=f"${total_sales:,.2f}")
    col2.metric(label="평균 매출 (Average Sales)", value=f"${avg_sales:,.2f}")
    col3.metric(label="평균 평점 (Average Rating)", value=f"{avg_rating:.2f} / 10")

    st.markdown("---")

    # 5. 상품 카테고리(Product line)별 평균 매출 계산 및 막대그래프 시각화
    st.subheader(f"📊 {selected_branch} 지점 - 상품 카테고리별 평균 매출")
    category_avg = filtered_df.groupby("Product line")["Total"].mean().reset_index()
    category_avg = category_avg.sort_values(by="Total", ascending=False)

    fig = px.bar(
        category_avg,
        x="Product line",
        y="Total",
        text_auto=".2s",
        labels={"Total": "평균 매출 ($)", "Product line": "상품 카테고리"},
        color="Total",
        color_continuous_scale="Blues"
    )
    fig.update_layout(xaxis_title="상품 카테고리", yaxis_title="평균 매출 ($)")
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"데이터를 로드하는 과정에서 오류가 발생했습니다: {e}")
