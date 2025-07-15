# 🔍 Discord Token MlemMlem

> ⚠️ **Ostrzeżenie**: Ten projekt ma charakter **czysto edukacyjny** i służy do analizy oraz zrozumienia działania narzędzi typu token grabber. Nieautoryzowane użycie tego kodu jest **nielegalne** i może prowadzić do konsekwencji prawnych. Korzystasz na własną odpowiedzialność.

---

## 📚 Opis

Ten projekt demonstruje, jak działa zaawansowane narzędzie służące do:

- Głębokiego skanowania katalogów aplikacji Discorda w systemie Windows,
- Wyszukiwania tokenów użytkownika w plikach `.ldb`, `.log`, `.sqlite`, `.json` itp.,
- Odszyfrowywania zakodowanych tokenów z plików konfiguracyjnych przy użyciu lokalnego klucza głównego (`master key`),
- Wysyłania danych na wskazany webhook.

---

## 🛠️ Funkcjonalności

- 🔎 Rekurencyjne przeszukiwanie folderów `AppData`, `LocalAppData` i `Program Files` Discorda.
- 🧠 Użycie wyrażeń regularnych do identyfikacji tokenów (`standardowe` oraz `zaszyfrowane`).
- 🔐 Odszyfrowanie tokenów przy użyciu klucza AES pobranego z pliku `Local State`.
- 📦 Przetwarzanie plików tekstowych i baz danych SQLite.
- 🌐 Gotowe do wysyłki danych na zewnętrzny serwer (np. webhook Discorda – do analizy w bezpiecznym środowisku).

---

## 🧪 Zastosowanie

- 📖 Nauka o sposobach działania złośliwego oprogramowania.
- 🔐 Testowanie własnych systemów zabezpieczeń.
- 🧬 Analiza próbki malware w bezpiecznym środowisku (sandbox, VM).
- 🛡️ Tworzenie narzędzi do detekcji i neutralizacji token grabberów.

---

## 📁 Struktura katalogów skanowanych

```text
📂 Ścieżki skanowane:
├── %APPDATA%\Discord
├── %LOCALAPPDATA%\Discord
├── %PROGRAMFILES%\Discord
└── %PROGRAMFILES(X86)%\Discord
