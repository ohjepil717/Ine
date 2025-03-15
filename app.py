import streamlit as st
import pandas as pd
from datetime import datetime
import io

# 세션 상태 초기화
if "data_list" not in st.session_state:
    st.session_state.data_list = []
if "memo_text" not in st.session_state:
    st.session_state.memo_text = ""

# 앱 UI
st.title("메모 분류 및 저장")

# 메모 입력
st.session_state.memo_text = st.text_area("여기에 메모를 입력하세요:", value=st.session_state.memo_text)

# 분류 버튼
if st.button("분류하기"):
    categorized_data = []
    lines = st.session_state.memo_text.split("\n")

    for line in lines:
        if "날짜" in line:
            categorized_data.append(("날짜", line.replace("날짜:", "").strip()))
        elif "이름" in line:
            categorized_data.append(("이름", line.replace("이름:", "").strip()))
        elif "가격" in line:
            categorized_data.append(("가격", line.replace("가격:", "").strip()))
        elif "인원수" in line:
            categorized_data.append(("인원수", line.replace("인원수:", "").strip()))
        elif "예약시간" in line:
            categorized_data.append(("예약시간", line.replace("예약시간:", "").strip()))
        elif "방문시간" in line:
            categorized_data.append(("방문시간", line.replace("방문시간:", "").strip()))
        elif "방문목적" in line:
            categorized_data.append(("방문목적", line.replace("방문목적:", "").strip()))

    # 데이터 저장
    if categorized_data:
        st.session_state.data_list.append(categorized_data)
        st.success("데이터가 분류되었습니다!")

# 데이터 표시
if st.session_state.data_list:
    st.subheader("분류된 데이터 목록")
    df = pd.DataFrame([dict(data) for data in st.session_state.data_list])
    st.dataframe(df)

    # 엑셀 다운로드 버튼
    if st.button("엑셀로 저장"):
        filename = f"memo_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False, engine="openpyxl")
        buffer.seek(0)
        st.download_button(
            label="엑셀 파일 다운로드",
            data=buffer,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        st.success(f"엑셀 파일이 준비되었습니다: {filename}")

# 메모 삭제 버튼
if st.button("메모 지우기"):
    st.session_state.memo_text = ""
    st.session_state.data_list.clear()
    st.warning("메모가 삭제되었습니다.")
