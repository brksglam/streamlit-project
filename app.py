import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os
from datetime import datetime
from pymongo import MongoClient

# ============================================================
# PAGE CONFIG & SETUP
# ============================================================
st.set_page_config(
    page_title="AGD | Yatırım Mühendisliği",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS ARCHITECTURE (SENIOR++ VISUALS)
# ============================================================
st.markdown("""
<style>
    /* === FONT IMPORT === */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* === GLOBAL RESET === */
    *, html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }
    
    /* === STREAMLIT CLEANUP === */
    #MainMenu, footer, header, .stDeployButton, [data-testid="stDecoration"], [data-testid="stToolbar"] {
        display: none !important;
    }
    
    /* === MAIN THEME === */
    .main {
        background-color: #0E1117 !important; /* Dark Mode Core */
        color: #FFFFFF !important;
    }
    
    .block-container {
        padding: 2rem 1rem !important;
        max-width: 900px !important;
    }

    /* === HEADER === */
    .app-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 2rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 3rem;
    }
    
    .brand-logo {
        font-size: 1.2rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.02em;
        text-transform: uppercase;
    }
    
    .brand-tag {
        font-size: 0.75rem;
        color: rgba(255,255,255,0.5);
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* === WIZARD CARDS (STEP 0) === */
    .wizard-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2.5rem;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        cursor: pointer;
        text-align: left;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .wizard-card:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.3);
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
    
    .wizard-card h3 {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: white;
    }
    
    .wizard-card p {
        font-size: 0.95rem;
        color: rgba(255,255,255,0.6);
        line-height: 1.5;
    }
    
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        display: block;
    }

    /* === FORM ELEMENTS === */
    .stButton > button {
        width: 100%;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        transition: all 0.2s ease !important;
        border: none !important;
    }
    
    /* Primary Action */
    .primary-btn > button {
        background: white !important;
        color: black !important;
    }
    .primary-btn > button:hover {
        background: #e0e0e0 !important;
        transform: scale(1.02);
    }

    /* Secondary Action */
    .secondary-btn > button {
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    .secondary-btn > button:hover {
        background: rgba(255,255,255,0.2) !important;
    }

    /* Inputs */
    .stTextInput input, .stSelectbox, .stNumberInput input {
        background-color: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: white !important;
        border-radius: 10px !important;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: white !important;
        box-shadow: 0 0 0 1px white !important;
    }
    
    /* Admin Table */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# MONGODB CONNECTION
# ============================================================
MONGO_URI = "mongodb+srv://buraksaglam415_db_user:jnIC2z40mFDD8rqh@cluster0.swtf7ev.mongodb.net/?appName=Cluster0"

@st.cache_resource
def get_db():
    try:
        client = MongoClient(MONGO_URI)
        db = client["agd_investment"]
        return db
    except:
        return None

def save_lead(name, phone, note, intent, city=None, budget=None):
    try:
        db = get_db()
        if db:
            # Capture Source Ref
            params = st.query_params
            ref = params.get("ref", "direct")
            
            db.leads.insert_one({
                "name": name,
                "phone": phone,
                "note": note,
                "intent": intent,
                "city": city,
                "budget": budget,
                "source": ref,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "status": "new"
            })
        return True
    except:
        return False

def get_all_leads():
    try:
        db = get_db()
        if db:
            return list(db.leads.find().sort("_id", -1))
        return []
    except:
        return []

# ============================================================
# STATE MANAGEMENT
# ============================================================
if 'step' not in st.session_state:
    st.session_state.step = 'init'
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'admin_auth' not in st.session_state:
    st.session_state.admin_auth = False

def set_step(new_step):
    st.session_state.step = new_step
    st.rerun()

def go_back():
    current = st.session_state.step
    if current.startswith('tr_'):
        if current == 'tr_1': set_step('init')
        elif current == 'tr_2': set_step('tr_1')
        elif current == 'tr_3': set_step('tr_2')
    elif current.startswith('cy_'):
        if current == 'cy_1': set_step('init')
        elif current == 'cy_2': set_step('cy_1')
        elif current == 'cy_3': set_step('cy_2')

# ============================================================
# SCREENS
# ============================================================
def render_header():
    st.markdown("""
    <div class="app-header">
        <div>
            <div class="brand-logo">AGD | YATIRIM MÜHENDİSLİĞİ</div>
            <div class="brand-tag">Premium Real Estate Solutions</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def screen_init():
    st.markdown("<h1 style='font-size: 2.8rem; text-align: center; margin-bottom: 0.5rem;'>Bugünkü Hedefiniz?</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.6); margin-bottom: 3rem;'>Size en uygun çözümü sunmak için lütfen bir seçim yapın.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        # Türkiye Card
        st.markdown("""
        <div class="wizard-card">
            <span class="card-icon">🇹🇷</span>
            <h3>Türkiye Operasyonları</h3>
            <p>İstanbul, Kocaeli veya Ankara'da Gayrimenkul Alım/Satım işlemleri.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("Türkiye İşlemleri →", key="btn_tr"):
            st.session_state.user_data['flow'] = 'TR'
            set_step('tr_1')
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # KKTC Card
        st.markdown("""
        <div class="wizard-card">
            <span class="card-icon">🌍</span>
            <h3>Global Yatırım (Döviz)</h3>
            <p>Enflasyondan korunma, Sterlin (GBP) geliri ve yüksek ROI fırsatları.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("Yatırım Simülasyonu →", key="btn_cy"):
            st.session_state.user_data['flow'] = 'CY'
            set_step('cy_1')
        st.markdown('</div>', unsafe_allow_html=True)

# === TÜRKİYE FLOW ===
def screen_tr_1():
    st.markdown("### İşlem Türünüz?")
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        if st.button("🏠 Mülk Satmak İstiyorum", key="tr_sell", use_container_width=True):
            st.session_state.user_data['tr_action'] = 'Satış'
            set_step('tr_2')
    with col2:
        if st.button("🔑 Mülk Almak İstiyorum", key="tr_buy", use_container_width=True):
            st.session_state.user_data['tr_action'] = 'Alış'
            set_step('tr_2')
    st.markdown("---")
    if st.button("← Geri Dön", on_click=go_back): pass

def screen_tr_2():
    action = st.session_state.user_data.get('tr_action', 'İşlem')
    st.markdown(f"### {action} için Gayrimenkul Tipi?")
    opts = ["Konut (Daire/Villa)", "Arsa / Arazi", "Ticari Mülk"]
    selection = st.radio("", opts, label_visibility="collapsed")
    if st.button("Devam Et →", key="tr_2_next", type="primary"):
        st.session_state.user_data['tr_type'] = selection
        set_step('tr_3')
    st.markdown("---")
    if st.button("← Geri Dön", key="back_tr2", on_click=go_back): pass

def screen_tr_3():
    st.markdown("### Son Adım: Uzmanımız Sizi Arasın")
    st.info(f"Talebiniz: {st.session_state.user_data.get('tr_action')} - {st.session_state.user_data.get('tr_type')}")
    with st.form("tr_final_form"):
        col1, col2 = st.columns(2)
        with col1:
            city = st.text_input("Şehir / İlçe", placeholder="Örn: İstanbul, Pendik")
            price = st.text_input("Tahmini Bedel / Bütçe", placeholder="Opsiyonel")
        with col2:
            name = st.text_input("Adınız Soyadınız")
            phone = st.text_input("Telefon Numaranız", placeholder="05XX...")
        submitted = st.form_submit_button("Talebi Gönder →", type="primary")
        if submitted:
            if not name or not phone:
                st.error("Lütfen İsim ve Telefon alanlarını doldurun.")
            else:
                intent_code = f"TR_{st.session_state.user_data.get('tr_action').upper()}_{st.session_state.user_data.get('tr_type')}"
                note = f"{intent_code} | Yer: {city}"
                save_lead(name, phone, note, intent_code, city=city, budget=price)
                set_step('success')
    st.markdown("---")
    if st.button("← Geri Dön", key="back_tr3", on_click=go_back): pass

# === KKTC (CY) FLOW ===
def screen_cy_1():
    st.markdown("### Varlık Koruma Analizi")
    st.markdown("Paranızın enflasyon karşısında nasıl eridiğini (veya KKTC'de nasıl değerlendiğini) görün.")
    budget = st.number_input("Yatırım Bütçeniz (TL)", min_value=100000, value=5000000, step=100000)
    if st.button("Simülasyonu Çalıştır →", type="primary"):
        st.session_state.user_data['budget'] = budget
        set_step('cy_2')
    st.markdown("---")
    if st.button("← Geri Dön", key="back_cy1", on_click=go_back): pass

def screen_cy_2():
    st.markdown("### Finansal Projeksiyon (10 Yıl)")
    budget = st.session_state.user_data.get('budget', 5000000)
    years = list(range(2026, 2037))
    tl_power = [budget * (0.65 ** i) for i in range(11)] 
    gbp_val = [budget * 1.5 * (1.12 ** i) for i in range(11)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=tl_power, name='TL Alım Gücü (Türkiye)', 
                             line=dict(color='#ef4444', width=3), fill='tozeroy'))
    fig.add_trace(go.Scatter(x=years, y=gbp_val, name='GBP Varlık Değeri (KKTC)', 
                             line=dict(color='#22c55e', width=3), fill='tonexty'))
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.05)',
        height=350,
        margin=dict(l=0,r=0,t=20,b=20),
        legend=dict(orientation="h", y=1.1)
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div style='background:rgba(239,68,68,0.1); border:1px solid #ef4444; padding:1rem; border-radius:10px; text-align:center;'>
            <div style='color:#ef4444; font-weight:bold;'>TL ERİMESİ</div>
            <div style='font-size:1.2rem;'>📉 %{int((1-(tl_power[-1]/budget))*100)} Kayıp</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div style='background:rgba(34,197,94,0.1); border:1px solid #22c55e; padding:1rem; border-radius:10px; text-align:center;'>
            <div style='color:#22c55e; font-weight:bold;'>DÖVİZ KAZANCI</div>
            <div style='font-size:1.2rem;'>🚀 {int(gbp_val[-1]/budget)}x Katlama</div>
        </div>""", unsafe_allow_html=True)

    st.plotly_chart(fig, use_container_width=True)
    if st.button("Fırsatları Göster →", type="primary"):
        set_step('cy_3')
    st.markdown("---")
    if st.button("← Geri Dön", key="back_cy2", on_click=go_back): pass

def screen_cy_3():
    st.markdown("### Size Özel High-Yield Fırsatlar")
    st.markdown("""
    <div style="background: rgba(255,255,255,0.05); border-radius: 15px; padding: 1.5rem; margin-bottom: 1rem;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div><h3 style="margin:0;">K-Island Garden</h3><p style="margin:0; font-size:0.9rem;">Tatlısu, North Cyprus</p></div>
            <div style="text-align:right;"><div style="font-size:1.4rem; font-weight:800;">£138,000</div><div style="color:#22c55e;">ROI: 7 Yıl</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.info("Bu projelerin resmi ödeme planlarını ve kira getiri tablolarını almak için formu doldurun.")
    with st.form("cy_final_form"):
        col1, col2 = st.columns(2)
        with col1: name = st.text_input("Adınız Soyadınız")
        with col2: phone = st.text_input("Telefon Numaranız")
        submitted = st.form_submit_button("Detaylı Dosyayı İste →", type="primary")
        if submitted:
            if not name or not phone:
                st.error("Eksik bilgi.")
            else:
                budget = st.session_state.user_data.get('budget', 0)
                save_lead(name, phone, "KKTC Yatırım Raporu Talebi", "CY_INVEST", budget=budget)
                set_step('success')
    st.markdown("---")
    if st.button("← Geri Dön", key="back_cy3", on_click=go_back): pass

def screen_success():
    st.balloons()
    st.markdown("""
    <div style="text-align: center; padding: 4rem 1rem;">
        <div style="font-size: 5rem; margin-bottom: 1rem;">✅</div>
        <h1 style="color: white;">Talebiniz Alındı!</h1>
        <p style="font-size: 1.2rem; color: rgba(255,255,255,0.7);">
            Uzman ekibimiz 24 saat içinde sizinle iletişime geçecektir.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ana Sayfaya Dön"):
        st.session_state.user_data = {}
        set_step('init')

# ============================================================
# ADMIN PANEL
# ============================================================
def admin_screen():
    st.markdown("## 🔐 Admin Dashboard")
    
    if not st.session_state.admin_auth:
        pwd = st.text_input("Admin Şifresi", type="password")
        if st.button("Giriş Yap"):
            if pwd == "AGD2026":
                st.session_state.admin_auth = True
                st.rerun()
            else:
                st.error("Hatalı Şifre")
    else:
        leads = get_all_leads()
        st.success(f"Toplam Lead Sayısı: {len(leads)}")
        
        if leads:
            df = pd.DataFrame(leads)
            # Cleanup id for display
            if '_id' in df.columns: del df['_id']
            
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv().encode('utf-8')
            st.download_button("CSV İndir", csv, "leads.csv", "text/csv")
        
        if st.button("Çıkış"):
            st.session_state.admin_auth = False
            st.rerun()

# ============================================================
# MAIN
# ============================================================
def main():
    # Admin Route check
    params = st.query_params
    if "admin" in params:
        admin_screen()
        return

    render_header()
    step = st.session_state.step
    
    if step == 'init': screen_init()
    elif step == 'tr_1': screen_tr_1()
    elif step == 'tr_2': screen_tr_2()
    elif step == 'tr_3': screen_tr_3()
    elif step == 'cy_1': screen_cy_1()
    elif step == 'cy_2': screen_cy_2()
    elif step == 'cy_3': screen_cy_3()
    elif step == 'success': screen_success()

if __name__ == "__main__":
    main()
