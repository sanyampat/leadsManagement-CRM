import sqlite3
import hashlib
import re
import threading

class DedupStore:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.lock = threading.Lock()
        
        with self.lock:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS processed_leads (
                    hash_key TEXT PRIMARY KEY,
                    source TEXT,
                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.conn.commit()

    def _normalize(self, value):
        if not value:
            return ""
        return re.sub(r'\W+', '', str(value).lower())

    def _generate_key(self, domain, phone, name, source):
        norm_domain = self._normalize(domain)
        norm_phone = self._normalize(phone)
        
        if not norm_domain and not norm_phone:
            norm_name = self._normalize(name)
            norm_source = self._normalize(source)
            if not norm_name:
                return None
            raw_key = f"name_{norm_name}_src_{norm_source}"
        else:
            raw_key = f"{norm_domain}_{norm_phone}"
            
        return hashlib.md5(raw_key.encode('utf-8')).hexdigest()

    def is_new(self, domain, phone, name, source):
        key = self._generate_key(domain, phone, name, source)
        if not key:
            return True
            
        with self.lock:
            cursor = self.conn.execute("SELECT 1 FROM processed_leads WHERE hash_key = ?", (key,))
            return cursor.fetchone() is None

    def mark_processed(self, domain, phone, name, source):
        key = self._generate_key(domain, phone, name, source)
        if key:
            with self.lock:
                try:
                    self.conn.execute(
                        "INSERT INTO processed_leads (hash_key, source) VALUES (?, ?)", 
                        (key, source)
                    )
                    self.conn.commit()
                except sqlite3.IntegrityError:
                    pass