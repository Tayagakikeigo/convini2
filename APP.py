import streamlit as st
import datetime
import time
import pandas as pd

# --- Streamlitページ設定 ---
# st.set_page_configは、stコマンドが呼ばれる前に一度だけ設定する必要があります。
st.set_page_config(layout="wide", page_title="店舗経営ダッシュボード")

# --- カスタムCSS ---
# HTML要素に適用されるスタイルを定義します。
st.markdown("""
<style>
    .stApp {
        background-color: #f0f2f6; /* 全体の背景色 */
    }
    .alert-custom-blue {
        background-color: #e0f7fa; /* 薄いシアン */
        border-left: 6px solid #00bcd4; /* シアンの左ボーダー */
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .alert-title {
        font-weight: bold;
        color: #00796b; /* 濃いシアン */
        font-size: 1.1em;
        margin-bottom: 5px;
    }
    .alert-description {
        color: #333;
        font-size: 0.95em;
    }
    .important-metric-card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        text-align: center;
        height: 100%; /* カードの高さを揃える */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .important-metric-card h3 {
        color: #4CAF50; /* 緑 */
        margin-top: 0;
        font-size: 1.3em;
    }
    .important-metric-card p {
        margin: 5px 0;
        color: #555;
    }
    .important-metric-card .amount {
        font-size: 1.8em;
        font-weight: bold;
        color: #2196F3; /* 青 */
        margin-top: 15px;
    }
    .management-advice-card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .management-advice-card ul {
        list-style-type: disc; /* リストのスタイル */
        padding-left: 20px;
        margin: 0;
    }
    .management-advice-card li {
        margin-bottom: 8px;
        color: #444;
    }
    .card-container {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: auto; /* 高さを自動調整 */
    }
    .metric-label {
        font-size: 0.9em;
        color: #777;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 1.5em;
        font-weight: bold;
        color: #E91E63; /* ピンク */
    }
    .card-header {
        font-size: 1.1em;
        font-weight: bold;
        color: #3F51B5; /* インディゴ */
        margin-bottom: 10px;
    }
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        border: 1px solid #ddd;
        background-color: #f8f8f8;
        color: #333;
        padding: 8px 12px;
        font-size: 0.9em;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .stButton > button:hover {
        background-color: #e0e0e0;
        border-color: #ccc;
    }
    /* Streamlitのメインコンテンツブロックにパディングを追加 */
    .st-emotion-cache-10trblm {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    /* カラム間のギャップを調整 */
    .st-emotion-cache-1c7y2kd {
        gap: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- ダミーデータ (実際のデータに置き換えてください) ---
order_qty = 1500
sell_through_rate = 0.85
avg_price = 250
sales_amount = order_qty * sell_through_rate * avg_price

inventory_rate = 0.10
avg_inv_price = 200
inventory_amount = order_qty * inventory_rate * avg_inv_price

disposal_rate = 0.05
avg_disposal_price = 100
disposal_amount = order_qty * disposal_rate * avg_disposal_price

data = [    {"label": "売上高", "value": 325000},    {"label": "客単価", "value": 750},    {"label": "来店客数", "value": 433},    {"label": "粗利率", "value": 0.35},    {"label": "廃棄率", "value": 0.05},    {"label": "在庫回転率", "value": 12.5},]

sales_data = pd.DataFrame({
    "day": ["月", "火", "水", "木", "金", "土", "日"],
    "sales": [15000, 18000, 16000, 20000, 25000, 35000, 30000]
})

hourly_visitors = pd.DataFrame({
    "hour": [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    "visitors": [10, 25, 40, 60, 80, 75, 65, 50, 45, 55, 70, 60, 30]
})

shift_plan = [    {"time": "8:00-12:00", "staff": 2},    {"time": "12:00-17:00", "staff": 3},    {"time": "17:00-21:00", "staff": 2},]

trends = [    "観光客によるお土産需要が増加中",    "健康志向の高まりでサラダ・惣菜が人気",    "キャッシュレス決済の利用率が上昇",]

events = [    "8/12 〇〇小学校運動会 (近隣)",    "8/15 地域のお祭り (徒歩5分)",    "8/20 花火大会 (バスで15分)",]

product_ordering_plan = [    {"category": "飲料", "recommendation": "スポーツドリンク、お茶", "reason": "夏場の需要増"},    {"category": "菓子", "recommendation": "個包装のお土産品", "reason": "観光客向け"},    {"category": "日配品", "recommendation": "牛乳、パン", "reason": "定番品は欠品注意"},]

hot_snack_preparation = [    {"item": "フライドチキン", "times": ["11:30", "17:00"]},
    {"item": "アメリカンドッグ", "times": ["12:00", "18:00"]},
    {"item": "肉まん", "times": ["10:00", "16:00"]},
]

time_based_recommendation = """
【午前中 (8:00-11:00)】
・出勤前のビジネスパーソン向けに、コーヒー、パン、おにぎりなどの朝食セットをレジ横に配置。
・観光客向けに、地域限定のお土産品や軽食を入口付近に展開。

【ランチタイム (11:00-14:00)】
・弁当、サンドイッチ、惣菜の品揃えを強化し、温かいスープや味噌汁とセットで提案。
・ホットスナックの揚げたて提供をアピール。

【午後 (14:00-17:00)】
・おやつ需要に対応し、スイーツ、アイスクリーム、スナック菓子を目立つ場所に。
・観光客の休憩需要を見込み、イートインスペースの清掃と快適性を維持。

【夕方以降 (17:00-21:00)】
・夕食の準備に便利な惣菜、冷凍食品、アルコール飲料の品揃えを充実。
・仕事帰りのビジネスパーソン向けに、割引商品やセット販売を提案。
"""

# --- Streamlit アプリケーションのレイアウト ---

st.title("店舗経営ダッシュボード")

# 地域イベント速報
st.markdown("""
    <div class="alert-custom-blue">
        <div class="alert-title">🔔 地域イベント速報</div>
        <div class="alert-description">8/12 〇〇小学校運動会。発注強化推奨。</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 重要指標の分解図
st.markdown("## 重要指標の分解図")
col_sales, col_inventory, col_disposal = st.columns(3)

with col_sales:
    st.markdown(f"""
    <div class="important-metric-card">
        <h3>売上額</h3>
        <p>商品発注数: {order_qty}個</p>
        <p>販売率: {(sell_through_rate * 100):.1f}%</p>
        <p>平均単価: {avg_price}円</p>
        <p class="amount">→ {sales_amount:,}円</p>
    </div>
    """, unsafe_allow_html=True)

with col_inventory:
    st.markdown(f"""
    <div class="important-metric-card">
        <h3>在庫額</h3>
        <p>商品発注数: {order_qty}個</p>
        <p>在庫率: {(inventory_rate * 100):.1f}%</p>
        <p>在庫単価: {avg_inv_price}円</p>
        <p class="amount">→ {inventory_amount:,}円</p>
    </div>
    """, unsafe_allow_html=True)

with col_disposal:
    st.markdown(f"""
    <div class="important-metric-card">
        <h3>廃棄額</h3>
        <p>商品発注数: {order_qty}個</p>
        <p>廃棄率: {(disposal_rate * 100):.1f}%</p>
        <p>廃棄単価: {avg_disposal_price}円</p>
        <p class="amount">→ {disposal_amount:,}円</p>
    </div>
    """, unsafe_allow_html=True)

# 経営の視点でのアドバイス
st.markdown("## 経営の視点でのアドバイス")
st.markdown("""
<div class="management-advice-card">
    <ul class="list-style-disc">
        <li>高粗利商品の販売促進とコスト最適化を継続的に実施。</li>
        <li>時間帯別・イベント別の陳列戦略で客単価向上を図る。</li>
        <li>発注計画精度向上で欠品と廃棄を両立。</li>
        <li>来店予測に基づくシフト最適化で人件費管理。</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 主要指標 (Key Metrics)
st.markdown("## 主要指標")
cols_metrics = st.columns(3) # 1行に3つのカードを配置
for i, item in enumerate(data):
    with cols_metrics[i % 3]: # カラムを循環して配置
        st.markdown(f"""
        <div class="card-container">
            <div class="metric-label">{item['label']}</div>
            <div class="metric-value">{item['value']:,}</div>
        </div>
        """, unsafe_allow_html=True)
        if "廃棄率" in item['label']:
            # Streamlitのprogressバーは0-100の整数を期待
            st.progress(int(item['value'] * 100))

st.markdown("---")

# チャートセクション
st.markdown("## 分析チャート")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("<div class='card-container'><div class='card-header'>週間売上推移</div>", unsafe_allow_html=True)
    st.line_chart(sales_data, x="day", y="sales")
    st.markdown("</div>", unsafe_allow_html=True) # card-containerの閉じタグ

with chart_col2:
    st.markdown("<div class='card-container'><div class='card-header'>時間帯別来店客数予測</div>", unsafe_allow_html=True)
    st.line_chart(hourly_visitors, x="hour", y="visitors")
    st.markdown("</div>", unsafe_allow_html=True) # card-containerの閉じタグ

st.markdown("---")

# インサイトと計画
st.markdown("## インサイトと計画")
insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    st.markdown("<div class='card-container'><div class='card-header'>シフト計画</div>", unsafe_allow_html=True)
    st.markdown(f"""
        <ul class="list-style-disc">
            {"".join([f"<li>{s['time']}: 店員 {s['staff']}人</li>" for s in shift_plan])}
        </ul>
    </div>
    """, unsafe_allow_html=True)

with insight_col2:
    st.markdown("<div class='card-container'><div class='card-header'>現在のトレンド</div>", unsafe_allow_html=True)
    st.markdown(f"""
        <ul class="list-style-disc">
            {"".join([f"<li>{t}</li>" for t in trends])}
        </ul>
    </div>
    """, unsafe_allow_html=True)

with insight_col3:
    st.markdown("<div class='card-container'><div class='card-header'>地域イベント情報</div>", unsafe_allow_html=True)
    st.markdown(f"""
        <ul class="list-style-disc">
            {"".join([f"<li>{e}</li>" for e in events])}
        </ul>
    </div>
    """, unsafe_allow_html=True)

# 商品発注計画とホットスナック仕込み時間
plan_col1, plan_col2 = st.columns(2)

with plan_col1:
    st.markdown("<div class='card-container'><div class='card-header'>商品発注計画</div>", unsafe_allow_html=True)
    st.markdown(f"""
        <ul class="list-style-disc">
            {"".join([f"<li><strong>{p['category']}</strong>: {p['recommendation']} ({p['reason']})</li>" for p in product_ordering_plan])}
        </ul>
    </div>
    """, unsafe_allow_html=True)

with plan_col2:
    st.markdown("<div class='card-container'><div class='card-header'>ホットスナック仕込み時間</div>", unsafe_allow_html=True)
    st.markdown(f"""
        <ul class="list-style-disc">
            {"".join([f"<li><strong>{h['item']}</strong>: {', '.join(h['times'])}</li>" for h in hot_snack_preparation])}
        </ul>
    </div>
    """, unsafe_allow_html=True)

# 時間帯別商品推奨
st.markdown("## 時間帯別商品推奨")
st.markdown(f"""
<div class="card-container">
    <p style="white-space: pre-wrap; font-size: 0.9em;">{time_based_recommendation}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# AIアシスタントチャット
st.markdown("## 🤖 AIアシスタント")

# チャット履歴の初期化
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# チャットメッセージの表示
chat_container = st.container(height=300, border=True)
with chat_container:
    for msg in st.session_state.chat_log:
        with st.chat_message(msg["role"]):
            st.write(msg["text"])
            st.caption(msg["time"]) # 時刻表示

# チャット入力
chat_input = st.chat_input("質問を入力...")

if chat_input:
    # ユーザーメッセージを履歴に追加
    st.session_state.chat_log.append({"role": "user", "text": chat_input, "time": datetime.datetime.now().strftime("%H:%M")})
    # ユーザーメッセージを即座に表示するために再実行
    st.rerun()

# ボットの応答生成 (最後のメッセージがユーザーからの場合のみ)
if st.session_state.chat_log and st.session_state.chat_log[-1]["role"] == "user":
    user_message = st.session_state.chat_log[-1]["text"].lower()
    
    with st.chat_message("assistant"):
        with st.spinner("考え中..."):
            time.sleep(1.2) # タイピングの遅延をシミュレート
            response = "経営全般に関するアドバイスをご希望ですか？もう少し具体的に教えてください。"
            if "売上" in user_message or "利益" in user_message:
                response = "売上を上げるには、観光客需要を意識した季節商品とお土産品の導入が効果的です。また、客単価を上げるためにセット販売や高単価商品の陳列を工夫しましょう。"
            elif "sns" in user_message or "トレンド" in user_message or "イベント" in user_message:
                response = "沖縄限定グッズやご当地グルメ関連商品がSNS映えし、話題性につながります。地域イベントと連動したキャンペーンも効果的です。"
            elif "発注" in user_message or "在庫" in user_message:
                response = "発注計画は、過去の販売データと天気予報、地域イベント情報を総合的に考慮して最適化しましょう。特に廃棄率と品切れ率のバランスが重要です。"
            elif "ホットスナック" in user_message or "仕込み" in user_message:
                response = "ホットスナックはピークタイムに合わせて仕込み時間を調整し、常に新鮮な商品を提供できるよう心がけましょう。特にランチタイムと夕食時に需要が高まります。"
            
            st.write(response)
            st.caption(datetime.datetime.now().strftime("%H:%M"))
            # ボットの応答を履歴に追加
            st.session_state.chat_log.append({"role": "assistant", "text": response, "time": datetime.datetime.now().strftime("%H:%M")})
            # チャット履歴の更新を反映するために再実行
            st.rerun()

# チャットの提案ボタン
st.markdown("### よくある質問")
chat_suggestions = [    "売上を上げるには？",    "おすすめ商品は？",    "イベント活用方法は？",    "SNSで話題になるには？",    "発注計画について",    "ホットスナックの仕込みは？"]

cols_suggestions = st.columns(3) # ボタンを3列に配置
for i, suggestion in enumerate(chat_suggestions):
    with cols_suggestions[i % 3]:
        if st.button(suggestion, key=f"suggestion_{i}"):
            st.session_state.chat_log.append({"role": "user", "text": suggestion, "time": datetime.datetime.now().strftime("%H:%M")})
            st.rerun()
