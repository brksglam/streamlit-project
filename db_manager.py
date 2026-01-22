"""
=============================================================================
AGD INVESTMENT - ROBUST DATABASE MANAGER
=============================================================================
Bu modül MongoDB bağlantısını ve lead yönetimini sağlar.
Tüm hatalar yakalanır ve yerel CSV'ye fallback yapılır.

ÖZELLIKLER:
- MongoDB Atlas bağlantısı (TLS/SSL ile)
- Otomatik retry mekanizması
- Yerel CSV fallback
- E-posta bildirimi (opsiyonel)
- Comprehensive logging
=============================================================================
"""

import os
import csv
import logging
from datetime import datetime
from typing import Tuple, List, Dict, Optional

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# =============================================================================
# CONFIGURATION
# =============================================================================
MONGO_URI = "mongodb+srv://buraksaglam415_db_user:jnIC2z40mFDD8rqh@cluster0.swtf7ev.mongodb.net/?appName=Cluster0"
DB_NAME = "agd_investment"
COLLECTION_NAME = "leads"
LOCAL_CSV_PATH = "local_leads.csv"

# Connection timeout settings
CONNECTION_TIMEOUT_MS = 5000
SERVER_SELECTION_TIMEOUT_MS = 5000

# =============================================================================
# DATABASE CONNECTION MANAGER
# =============================================================================
class DatabaseManager:
    """Thread-safe, robust database manager with fallback support."""
    
    _instance = None
    _client = None
    _db = None
    _status = "unknown"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self._connect()
    
    def _connect(self) -> None:
        """Attempt MongoDB connection with multiple strategies."""
        
        # Strategy 1: Secure connection with certifi
        try:
            import certifi
            from pymongo import MongoClient
            
            logger.info("MongoDB bağlantısı deneniyor (Strateji 1: Certifi)...")
            
            self._client = MongoClient(
                MONGO_URI,
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=SERVER_SELECTION_TIMEOUT_MS,
                connectTimeoutMS=CONNECTION_TIMEOUT_MS,
                retryWrites=True,
                w='majority'
            )
            
            # Test connection
            self._client.admin.command('ping')
            self._db = self._client[DB_NAME]
            self._status = "online"
            logger.info("✅ MongoDB bağlantısı BAŞARILI (Certifi)")
            return
            
        except ImportError:
            logger.warning("Certifi modülü bulunamadı, Strateji 2'ye geçiliyor...")
        except Exception as e:
            logger.warning(f"Strateji 1 başarısız: {e}")
        
        # Strategy 2: TLS without certificate verification (less secure)
        try:
            from pymongo import MongoClient
            
            logger.info("MongoDB bağlantısı deneniyor (Strateji 2: TLS Fallback)...")
            
            self._client = MongoClient(
                MONGO_URI,
                tls=True,
                tlsAllowInvalidCertificates=True,
                serverSelectionTimeoutMS=SERVER_SELECTION_TIMEOUT_MS,
                connectTimeoutMS=CONNECTION_TIMEOUT_MS
            )
            
            self._client.admin.command('ping')
            self._db = self._client[DB_NAME]
            self._status = "online"
            logger.info("✅ MongoDB bağlantısı BAŞARILI (TLS Fallback)")
            return
            
        except Exception as e:
            logger.warning(f"Strateji 2 başarısız: {e}")
        
        # Strategy 3: Offline mode
        logger.warning("⚠️ MongoDB bağlantısı kurulamadı - OFFLINE modda çalışılıyor")
        self._status = "offline"
        self._client = None
        self._db = None
    
    @property
    def status(self) -> str:
        return self._status
    
    @property
    def is_online(self) -> bool:
        # Use status flag - avoids pymongo deprecation warning
        return self._status == "online"
    
    def _check_db_ready(self) -> bool:
        """Check if database connection is ready for operations."""
        return self._status == "online" and self._db is not None
    
    def reconnect(self) -> bool:
        """Force reconnection attempt."""
        self._client = None
        self._db = None
        self._status = "unknown"
        self._connect()
        return self.is_online
    
    def save_lead(self, name: str, phone: str, note: str, source: str = "web") -> Tuple[bool, str]:
        """
        Save a lead to the database.
        
        Args:
            name: Customer name
            phone: Customer phone
            note: Additional notes (property info, etc.)
            source: Lead source (web, admin, etc.)
            
        Returns:
            Tuple of (success: bool, mode: str)
            mode can be: 'online', 'offline', 'error'
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        lead_data = {
            "name": name.strip(),
            "phone": phone.strip(),
            "note": note.strip() if note else "",
            "source": source,
            "timestamp": timestamp,
            "status": "new",
            "created_at": datetime.now()
        }
        
        # Try MongoDB first
        if self.is_online:
            try:
                result = self._db[COLLECTION_NAME].insert_one(lead_data)
                logger.info(f"✅ Lead MongoDB'ye kaydedildi: {result.inserted_id}")
                return True, "online"
            except Exception as e:
                logger.error(f"MongoDB yazma hatası: {e}")
                # Fall through to offline backup
        
        # Offline fallback - save to CSV
        try:
            file_exists = os.path.isfile(LOCAL_CSV_PATH)
            
            with open(LOCAL_CSV_PATH, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                
                if not file_exists:
                    writer.writerow(["name", "phone", "note", "source", "timestamp", "status"])
                
                writer.writerow([
                    lead_data["name"],
                    lead_data["phone"],
                    lead_data["note"],
                    lead_data["source"],
                    lead_data["timestamp"],
                    "new_offline"
                ])
            
            logger.info(f"✅ Lead CSV'ye kaydedildi (Offline)")
            return True, "offline"
            
        except Exception as e:
            logger.error(f"❌ CSV yazma hatası: {e}")
            return False, "error"
    
    def get_all_leads(self) -> List[Dict]:
        """
        Get all leads from MongoDB and local CSV.
        
        Returns:
            List of lead dictionaries, sorted by timestamp (newest first)
        """
        all_leads = []
        
        # 1. Fetch from MongoDB
        if self.is_online:
            try:
                mongo_leads = list(self._db[COLLECTION_NAME].find().sort("_id", -1))
                for lead in mongo_leads:
                    lead['_id'] = str(lead['_id'])  # Convert ObjectId to string
                    lead['db_source'] = 'MongoDB'
                all_leads.extend(mongo_leads)
                logger.info(f"MongoDB'den {len(mongo_leads)} lead alındı")
            except Exception as e:
                logger.error(f"MongoDB okuma hatası: {e}")
        
        # 2. Fetch from local CSV
        if os.path.isfile(LOCAL_CSV_PATH):
            try:
                with open(LOCAL_CSV_PATH, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    csv_leads = list(reader)
                    
                    for lead in csv_leads:
                        lead['db_source'] = 'CSV (Offline)'
                    
                    all_leads.extend(csv_leads)
                    logger.info(f"CSV'den {len(csv_leads)} lead alındı")
            except Exception as e:
                logger.error(f"CSV okuma hatası: {e}")
        
        # Sort by timestamp (newest first)
        try:
            all_leads.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        except:
            pass
        
        return all_leads
    
    def get_lead_count(self) -> Dict[str, int]:
        """Get lead counts from all sources."""
        counts = {"mongodb": 0, "csv": 0, "total": 0}
        
        if self.is_online:
            try:
                counts["mongodb"] = self._db[COLLECTION_NAME].count_documents({})
            except:
                pass
        
        if os.path.isfile(LOCAL_CSV_PATH):
            try:
                with open(LOCAL_CSV_PATH, "r", encoding="utf-8") as f:
                    counts["csv"] = sum(1 for _ in f) - 1  # Subtract header
                    if counts["csv"] < 0:
                        counts["csv"] = 0
            except:
                pass
        
        counts["total"] = counts["mongodb"] + counts["csv"]
        return counts
    
    def sync_offline_leads(self) -> Tuple[int, int]:
        """
        Sync offline CSV leads to MongoDB.
        
        Returns:
            Tuple of (synced_count, failed_count)
        """
        if not self.is_online:
            logger.warning("MongoDB offline - senkronizasyon yapılamadı")
            return 0, 0
        
        if not os.path.isfile(LOCAL_CSV_PATH):
            return 0, 0
        
        synced = 0
        failed = 0
        remaining_leads = []
        
        try:
            with open(LOCAL_CSV_PATH, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                leads = list(reader)
            
            for lead in leads:
                try:
                    # Insert to MongoDB
                    self._db[COLLECTION_NAME].insert_one({
                        "name": lead.get("name", ""),
                        "phone": lead.get("phone", ""),
                        "note": lead.get("note", ""),
                        "source": lead.get("source", "csv_sync"),
                        "timestamp": lead.get("timestamp", ""),
                        "status": "synced_from_offline",
                        "synced_at": datetime.now()
                    })
                    synced += 1
                except Exception as e:
                    logger.error(f"Lead senkronizasyon hatası: {e}")
                    remaining_leads.append(lead)
                    failed += 1
            
            # Rewrite CSV with only failed leads
            if remaining_leads:
                with open(LOCAL_CSV_PATH, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=["name", "phone", "note", "source", "timestamp", "status"])
                    writer.writeheader()
                    writer.writerows(remaining_leads)
            else:
                # All synced, remove CSV
                os.remove(LOCAL_CSV_PATH)
            
            logger.info(f"✅ {synced} lead senkronize edildi, {failed} başarısız")
            return synced, failed
            
        except Exception as e:
            logger.error(f"Senkronizasyon hatası: {e}")
            return 0, 0
    
    def test_connection(self) -> Dict:
        """
        Run comprehensive connection diagnostics.
        
        Returns:
            Dictionary with test results
        """
        results = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": self._status,
            "tests": {}
        }
        
        # Test 1: Certifi availability
        try:
            import certifi
            results["tests"]["certifi"] = {
                "status": "pass",
                "path": certifi.where()
            }
        except ImportError:
            results["tests"]["certifi"] = {
                "status": "fail",
                "error": "Certifi modülü bulunamadı"
            }
        
        # Test 2: MongoDB ping
        if self._client is not None:
            try:
                self._client.admin.command('ping')
                results["tests"]["ping"] = {"status": "pass"}
            except Exception as e:
                results["tests"]["ping"] = {"status": "fail", "error": str(e)}
        else:
            results["tests"]["ping"] = {"status": "skip", "reason": "No client"}
        
        # Test 3: Database access
        if self._db is not None:
            try:
                collections = self._db.list_collection_names()
                results["tests"]["database"] = {
                    "status": "pass",
                    "collections": collections
                }
            except Exception as e:
                results["tests"]["database"] = {"status": "fail", "error": str(e)}
        else:
            results["tests"]["database"] = {"status": "skip", "reason": "No database"}
        
        # Test 4: Write test
        if self._db is not None:
            try:
                test_id = self._db["_connection_tests"].insert_one({
                    "test": True,
                    "timestamp": datetime.now()
                }).inserted_id
                self._db["_connection_tests"].delete_one({"_id": test_id})
                results["tests"]["write"] = {"status": "pass"}
            except Exception as e:
                results["tests"]["write"] = {"status": "fail", "error": str(e)}
        else:
            results["tests"]["write"] = {"status": "skip", "reason": "No database"}
        
        # Test 5: CSV fallback
        try:
            test_file = "_test_csv_write.tmp"
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
            results["tests"]["csv_fallback"] = {"status": "pass"}
        except Exception as e:
            results["tests"]["csv_fallback"] = {"status": "fail", "error": str(e)}
        
        return results


# =============================================================================
# GLOBAL INSTANCE
# =============================================================================
_db_manager = None

def get_db_manager() -> DatabaseManager:
    """Get the singleton database manager instance."""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================
def save_lead(name: str, phone: str, note: str = "", source: str = "web") -> Tuple[bool, str]:
    """Save a lead using the database manager."""
    return get_db_manager().save_lead(name, phone, note, source)

def get_all_leads() -> List[Dict]:
    """Get all leads using the database manager."""
    return get_db_manager().get_all_leads()

def get_db_status() -> str:
    """Get current database connection status."""
    return get_db_manager().status

def test_db_connection() -> Dict:
    """Run connection diagnostics."""
    return get_db_manager().test_connection()


# =============================================================================
# CLI TEST MODE
# =============================================================================
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🔧 AGD DATABASE MANAGER - DIAGNOSTIC TEST")
    print("=" * 60)
    
    db = get_db_manager()
    
    print(f"\n📊 Status: {db.status}")
    print(f"📊 Is Online: {db.is_online}")
    
    print("\n" + "-" * 60)
    print("🧪 Running Connection Tests...")
    print("-" * 60)
    
    results = db.test_connection()
    
    for test_name, test_result in results["tests"].items():
        status = test_result["status"]
        icon = "✅" if status == "pass" else "❌" if status == "fail" else "⏭️"
        print(f"   {icon} {test_name}: {status}")
        if "error" in test_result:
            print(f"      └─ {test_result['error']}")
    
    print("\n" + "-" * 60)
    print("📈 Lead Statistics")
    print("-" * 60)
    
    counts = db.get_lead_count()
    print(f"   MongoDB: {counts['mongodb']}")
    print(f"   CSV:     {counts['csv']}")
    print(f"   Total:   {counts['total']}")
    
    print("\n" + "=" * 60)
    print("🎉 DIAGNOSTIC COMPLETE")
    print("=" * 60 + "\n")
