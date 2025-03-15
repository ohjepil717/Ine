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

# 메모 입력 및 실시간 분류
st.session_state.memo_text = st.text_area("여기에 메모를 입력하세요:", value=st.session_state.memo_text, height=200, key="memo_input")

# 실시간 분류 로직
if st.session_state.memo_text:
    categorized_data = []
    lines = st.session_state.memo_text.split("\n")
    names = []  # 이름 중복 체크용 리스트
    current_set = {}  # 한 사람의 데이터를 저장

    for line in lines:
        line = line.strip()
        if not line:  # 빈 줄 무시
            continue

        # 새로운 "이름"이 나타나면 이전 세트를 저장하고 새로운 세트 시작
        if "이름:" in line:
            if current_set:  # 이전 세트가 있으면 저장
                categorized_data.append(current_set.copy())
            current_set = {}  # 새로운 세트 초기화
            name = line.replace("이름:", "").strip()
            if name in names:
                st.warning(f"중복된 이름 '{name}'이 발견되었습니다!")
                choice = st.selectbox(f"'{name}'을(를) 사용하시겠습니까?", ["무시", "사용"], key=f"dup_{name}")
                if choice == "사용":
                    current_set["이름"] = name
            else:
                names.append(name)
                current_set["이름"] = name
        elif "날짜:" in line:
            current_set["날짜"] = line.replace("날짜:", "").strip()
        elif "가격:" in line:
            current_set["가격"] = line.replace("가격:", "").strip()
        elif "인원수:" in line:
            current_set["인원수"] = line.replace("인원수:", "").strip()
        elif "예약시간:" in line:
            current_set["예약시간"] = line.replace("예약시간:", "").strip()
        elif "방문시간:" in line:
            current_set["방문시간"] = line.replace("방문시간:", "").strip()
        elif "방문목적:" in line:
            current_set["방문목적"] = line.replace("방문목적:", "").strip()

    # 마지막 세트 추가
    if current_set and current_set not in categorized_data:
        categorized_data.append(current_set)

    # 기존 데이터와 비교 후 추가
    st.session_state.data_list = []
    for data in categorized_data:
        if data not in st.session_state.data_list:
            st.session_state.data_list.append(data)
    st.success("데이터가 실시간으로 분류되었습니다!")

# 데이터 표시
if st.session_state.data_list:
    st.subheader("분류된 데이터 목록")
    df = pd.DataFrame(st.session_state.data_list)
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

# 메모 지우기 (메모장만 지우기)
if st.button("메모 지우기"):
    st.session_state.memo_text = ""
    st.experimental_rerun()  # 페이지를 새로고침하여 UI 업데이트
    st.warning("메모장이 지워졌습니다.")

# 분류 데이터 삭제 (분류된 데이터만 지우기)
if st.button("분류 데이터 삭제"):
    st.session_state.data_list.clear()
    st.experimental_rerun()  # 페이지를 새로고침하여 UI 업데이트
    st.warning("분류된 데이터가 삭제되었습니다.")
