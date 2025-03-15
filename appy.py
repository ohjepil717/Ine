import streamlit as st
import pandas as pd
from datetime import datetime
import io
import re

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
    current_set = {}  # 한 사람의 데이터를 저장

    for line in lines:
        line = line.strip()
        if not line:  # 빈 줄 무시
            continue

        # 새로운 "이름"이 나타나면 이전 세트를 저장하고 새로운 세트 시작
        if "이름:" in line:
            if current_set and "이름" in current_set:  # 이전 세트가 완성된 경우 저장
                categorized_data.append(current_set.copy())
            current_set = {"이름": line.replace("이름:", "").strip()}  # 새로운 세트 시작
        elif "날짜:" in line or "방문 날짜:" in line:
            current_set["날짜"] = line.replace("날짜:", "").replace("방문 날짜:", "").strip()
        elif "가격:" in line:
            current_set["가격"] = line.replace("가격:", "").strip()
        elif "인원수:" in line:
            current_set["인원수"] = line.replace("인원수:", "").strip()
        elif "예약시간:" in line:
            current_set["예약시간"] = line.replace("예약시간:", "").strip()
        elif "방문시간:" in line:
            current_set["방문시간"] = line.replace("방문시간:", "").strip()
        elif "목적/이유:" in line:
            purpose = line.replace("목적/이유:", "").strip()
            valid_purposes = ["방문", "견학", "관광", "모임", "판매", "면접", "점검", "납품", "택배"]
            if purpose not in valid_purposes:
                st.warning(f"유효하지 않은 목적/이유: {purpose}. '없음'으로 설정됩니다.")
            current_set["목적/이유"] = purpose if purpose in valid_purposes else "없음"
        elif "자동차번호:" in line:
            car_number = line.replace("자동차번호:", "").strip()
            # 한국 자동차 번호판 패턴: [0-9]{1,3}[가-힣]{1,2}[0-9]{2,4} (공백 허용)
            if re.match(r'^\d{1,3}[가-힣]{1,2}\s?\d{2,4}$', car_number) or re.match(r'^\d{4}$', car_number):
                current_set["자동차번호"] = car_number
            else:
                current_set["자동차번호"] = "잘못된 형식"

    # 마지막 세트 추가 (이름이 있는 경우에만)
    if current_set and "이름" in current_set and current_set not in categorized_data:
        categorized_data.append(current_set)

    # 기존 데이터와 비교 후 추가
    new_data = [d for d in categorized_data if d not in st.session_state.data_list]
    if new_data:
        st.session_state.data_list.extend(new_data)
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
