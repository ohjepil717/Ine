import streamlit as st
import pandas as pd
import re

# 목적/이유 선택 옵션
purpose_options = ["방문", "견학", "관광", "모임", "판매", "면접", "점검", "납품", "택배"]

# 메모장 입력
memo = st.text_area("메모장", height=200)

# 메모장 내용 분류 함수
def classify_memo(memo):
    data = []
    lines = memo.split("\n")
    for line in lines:
        line = line.strip()
        if line:
            item = {}
            # 목적/이유 추출
            for option in purpose_options:
                if option in line:
                    item["목적/이유"] = option
                    break
            # 자동차 번호 추출
            car_match = re.search(r"(\d{2}[가-힣]\d{4})", line)
            if car_match:
                item["자동차번호"] = car_match.group(1)
            # 이름 추출
            name_match = re.search(r"이름:\s*(\S+)", line)
            if name_match:
                item["이름"] = name_match.group(1)
            # 방문 날짜 추출
            date_match = re.search(r"방문 날짜:\s*(\d{4}-\d{2}-\d{2})", line)
            if date_match:
                item["날짜"] = date_match.group(1)
            # 가격 추출
            price_match = re.search(r"가격:\s*([\d,]+원)", line)
            if price_match:
                item["가격"] = price_match.group(1)
            # 인원수 추출
            person_match = re.search(r"인원수:\s*(\d+명)", line)
            if person_match:
                item["인원수"] = person_match.group(1)
            data.append(item)
    return pd.DataFrame(data)

# 데이터 분류 및 표시
if memo:
    df = classify_memo(memo)
    st.write("데이터가 실시간으로 분류되었습니다!")
    st.write("분류된 데이터 목록")
    st.dataframe(df)

    # 엑셀로 저장 버튼
    if st.button("엑셀로 저장"):
        df.to_excel("data.xlsx", index=False)
        st.success("엑셀 파일이 저장되었습니다.")

# 메모장 지우기 버튼
if st.button("메모장 지우기"):
    st.text_area("메모장", value="", height=200)

# Streamlit 앱 실행
if __name__ == "__main__":
    st.set_page_config(page_title="메모 분류 앱")
