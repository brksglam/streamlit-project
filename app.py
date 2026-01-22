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
    
    /* === AUTHORITY SECTION (PREMIUM) === */
    .authority-bar {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        border: 1px solid #312e81;
        border-radius: 16px;
        padding: 3rem;
        margin-top: 4rem;
        box-shadow: 0 10px 40px -10px rgba(30, 27, 75, 0.4);
        position: relative;
        overflow: hidden;
    }

    /* Decorative background blur */
    .authority-bar::before {
        content: '';
        position: absolute;
        top: 0; right: 0;
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, rgba(0,0,0,0) 70%);
        pointer-events: none;
    }
    
    .authority-inner {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 2rem;
        position: relative;
        z-index: 1;
    }
    
    .authority-info h3 {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0 0 8px 0;
        letter-spacing: -0.02em;
        background: linear-gradient(to right, #fff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .authority-info .title {
        color: #818cf8; /* Soft Indigo */
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0 0 8px 0;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    
    .authority-info .loc {
        color: #94a3b8;
        font-size: 0.95rem;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .authority-btns {
        display: flex;
        gap: 16px;
        flex-wrap: wrap;
    }
    
    /* Modern Glass Buttons */
    .auth-link {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        padding: 14px 24px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: #e2e8f0;
        font-size: 0.95rem;
        font-weight: 600;
        text-decoration: none !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(5px);
    }
    
    .auth-link:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
        color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }

    /* Specific Button Styles */
    .auth-link.whatsapp {
        background: rgba(34, 197, 94, 0.1);
        border-color: rgba(34, 197, 94, 0.2);
        color: #4ade80;
    }
    .auth-link.whatsapp:hover {
        background: rgba(34, 197, 94, 0.2);
        border-color: #4ade80;
        color: #ffffff;
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.3);
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
        padding: 3rem 0;
        color: #94a3b8;
        font-size: 0.85rem;
        display: flex;
        flex-direction: column;
        gap: 12px;
        align-items: center;
    }
    
    .footer-divider {
        width: 60px;
        height: 2px;
        background: #e2e8f0;
        margin: 0 auto;
        border-radius: 2px;
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
        "form_email": "E-Posta (Tercihen)",
        "form_submit": "Gönder",
        "form_ok": "Talebiniz alındı.",
        "form_warning": "Lütfen en az bir iletişim bilgisi (Telefon veya E-Posta) giriniz.",
        "form_phone_err": "Telefon numarası çok uzun. Lütfen kontrol ediniz.",
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
        "form_email": "E-Mail (Optional)",
        "form_submit": "Submit",
        "form_ok": "Request received.",
        "form_warning": "Please provide at least one contact method (Phone or Email).",
        "form_phone_err": "Phone number is too long.",
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
        "form_email": "البريد الإلكتروني",
        "form_submit": "إرسال",
        "form_ok": "تم استلام الطلب.",
        "form_warning": "يرجى تقديم وسيلة اتصال واحدة على الأقل.",
        "form_phone_err": "رقم الهاتف طويل جدا.",
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
try:
    from pymongo import MongoClient
    from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
    import certifi
except ImportError:
    # Graceful fallback if libraries are missing (should not happen with requirements.txt)
    MongoClient = None
    certifi = None

MONGO_URI = "mongodb+srv://buraksaglam415_db_user:jnIC2z40mFDD8rqh@cluster0.swtf7ev.mongodb.net/?appName=Cluster0"

# ============================================================
# DATABASE MANAGER (MONGODB + LOCAL FALLBACK)
# ============================================================
import json
import os

# Global variable to track connection status
if 'db_status' not in st.session_state:
    st.session_state.db_status = "unknown"

@st.cache_resource
def get_db_client():
    """
    Attempts to connect to MongoDB with multiple strategies.
    Returns (client, db, 'online') if successful.
    Returns (None, None, 'offline') if failed.
    """
    if MongoClient is None:
        return None, None, 'offline'

    # Strategy 1: Standard Secure (Best Practice)
    try:
        client = MongoClient(
            MONGO_URI, 
            tlsCAFile=certifi.where() if certifi else None, 
            serverSelectionTimeoutMS=2000,
            connectTimeoutMS=2000,
            socketTimeoutMS=2000
        )
        # Force a connection check
        client.admin.command('ping')
        return client, client["agd_investment"], 'online'
    except Exception as e:
        print(f"Strategy 1 Failed: {e}")

    # Strategy 2: Aggressive Fallback (No Verify - useful for restrictive networks)
    try:
        client = MongoClient(
            MONGO_URI, 
            tls=True, 
            tlsAllowInvalidCertificates=True, 
            serverSelectionTimeoutMS=2000,
            connectTimeoutMS=2000
        )
        client.admin.command('ping')
        return client, client["agd_investment"], 'online'
    except Exception as e:
        print(f"Strategy 2 Failed: {e}")
    
    # Strategy 3: Offline Mode
    return None, None, 'offline'

def save_lead(name, phone, email, note):
    """
    Save lead with GUARANTEED persistence.
    1. Try Online DB.
    2. If fails, write to Local CSV.
    3. Never show 'DB Error' to user, just 'Saved'.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 1. Attempt Online Save
    try:
        client, db, status = get_db_client()
        st.session_state.db_status = status
        
        if status == 'online' and db is not None:
            db.leads.insert_one({
                "name": name,
                "phone": phone,
                "email": email,
                "note": note,
                "timestamp": timestamp,
                "status": "new"
            })
            return True, "online"
    except Exception as e:
        print(f"Online Save Failed: {e}")
        # Continue to offline backup immediately

    # 2. Offline Fallback (Guaranteed)
    try:
        file_path = "local_leads.csv"
        file_exists = os.path.isfile(file_path)
        
        with open(file_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                # Add header if new file (Updated with Email)
                writer.writerow(["name", "phone", "email", "note", "timestamp", "status", "source"])
            
            # Write data (Updated with Email)
            writer.writerow([name, phone, email, note, timestamp, "new_offline", "CSV_BACKUP"])
            
        return True, "offline"
    except Exception as e:
        print(f"CRITICAL: Link Save Failed completely: {e}")
        # This is the only time we might return False, but practically CSV write shouldn't fail
        return False, "error"

def get_all_leads():
    """Get leads from MongoDB AND Local CSV merged"""
    all_leads = []
    
    # 1. Fetch Online Leads
    try:
        client, db, status = get_db_client()
        if status == 'online' and db is not None:
            online_leads = list(db.leads.find().sort("_id", -1))
            all_leads.extend(online_leads)
    except Exception as e:
        print(f"Fetch Online Failed: {e}")
            
    # 2. Fetch Offline Leads
    if os.path.isfile("local_leads.csv"):
        try:
            with open("local_leads.csv", "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                offline_leads = list(reader)
                # Ensure source is marked
                for lead in offline_leads:
                    if 'source' not in lead:
                        lead['source'] = 'OFFLINE (Yerel)'
                all_leads.extend(offline_leads)
        except Exception as e:
            print(f"Fetch CSV Failed: {e}")
            
    # Remove duplicates if needed (optional logic, but simplistic for now)
    # Convert all to list and sort by timestamp if possible
    try:
        all_leads.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    except:
        pass
        
    return all_leads

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
                        if lead.get('email'):
                            st.write(f"📧 {lead.get('email', '')}")
                        st.write(f"📝 {lead.get('note', 'N/A')}")
                    with col2:
                        st.write(f"🕐 {lead.get('timestamp', 'N/A')}")
            
            st.info(f"Toplam: {len(leads)} lead")
            
            # Export to CSV
            csv_data = [["İsim", "Telefon", "Email", "Not", "Tarih"]]
            for lead in leads:
                csv_data.append([
                    lead.get('name', ''),
                    lead.get('phone', ''),
                    lead.get('email', ''),
                    lead.get('note', ''),
                    lead.get('timestamp', '')
                ])
            
            import io
            import csv
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerows(csv_data)
            
            st.download_button(
                "📥 Excel/CSV Olarak İndir",
                data=output.getvalue().encode('utf-8-sig'),
                file_name=f"leads_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("Henüz lead yok")
        
        if st.button("Çıkış Yap"):
            st.session_state.admin_auth = False
            st.rerun()

        # === DIAGNOSTIC SECTION ===
        with st.expander("🛠️ Bağlantı Tanı / Debugging", expanded=True):
            if st.button("Bağlantıyı Şimdi Test Et"):
                st.write("Test başlatılıyor...")
                # 1. Check Libraries
                try:
                    import certifi
                    st.success(f"Certifi Yüklü: {certifi.where()}")
                except ImportError:
                    st.error("Certifi Modülü YOK!")
                
                # 2. Check Connection Strategies
                st.write("--- Strateji 1: Güvenli Bağlantı (Certifi) ---")
                try:
                    c1 = MongoClient(MONGO_URI, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=2000)
                    c1.admin.command('ping')
                    st.success("✅ BAŞARILI: Güvenli bağlantı kuruldu.")
                except Exception as e:
                    st.error(f"❌ BAŞARISIZ: {e}")
                
                st.write("--- Strateji 2: Güvenli Olmayan (Fallback) ---")
                try:
                    c2 = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True, serverSelectionTimeoutMS=2000)
                    c2.admin.command('ping')
                    st.success("✅ BAŞARILI: Yedek bağlantı kuruldu.")
                except Exception as e:
                    st.error(f"❌ BAŞARISIZ: {e}")
                
                # 3. Check CSV
                st.write("--- Yerel Kayıt Durumu ---")
                import os
                if os.path.isfile("local_leads.csv"):
                    st.success("✅ local_leads.csv dosyası mevcut.")
                    with open("local_leads.csv", "r", encoding="utf-8") as f:
                        st.code(f.read())
                else:
                    st.warning("⚠️ local_leads.csv henüz oluşturulmamış.")
                    
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
        
        # Unique key for state management
        prop_id = prop['id']
        
        # Initialize state for this property if not exists
        if f"show_form_{prop_id}" not in st.session_state:
            st.session_state[f"show_form_{prop_id}"] = False

        # Toggle button
        if st.button(T['cta'], key=f"cta_{prop_id}", use_container_width=True):
            st.session_state[f"show_form_{prop_id}"] = not st.session_state[f"show_form_{prop_id}"]
            
        # Show form if active
        if st.session_state[f"show_form_{prop_id}"]:
            with st.container(border=True):
                with st.form(key=f"form_{prop_id}"):
                    st.write(f"**{prop['name']} - {T['cta']}**")
                    name = st.text_input(T['form_name'])
                    phone = st.text_input(T['form_phone']) 
                    email = st.text_input(T['form_email'])
                    note = st.text_area("Not (Opsiyonel)")
                    submitted = st.form_submit_button(T['form_submit'])
                    
                    if submitted:
                        # Validation Logic: Name + (Phone OR Email)
                        if not name:
                            st.warning("⚠️ İsim zorunludur.")
                        elif not phone and not email:
                            st.warning(f"⚠️ {T['form_warning']}")
                        elif phone and len(phone) > 20: 
                            # Max char limit check (Soft Limit)
                            st.warning(f"⚠️ {T['form_phone_err']}")
                        else:
                            success, _ = save_lead(name, phone, email, f"{prop['name']} - {note}")
                            if success:
                                st.success(f"✅ {T['form_ok']}")
                                # Close form after success
                                st.session_state[f"show_form_{prop_id}"] = False
                            else:
                                st.error("❌ Bir bağlantı hatası oluştu, ancak not alındı.")
    
    # === AUTHORITY SECTION ===
    st.markdown(f"""
    <div class="authority-bar">
        <div class="authority-inner">
            <div class="authority-info">
                <h3>Burak Sağlam</h3>
                <p class="title">{T['broker_title']}</p>
                <p class="loc">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
                    Marmara Kule, Kartal / İstanbul
                </p>
            </div>
            <div class="authority-btns">
                <a href="https://wa.me/905064201248" class="auth-link whatsapp" target="_blank">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21l1.65-3.8a9 9 0 1 1 3.4 2.9L3 21"/><path d="M9 10a.5.5 0 0 0 1 0V9a.5.5 0 0 0 1 0v1a5 5 0 0 0 5 5h1a.5.5 0 0 0 0-1h-1a.5.5 0 0 0 0-1h1a.5.5 0 0 0 0-1h-1a5 5 0 0 0-5-5z"/></svg>
                    {T['btn_wa']}
                </a>
                <a href="https://linkedin.com" class="auth-link" target="_blank">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/></svg>
                    {T['btn_li']}
                </a>
                <a href="https://maps.google.com" class="auth-link" target="_blank">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>
                    {T['btn_map']}
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="site-footer">
        <div class="footer-divider"></div>
        <div>
            AGD Investment © 2026<br>
            <span style="opacity: 0.6; font-size: 0.75rem;">Yatırım Mühendisliği & Varlık Yönetimi</span>
        </div>
        <a href="/?admin" target="_self" style="color: #cbd5e1; text-decoration: none; font-size: 0.7rem; opacity: 0.3; transition: opacity 0.2s;">
            Admin
        </a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
