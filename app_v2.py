import streamlit as st

st.set_page_config(page_title="결정에도 성격이 있다", layout="centered")

# 문항별 (질문, 해당 성향 축, 높은 응답이 가리키는 방향)
QUESTIONS = [
    ("식당에서 메뉴를 고를 때, 오래 고민하지 않고 빠르게 결정하는 편이다.", 0, "Q"),
    ("쇼핑을 할 때, 마음에 드는 물건을 발견해도 다른 제품과 비교하느라 구매 결정을 미루는 편이다.", 0, "D"),
    ("여가 시간에 무엇을 할지 금방 결정하는 편이다.", 0, "Q"),
    ("물건을 구매할 때, 디자인이나 느낌보다 가격과 성능을 더 중요하게 생각하는 편이다.", 1, "L"),
    ("진로를 고민할 때, 현실적인 조건보다 내가 하고 싶은 일인지를 더 중요하게 생각하는 편이다.", 1, "F"),
    ("여행지를 선택할 때, 여러 여행지의 장단점을 비교한 후 결정하는 편이다.", 1, "L"),
    ("친구들과 메뉴를 고를 때, 내 의견보다 친구들의 의견을 더 따르는 편이다.", 2, "S"),
    ("개인적인 선택을 할 때, 주변 사람들의 의견에 따라 내 생각이 바뀌는 편이다.", 2, "S"),
    ("주변 사람들이 나와 다른 의견을 제시해도 내 생각대로 결정하는 편이다.", 2, "I"),
    ("물건을 구매한 후에도, 다른 제품을 샀으면 더 좋았을지 생각하는 편이다.", 3, "R"),
    ("메뉴를 주문한 후, 다른 메뉴가 더 맛있어 보여도 내 선택에 만족하는 편이다.", 3, "C"),
    ("한 번 내린 결정은 나중에 다시 고민하지 않는 편이다.", 3, "C"),
]

