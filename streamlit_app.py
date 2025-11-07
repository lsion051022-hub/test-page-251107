import streamlit as st
import random
import time
import pandas as pd


st.set_page_config(page_title="주사위 굴리기", page_icon="🎲")

st.title("� 간단한 주사위 굴리기 앱")

st.markdown("주사위 개수와 면 수를 선택한 뒤 `굴리기` 버튼을 눌러 보세요.")

with st.sidebar:
    st.header("설정")
    num_dice = st.slider("주사위 개수", min_value=1, max_value=10, value=2)
    sides = st.selectbox("면 수 (한 주사위) ", options=[4, 6, 8, 10, 12, 20, 100], index=1)
    keep_history = st.checkbox("히스토리 저장", value=True)


def roll_dice(n, s):
    return [random.randint(1, s) for _ in range(n)]


if "history" not in st.session_state:
    st.session_state.history = []

col1, col2 = st.columns([2, 1])

with col1:
    if st.button("굴리기 🎲"):
        results = roll_dice(num_dice, sides)
        total = sum(results)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # 표시
        st.subheader("결과")
        # 한 줄에 주사위들을 보여주기
        faces = []
        for r in results:
            if 1 <= r <= 6:
                # 유니코드 주사위 1-6 (U+2680 .. U+2685)
                faces.append(chr(0x2680 + (r - 1)))
            else:
                faces.append(f"{r} 🎲")

        st.write(" ".join(faces))
        st.info(f"총합: {total}")

        # 히스토리 저장
        if keep_history:
            st.session_state.history.insert(0, {"time": timestamp, "results": results, "total": total})

        # 분포 차트
        try:
            df = pd.DataFrame({'value': results})
            st.bar_chart(df['value'].value_counts().sort_index())
        except Exception:
            # pandas/plotting에 이상이 있으면 건너뜀
            pass

with col2:
    st.write("")
    st.write("")
    if st.button("히스토리 초기화"):  # 초기화 버튼
        st.session_state.history = []

    st.markdown("---")
    st.subheader("최근 굴림 히스토리")
    if len(st.session_state.history) == 0:
        st.write("아직 기록이 없습니다. '히스토리 저장'을 켜고 굴려보세요.")
    else:
        for entry in st.session_state.history[:20]:
            t = entry['time']
            results = entry['results']
            total = entry['total']
            st.write(f"**{t}** — 결과: {results}  → 총합: {total}")

    st.markdown("---")
    st.caption("간단한 주사위 굴리기 앱입니다. 필요하면 기능을 더 추가할게요.")

