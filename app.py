import streamlit as st
import plotly.graph_objects as go
import csv
import os
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="AGD | Yatırım Mühendisliği",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# SESSION STATE
# ============================================================
if 'lang' not in st.session_state:
    st.session_state.lang = 'TR'

# ============================================================
# CSS MİMARİSİ (GÖRSEL DEVRİM)
# ============================================================
st.markdown("""
<style>
    /* === FONT IMPORT === */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* === GLOBAL RESET === */
    *, html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }
    
    /* === STREAMLIT TEMİZLİĞİ === */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    
    /* === BODY === */
    .main {
        background-color: #FFFFFF !important;
    }
    
    .block-container {
        padding: 1.5rem 2rem 3rem 2rem !important;
        max-width: 1100px !important;
    }
    
    /* === HEADER BAR === */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid #f0f0f0;
        margin-bottom: 2rem;
    }
    
    .brand-section h1 {
        font-size: 1.5rem;
        font-weight: 800;
        color: #0E1117;
        margin: 0;
        letter-spacing: -0.03em;
    }
    
    .brand-section p {
        font-size: 0.8rem;
        color: #888;
        margin: 4px 0 0 0;
        font-weight: 500;
    }
    
    .lang-pills {
        display: flex;
        background: #f5f5f5;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #e8e8e8;
    }
    
    .lang-pill {
        padding: 8px 18px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #666;
        background: transparent;
        border: none;
        cursor: pointer;
        transition: all 0.15s ease;
    }
    
    .lang-pill:hover {
        background: #e0e0e0;
    }
    
    .lang-pill.active {
        background: #0E1117;
        color: white;
    }
    
    /* === HERO SECTION === */
    .hero-box {
        background: linear-gradient(135deg, #fafafa 0%, #ffffff 100%);
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 2.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 1.5rem;
    }
    
    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        color: #0E1117;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.03em;
    }
    
    .hero-subtitle {
        font-size: 1rem;
        color: #666;
        margin: 0;
    }
    
    /* === SONUÇ KARTLARI === */
    .result-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    @media (max-width: 768px) {
        .result-row {
            grid-template-columns: 1fr;
        }
    }
    
    .result-box {
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid;
    }
    
    .result-box.loss {
        background: linear-gradient(180deg, #fff5f5 0%, #fee2e2 100%);
        border-color: #fecaca;
    }
    
    .result-box.gain {
        background: linear-gradient(180deg, #f0fdf4 0%, #dcfce7 100%);
        border-color: #bbf7d0;
    }
    
    .result-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .result-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.75rem;
    }
    
    .result-box.loss .result-label { color: #b91c1c; }
    .result-box.gain .result-label { color: #15803d; }
    
    .result-amount {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .result-box.loss .result-amount { color: #dc2626; }
    .result-box.gain .result-amount { color: #16a34a; }
    
    .result-desc {
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .result-box.loss .result-desc { color: #991b1b; }
    .result-box.gain .result-desc { color: #166534; }
    
    /* === SECTION HEADERS === */
    .section-title {
        font-size: 1.6rem;
        font-weight: 800;
        color: #0E1117;
        margin: 2.5rem 0 0.5rem 0;
        letter-spacing: -0.02em;
    }
    
    .section-desc {
        font-size: 0.95rem;
        color: #666;
        margin: 0 0 1.5rem 0;
    }
    
    /* === PROPERTY CARDS === */
    .prop-card {
        background: #FFFFFF;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.75rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    
    .prop-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        border-color: #0E1117;
    }
    
    .prop-badge {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 5px 10px;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    
    .badge-fire { background: #fef3c7; color: #b45309; }
    .badge-gem { background: #dbeafe; color: #1d4ed8; }
    .badge-star { background: #f3e8ff; color: #7c3aed; }
    
    .prop-row {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
    }
    
    .prop-name {
        font-size: 1.3rem;
        font-weight: 700;
        color: #0E1117;
        margin: 0 0 4px 0;
    }
    
    .prop-loc {
        font-size: 0.9rem;
        color: #888;
        margin: 0;
    }
    
    .prop-price {
        font-size: 1.6rem;
        font-weight: 800;
        color: #0E1117;
    }
    
    .yield-tag {
        display: inline-block;
        background: #ecfdf5;
        color: #059669;
        font-size: 0.8rem;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 20px;
        margin-top: 1rem;
    }
    
    /* === AUTHORITY SECTION === */
    .authority-bar {
        background: linear-gradient(135deg, #0E1117 0%, #1a1a2e 100%);
        border-radius: 12px;
        padding: 2.5rem;
        margin-top: 3rem;
    }
    
    .authority-inner {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1.5rem;
    }
    
    .authority-info h3 {
        color: white;
        font-size: 1.4rem;
        font-weight: 800;
        margin: 0 0 6px 0;
    }
    
    .authority-info .title {
        color: #94a3b8;
        font-size: 1rem;
        margin: 0 0 4px 0;
    }
    
    .authority-info .loc {
        color: #64748b;
        font-size: 0.9rem;
        margin: 0;
    }
    
    .authority-btns {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
    }
    
    .auth-link {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 12px 20px;
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 8px;
        color: white;
        font-size: 0.9rem;
        font-weight: 600;
        text-decoration: none;
        transition: all 0.2s ease;
    }
    
    .auth-link:hover {
        background: rgba(255,255,255,0.2);
        color: white;
        text-decoration: none;
    }
    
    /* === BUTTONS === */
    .stButton > button {
        background: #0E1117 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.9rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background: #1a1a2e !important;
        box-shadow: 0 4px 12px rgba(14,17,23,0.3) !important;
    }
    
    /* === INPUT === */
    .stNumberInput input {
        border-radius: 10px !important;
        border: 1px solid #e0e0e0 !important;
        padding: 0.8rem 1rem !important;
    }
    
    .stNumberInput input:focus {
        border-color: #0E1117 !important;
        box-shadow: 0 0 0 2px rgba(14,17,23,0.1) !important;
    }
    
    /* === FOOTER === */
    .site-footer {
        text-align: center;
        padding: 2.5rem 0 1rem 0;
        color: #aaa;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DİL SÖZLÜĞÜ
# ============================================================
LANG = {
    "TR": {
        "brand": "AGD | YATIRIM MÜHENDİSLİĞİ",
        "hq": "HQ: Marmara Kule, Kartal / İstanbul",
        "hero_title": "Varlık Koruma Simülasyonu",
        "hero_sub": "10 yıllık sermaye projeksiyon analizi",
        "budget": "Yatırım Sermayesi (TL)",
        "analyze": "Simülasyonu Başlat",
        "loss_label": "Türkiye Senaryosu",
        "loss_desc": "Enflasyon karşısında değer kaybı",
        "gain_label": "Kıbrıs Senaryosu",
        "gain_desc": "Sterlin bazlı değer artışı",
        "port_title": "Algoritmik Eşleşme Portföyü",
        "port_sub": "Yüksek performans potansiyelli varlıklar",
        "cta": "Yatırım Raporunu İste",
        "broker_title": "Veri Odaklı Gayrimenkul Danışmanı",
        "btn_wa": "WhatsApp",
        "btn_li": "LinkedIn",
        "btn_map": "Ofis Konumu",
        "form_name": "Ad Soyad",
        "form_phone": "Telefon",
        "form_submit": "Gönder",
        "form_ok": "Talebiniz alındı.",
        "badge_fire": "🔥 Çok Talep Görüyor",
        "badge_gem": "💎 Fırsat Ürünü",
        "badge_star": "⭐ Nadir Lokasyon",
        "yield_lbl": "Yıllık Getiri",
    },
    "EN": {
        "brand": "AGD | INVESTMENT ENGINEERING",
        "hq": "HQ: Marmara Tower, Kartal / Istanbul",
        "hero_title": "Asset Protection Simulation",
        "hero_sub": "10-year capital projection analysis",
        "budget": "Investment Capital (TRY)",
        "analyze": "Run Simulation",
        "loss_label": "Turkey Scenario",
        "loss_desc": "Value depreciation vs inflation",
        "gain_label": "Cyprus Scenario",
        "gain_desc": "Sterling-based appreciation",
        "port_title": "Algorithmic Match Portfolio",
        "port_sub": "High-performance potential assets",
        "cta": "Request Investment Report",
        "broker_title": "Data-Driven Real Estate Advisor",
        "btn_wa": "WhatsApp",
        "btn_li": "LinkedIn",
        "btn_map": "Office",
        "form_name": "Full Name",
        "form_phone": "Phone",
        "form_submit": "Submit",
        "form_ok": "Request received.",
        "badge_fire": "🔥 High Demand",
        "badge_gem": "💎 Opportunity",
        "badge_star": "⭐ Rare Location",
        "yield_lbl": "Annual Yield",
    },
    "AR": {
        "brand": "AGD | هندسة الاستثمار",
        "hq": "المقر: برج مرمرة، كارتال / إسطنبول",
        "hero_title": "محاكاة حماية الأصول",
        "hero_sub": "تحليل توقعات رأس المال لمدة 10 سنوات",
        "budget": "رأس المال (ليرة)",
        "analyze": "بدء المحاكاة",
        "loss_label": "سيناريو تركيا",
        "loss_desc": "انخفاض القيمة مقابل التضخم",
        "gain_label": "سيناريو قبرص",
        "gain_desc": "ارتفاع قائم على الإسترليني",
        "port_title": "محفظة المطابقة الخوارزمية",
        "port_sub": "أصول ذات إمكانات أداء عالية",
        "cta": "طلب تقرير الاستثمار",
        "broker_title": "مستشار عقاري قائم على البيانات",
        "btn_wa": "واتساب",
        "btn_li": "لينكدإن",
        "btn_map": "المكتب",
        "form_name": "الاسم",
        "form_phone": "الهاتف",
        "form_submit": "إرسال",
        "form_ok": "تم استلام الطلب.",
        "badge_fire": "🔥 طلب عالي",
        "badge_gem": "💎 فرصة",
        "badge_star": "⭐ موقع نادر",
        "yield_lbl": "العائد السنوي",
    }
}

# ============================================================
# PROPERTY DATA
# ============================================================
PROPERTIES = [
    {"id": "thalassa", "name": "Thalassa Studio", "price": 95000, "loc": "Bafra, NC", "yield": "8.2%", "badge": "gem"},
    {"id": "k_garden", "name": "K-Island Garden", "price": 138000, "loc": "Tatlısu, NC", "yield": "7.5%", "badge": "fire"},
    {"id": "west_one", "name": "West One 2+1", "price": 210000, "loc": "Kyrenia, NC", "yield": "9.1%", "badge": "fire"},
    {"id": "karpasia", "name": "Karpasia Elite", "price": 275000, "loc": "Karpaz, NC", "yield": "6.8%", "badge": "star"},
    {"id": "k_villa", "name": "K-Island Villa", "price": 385000, "loc": "Tatlısu, NC", "yield": "7.2%", "badge": "star"},
]

# ============================================================
# MONGODB CONNECTION
# ============================================================
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://buraksaglam415_db_user:jnIC2z40mFDD8rqh@cluster0.swtf7ev.mongodb.net/?appName=Cluster0"

@st.cache_resource
def get_db():
    """Get MongoDB connection (cached)"""
    try:
        client = MongoClient(MONGO_URI)
        db = client["agd_investment"]
        return db
    except:
        return None

# ============================================================
# HELPERS
# ============================================================
def save_lead(name, phone, note):
    """Save lead to MongoDB"""
    try:
        db = get_db()
        if db:
            db.leads.insert_one({
                "name": name,
                "phone": phone,
                "note": note,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "status": "new"
            })
        return True
    except:
        return False

def get_all_leads():
    """Get all leads from MongoDB"""
    try:
        db = get_db()
        if db:
            return list(db.leads.find().sort("_id", -1))
        return []
    except:
        return []

# ============================================================
# ADMIN PANEL
# ============================================================
def admin_panel():
    """Password-protected admin panel"""
    st.title("🔐 Admin Panel")
    
    # Check if already authenticated
    if st.session_state.get("admin_auth", False):
        st.success("✅ Giriş yapıldı")
        
        # Show leads
        st.subheader("📋 Tüm Lead'ler")
        leads = get_all_leads()
        
        if leads:
            for lead in leads:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{lead.get('name', 'N/A')}**")
                        st.write(f"📞 {lead.get('phone', 'N/A')}")
                        st.write(f"📝 {lead.get('note', 'N/A')}")
                    with col2:
                        st.write(f"🕐 {lead.get('timestamp', 'N/A')}")
            
            st.info(f"Toplam: {len(leads)} lead")
        else:
            st.warning("Henüz lead yok")
        
        if st.button("Çıkış Yap"):
            st.session_state.admin_auth = False
            st.rerun()
    else:
        # Login form
        password = st.text_input("Şifre", type="password")
        if st.button("Giriş"):
            if password == "AGD2026":
                st.session_state.admin_auth = True
                st.rerun()
            else:
                st.error("❌ Yanlış şifre")

# ============================================================
# MAIN APP
# ============================================================
def main():
    # === ADMIN ROUTING ===
    if "admin" in st.query_params:
        admin_panel()
        return
    
    # Check query params for language change
    if "lang" in st.query_params:
        new_lang = st.query_params["lang"]
        if new_lang in ["TR", "EN", "AR"]:
            st.session_state.lang = new_lang
    
    T = LANG[st.session_state.lang]
    
    # === HEADER WITH CLICKABLE LANG PILLS ===
    st.markdown(f"""
    <div class="header-container">
        <div class="brand-section">
            <h1>{T['brand']}</h1>
            <p>{T['hq']}</p>
        </div>
        <div class="lang-pills">
            <a href="?lang=TR" class="lang-pill {'active' if st.session_state.lang=='TR' else ''}" style="text-decoration:none;">TR</a>
            <a href="?lang=EN" class="lang-pill {'active' if st.session_state.lang=='EN' else ''}" style="text-decoration:none;">EN</a>
            <a href="?lang=AR" class="lang-pill {'active' if st.session_state.lang=='AR' else ''}" style="text-decoration:none;">AR</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # === HERO SECTION ===
    st.markdown(f"""
    <div class="hero-box">
        <h1 class="hero-title">{T['hero_title']}</h1>
        <p class="hero-subtitle">{T['hero_sub']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Budget Input
    budget = st.number_input(T['budget'], min_value=1000000, max_value=100000000, value=10000000, step=1000000, format="%d")
    
    if st.button(T['analyze'], use_container_width=True):
        # Calculations
        years = list(range(2026, 2037))
        tl = [budget * (0.85 ** i) for i in range(11)]
        gbp = [budget * 1.8 * (1.10 ** i) for i in range(11)]
        loss = budget - tl[-1]
        gain = gbp[-1] - (budget * 1.8)
        
        # Result Cards
        st.markdown(f"""
        <div class="result-row">
            <div class="result-box loss">
                <div class="result-icon">📉</div>
                <div class="result-label">{T['loss_label']}</div>
                <div class="result-amount">-{loss:,.0f} TL</div>
                <div class="result-desc">{T['loss_desc']}</div>
            </div>
            <div class="result-box gain">
                <div class="result-icon">🚀</div>
                <div class="result-label">{T['gain_label']}</div>
                <div class="result-amount">+{gain:,.0f} TL</div>
                <div class="result-desc">{T['gain_desc']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Plotly Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=years, y=tl,
            mode='lines',
            name='Turkey (TRY)',
            fill='tozeroy',
            line=dict(color='#dc2626', width=2, shape='spline'),
            fillcolor='rgba(220, 38, 38, 0.1)'
        ))
        fig.add_trace(go.Scatter(
            x=years, y=gbp,
            mode='lines',
            name='Cyprus (GBP)',
            fill='tozeroy',
            line=dict(color='#16a34a', width=2, shape='spline'),
            fillcolor='rgba(22, 163, 74, 0.1)'
        ))
        fig.update_layout(
            template="plotly_white",
            height=380,
            margin=dict(l=0, r=0, t=30, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            font=dict(family="Inter, sans-serif")
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # === PORTFOLIO SECTION ===
    st.markdown(f"""
    <h2 class="section-title">{T['port_title']}</h2>
    <p class="section-desc">{T['port_sub']}</p>
    """, unsafe_allow_html=True)
    
    for prop in PROPERTIES:
        badge_class = f"badge-{prop['badge']}"
        badge_text = T[f"badge_{prop['badge']}"]
        
        st.markdown(f"""
        <div class="prop-card">
            <span class="prop-badge {badge_class}">{badge_text}</span>
            <div class="prop-row">
                <div>
                    <h3 class="prop-name">{prop['name']}</h3>
                    <p class="prop-loc">{prop['loc']}</p>
                </div>
                <div class="prop-price">£{prop['price']:,}</div>
            </div>
            <span class="yield-tag">{T['yield_lbl']}: {prop['yield']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(T['cta'], key=f"cta_{prop['id']}", use_container_width=True):
            with st.form(key=f"form_{prop['id']}"):
                st.write(f"**{prop['name']}**")
                name = st.text_input(T['form_name'])
                phone = st.text_input(T['form_phone'])
                submitted = st.form_submit_button(T['form_submit'])
                if submitted and name and phone:
                    save_lead(name, phone, prop['name'])
                    st.success(T['form_ok'])
    
    # === AUTHORITY SECTION ===
    st.markdown(f"""
    <div class="authority-bar">
        <div class="authority-inner">
            <div class="authority-info">
                <h3>Burak Sağlam</h3>
                <p class="title">{T['broker_title']}</p>
                <p class="loc">Marmara Kule, Kartal / İstanbul</p>
            </div>
            <div class="authority-btns">
                <a href="https://wa.me/905064201248" class="auth-link" target="_blank">💬 {T['btn_wa']}</a>
                <a href="https://linkedin.com" class="auth-link" target="_blank">🔗 {T['btn_li']}</a>
                <a href="https://maps.google.com" class="auth-link" target="_blank">📍 {T['btn_map']}</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="site-footer">
        AGD Investment © 2026 | Tüm hakları saklıdır
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