# 결과 문구는 최종 제공된 프롬프트를 기준으로 작성
RESULTS = {
    "QLIC": ("확신의 직진러", "빠르게 상황을 파악하고 논리적으로 결론을 내리는 타입. 남의 말에 쉽게 흔들리지 않고, 한번 결정하면 뒤돌아보지 않아요.", "추진력, 명확한 판단력", "다른 사람의 의견을 놓칠 수 있음", "고민 끝났어. 이게 제일 낫잖아."),
    "QLIR": ("속전속결 뒤끝왕", "결정할 때는 빠르고 계산적이지만, 선택한 뒤에도 다른 가능성을 계속 따져보는 타입.", "빠른 실행력, 사후 점검 능력", "이미 끝난 선택에 에너지를 많이 쓸 수 있음", "그때 그걸 골랐으면 더 이득이었나?"),
    "QLSC": ("효율적인 조율왕", "필요한 정보를 빠르게 정리하고 주변 의견까지 반영해 결론을 내리는 타입. 합리적인 합의가 이루어지면 결과에도 만족해요.", "조율 능력, 효율적인 문제 해결", "빠른 합의를 위해 소수 의견을 놓칠 수 있음", "의견 다 들었지? 그럼 이걸로 가자!"),
    "QLSR": ("초고속 여론탐지기", "판단은 빠르고 논리적이지만, 다른 사람의 반응도 중요하게 생각하는 타입. 결정 후에도 주변 피드백을 확인해요.", "상황 파악, 피드백 수용", "주변 반응에 지나치게 신경 쓸 수 있음", "이게 합리적이긴 한데, 다들 어떻게 생각해?"),
    "QFIC": ("본능형 확신러", "마음이 끌리는 순간 결정을 내리고, 자신의 감각을 믿는 타입. 결과가 조금 아쉬워도 자신의 선택을 존중해요.", "자신감, 직관적인 판단", "중요한 조건을 확인하지 않을 수 있음", "그냥 느낌이 왔어. 난 이거!"),
    "QFIR": ("직감 폭주 후폭풍러", "직감이 오면 누구보다 빠르게 움직이지만, 시간이 지나면 다른 선택지가 떠오르는 타입.", "과감함, 빠른 행동력", "순간의 감정과 사후 고민 사이에서 피로해질 수 있음", "그땐 진짜 이게 맞는 줄 알았지…"),
    "QFSC": ("분위기 타는 행복러", "주변 분위기와 자신의 감각을 따라 빠르게 선택하는 타입. 함께 즐겁게 결정했다면 그걸로 충분해요.", "적응력, 긍정적인 태도", "분위기에 휩쓸려 자신의 취향을 놓칠 수 있음", "다들 좋으면 나도 좋아!"),
    "QFSR": ("선택 후 단톡방 소환러", "느낌과 주변 의견을 따라 빠르게 결정하지만, 선택하고 나면 친구들에게 다시 확인하고 싶은 타입.", "친화력, 공감 능력", "다른 사람의 평가에 쉽게 흔들릴 수 있음", "얘들아, 나 이거 골랐는데 괜찮지?"),
    "DLIC": ("철저한 계획주의자", "정보를 충분히 분석하고 스스로 납득할 때까지 검토하는 타입. 일단 결정하면 계획대로 밀고 나가요.", "체계성, 안정적인 판단", "준비 과정이 길어질 수 있음", "계획대로만 하면 문제없어."),
    "DLIR": ("신중한 무한검증러", "결정하기 전에도 자료를 비교하고, 결정한 뒤에도 빠뜨린 것이 없는지 다시 확인하는 타입.", "꼼꼼함, 위험 발견 능력", "지나친 검토로 결정을 즐기기 어려울 수 있음", "잠깐, 한 번만 더 확인해 보자."),
    "DLSC": ("모두가 납득하는 결정러", "자료를 꼼꼼히 살피면서 여러 사람의 의견도 충분히 듣는 타입. 모두가 이해할 만한 결론을 찾으면 만족해요.", "신뢰감, 균형 잡힌 조정 능력", "합의 과정이 길어질 수 있음", "다 같이 납득할 수 있는 방법을 찾자."),
    "DLSR": ("생각이 많은 완벽주의자", "정보도 비교하고 주변 의견도 수렴하지만, 결정 후에도 더 좋은 답이 있었을지 고민하는 타입.", "세심함, 다양한 관점의 고려", "완벽한 답을 찾느라 지칠 수 있음", "좋은 선택인 건 알겠는데, 최선이었을까?"),
    "DFIC": ("조용한 소신파", "충분히 고민하지만 최종 판단에서는 자신의 마음을 중요하게 생각하는 타입. 결정한 뒤에는 자기 선택을 믿어요.", "진정성, 흔들리지 않는 가치관", "객관적인 조건을 덜 고려할 수 있음", "오래 생각했어. 내 마음은 이거야."),
    "DFIR": ("마음속 무한 시뮬레이터", "마음이 원하는 선택을 신중하게 고민하지만, 결정한 후에도 여러 가능성을 머릿속으로 다시 그려보는 타입.", "깊은 자기성찰, 풍부한 상상력", "지나간 선택에 대한 미련이 길어질 수 있음", "만약 그때 다른 걸 골랐다면 어땠을까?"),
    "DFSC": ("신중한 공감요정", "자신의 감정뿐 아니라 다른 사람의 마음도 살피며 천천히 결정하는 타입. 모두가 편안한 선택을 했다면 만족해요.", "배려심, 공감 능력", "타인을 배려하다 자신의 욕구를 뒤로 미룰 수 있음", "나는 괜찮은데 너희는 진짜 괜찮아?"),
    "DFSR": ("고민이 취미인 공감러", "자신과 주변 사람들의 감정을 모두 고려하다 보니 결정이 쉽지 않은 타입. 선택 후에도 누군가 아쉬워하지 않을지 신경 써요.", "세심한 배려, 감정 이해력", "다른 사람의 감정까지 책임지려 할 수 있음", "다 괜찮다고 했는데… 정말 괜찮은 거겠지?"),
}

AXES = [("결정 속도", "Q", "D", "빠른 결정", "신중한 결정"),
        ("판단 근거", "L", "F", "논리·정보", "감정·직감"),
        ("타인 영향", "I", "S", "독립 결정", "의견 반영"),
        ("선택 후 태도", "C", "R", "선택 만족", "선택 고민")]
OPTIONS = ["전혀 그렇지 않다", "그렇지 않은 편이다", "그런 편이다", "매우 그렇다"]

st.markdown("""<style>
.stApp {background:linear-gradient(160deg,#f7f1ff 0%,#fdfaff 55%,#f2edff 100%);color:#302445}
.block-container {max-width:1050px;padding-top:2rem;padding-bottom:3rem}
h1,h2,h3 {color:#50387e!important}
.hero {background:linear-gradient(120deg,#e4d4ff,#f4e9ff);padding:30px 26px;border-radius:24px;text-align:center;margin-bottom:22px;border:1px solid #dac7f7}
.hero h1 {font-size:2.2rem;line-height:1.2;margin:0 0 .55rem;padding:0;word-break:keep-all}
.hero p {margin:0;color:#54436c;font-size:1.08rem;line-height:1.45;white-space:nowrap}
[class*="st-key-question-card-"] {
  background:#fff;border:1px solid #e2d5f1;border-radius:18px;padding:1.2rem 1.3rem;
  box-shadow:0 3px 12px #6c4a9a0d;
}
[class*="st-key-question-card-"] .num {font-size:.82rem;color:#6b4c8d;font-weight:700}
[class*="st-key-question-card-"] .q {font-size:1.15rem;line-height:1.5;color:#33254b;font-weight:700;margin-top:.35rem}
.result-card {background:#fff;color:#302445;border:1px solid #e4d4f5;border-radius:22px;padding:25px;margin:16px 0;box-shadow:0 5px 20px #6c4a9a12}
.quote {background:#f5edff;border-radius:12px;padding:15px;color:#60458b;font-style:italic}
[class*="st-key-question-card-"] [data-testid="stRadio"] {width:100% !important}
[class*="st-key-question-card-"] [role="radiogroup"] {
  display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.6rem;width:100%;
}
[class*="st-key-question-card-"] [role="radiogroup"] > label {
  min-width:0;min-height:3.25rem;margin:0;padding:.55rem .65rem;
  border:1px solid #e4d7f3;border-radius:10px;background:#faf6ff;
  box-sizing:border-box;cursor:pointer;
}
[class*="st-key-question-card-"] [role="radiogroup"] > label:hover {background:#f1e8fc}
[class*="st-key-question-card-"] [role="radiogroup"] > label:has(input:checked) {
  background:#ede1ff;border-color:#7956b4;
}
[class*="st-key-question-card-"] [role="radiogroup"] > label:has(input:focus-visible) {
  outline:2px solid #7956b4;outline-offset:2px;
}
[class*="st-key-question-card-"] [role="radiogroup"] > label,
[class*="st-key-question-card-"] [role="radiogroup"] > label p {
  color:#2c2040 !important;font-size:1.08rem !important;font-weight:650;
  line-height:1.35;word-break:keep-all;overflow-wrap:anywhere;
}
@media (max-width:760px) {
  [class*="st-key-question-card-"] [role="radiogroup"] {grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width:480px) {
  .block-container {padding-left:1rem;padding-right:1rem}
  .hero {padding:24px 8px}
  .hero h1 {font-size:1.65rem}
  .hero p {font-size:clamp(.65rem,3.3vw,.98rem)}
  [class*="st-key-question-card-"] {padding:.85rem}
  [class*="st-key-question-card-"] .q {font-size:1.05rem}
  [class*="st-key-question-card-"] [role="radiogroup"] > label {padding:.45rem}
  [class*="st-key-question-card-"] [role="radiogroup"] > label,
  [class*="st-key-question-card-"] [role="radiogroup"] > label p {font-size:1rem !important}
}
div[data-testid="stButton"] button {background:#7956b4;color:white;border-radius:12px;border:0;font-weight:700;padding:11px 24px}
div[data-testid="stButton"] button:hover {background:#62449c;color:white}
</style>""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>결정에도 성격이 있다</h1><p>12가지 질문으로 알아보는 나의 의사결정 유형</p></div>', unsafe_allow_html=True)

if "show_result" not in st.session_state:
    st.session_state.show_result = False

# 다시 검사하기: 라디오 응답을 완전히 초기화
if st.session_state.show_result:
    scores = [0, 0, 0, 0]
    for idx, (_, axis, positive) in enumerate(QUESTIONS):
        selected = st.session_state[f"answer_{idx}"]
        value = OPTIONS.index(selected) + 1
        scores[axis] += value if positive == AXES[axis][1] else 5 - value  # 4점 척도 역채점

    code = "".join(AXES[i][1] if score >= 8 else AXES[i][2] for i, score in enumerate(scores))
    name, desc, strength, caution, quote = RESULTS[code]
    st.success("테스트 완료! 나의 의사결정 유형을 확인해 보세요.")
    st.markdown(f'<div class="result-card"><div style="color:#8c6aaf;font-weight:700">나의 유형 · {code}</div><h2 style="margin:8px 0 16px">{name}</h2><p>{desc}</p><p>✨ <b>장점:</b> {strength}</p><p>🔎 <b>주의할 점:</b> {caution}</p><div class="quote">“{quote}”</div></div>', unsafe_allow_html=True)

    st.subheader("📊 나의 4가지 의사결정 성향")
    st.caption("각 축은 3~12점입니다. 8점 이상은 왼쪽 성향, 7점 이하는 오른쪽 성향으로 분류합니다.")
    for i, (axis_name, left_code, right_code, left_label, right_label) in enumerate(AXES):
        # 3점 -> 0%, 12점 -> 100%로 환산해 왼쪽 성향의 강도를 표시
        percentage = round((scores[i] - 3) / 9 * 100)
        st.markdown(f"**{axis_name}** · {left_code if scores[i] >= 8 else right_code}형 ({scores[i]}/12점)")
        st.progress(percentage, text=f"{left_label}  ←  {percentage}%  →  {right_label}")
    st.caption("이 테스트는 자기이해를 위한 간단한 유형 분류이며, 표준화된 심리검사는 아닙니다.")

    if st.button("🔄 다시 검사하기", use_container_width=True):
        for idx in range(len(QUESTIONS)):
            st.session_state.pop(f"answer_{idx}", None)
        st.session_state.show_result = False
        st.rerun()
else:
    st.write("평소 자신의 모습과 가장 가까운 답을 하나씩 골라주세요. 정답은 없어요!")
    answered = sum(st.session_state.get(f"answer_{idx}") is not None for idx in range(len(QUESTIONS)))
    st.progress(answered / len(QUESTIONS), text=f"응답 진행률: {answered} / {len(QUESTIONS)}문항 ({answered / len(QUESTIONS):.0%})")

    for idx, (question, _, _) in enumerate(QUESTIONS):
        with st.container(key=f"question-card-{idx}"):
            st.markdown(
                f'<div class="num">QUESTION {idx + 1:02d} / 12</div><div class="q">{question}</div>',
                unsafe_allow_html=True,
            )
            # index=None으로 시작해 실제 미응답과 선택 상태를 구분
            st.radio(
                question,
                OPTIONS,
                index=None,
                key=f"answer_{idx}",
                label_visibility="collapsed",
                horizontal=True,
            )

    answered = sum(st.session_state.get(f"answer_{idx}") is not None for idx in range(len(QUESTIONS)))
    st.progress(answered / len(QUESTIONS), text=f"현재 완료: {answered} / {len(QUESTIONS)}문항")
    if st.button("✨ 내 의사결정 유형 확인하기", disabled=answered != len(QUESTIONS), use_container_width=True):
        st.session_state.show_result = True
        st.rerun()
    if answered < len(QUESTIONS):
        st.caption(f"결과를 보려면 남은 {len(QUESTIONS)-answered}문항에 답해주세요.")
