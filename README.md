# 🥇 Gold & Dollar Bias Analyzer

Analyse macroéconomique en temps réel du sentiment entre l'Or (XAUUSD) et le Dollar (DXY).

## 📋 Concept

Ce système :
- Scrape les articles de FXStreet concernant l'or et le dollar
- Analyse le sentiment via IA (Claude ou GPT)
- Met à jour toutes les 35 minutes (configurable)
- Publie sur un canal Telegram
- Affiche les résultats sur un site web (Next.js)

## ⚠️ Notes importantes avant de déployer

1. **Scraping** : les sélecteurs CSS dans `backend/scraper/fxstreet.py` sont génériques.
   FXStreet peut changer sa structure HTML ou bloquer le scraping automatisé
   (Cloudflare, rate limiting). Vérifie les CGU du site et ajuste les sélecteurs
   si besoin en inspectant le DOM réel.
2. **Clé IA** : sans `ANTHROPIC_API_KEY` ou `OPENAI_API_KEY`, le système fonctionne
   quand même grâce à un mode de secours (comptage de mots-clés), mais la qualité
   de l'analyse est bien plus faible.

## 🚀 Installation

### 1. Prérequis
- Python 3.11+
- Node.js 18+

### 2. Backend

```bash
cd gold-dollar-bias
pip install -r requirements.txt
cp .env.example .env
nano .env   # renseigne tes clés API
```

### 3. Frontend

```bash
cd frontend
npm install
```

### 4. Configuration Telegram (optionnel)

1. Crée un bot via [@BotFather](https://t.me/BotFather) → note le token
2. Crée un canal (public ou privé)
3. Ajoute le bot comme administrateur du canal
4. Renseigne `TELEGRAM_BOT_TOKEN` et `TELEGRAM_CHANNEL_ID` dans `.env`

### 5. Lancement en local

```bash
# Terminal 1 - backend
python backend/main.py

# Terminal 2 - frontend
cd frontend
npm run dev
```

Le site est sur http://localhost:3000, l'API sur http://localhost:8000.

Pour tester sans attendre 35 minutes :
```bash
curl -X POST http://localhost:8000/api/analyze-now
```

### 6. Production avec Docker

```bash
docker-compose up -d --build
```

## 📊 API Endpoints

- `GET /api/latest` — Dernière analyse
- `GET /api/history?hours=24` — Historique
- `GET /api/stats` — Statistiques du système
- `GET /api/health` — Health check
- `POST /api/analyze-now` — Déclenche un cycle immédiatement

## 🛠️ Stack technique

- **Backend** : Python, FastAPI, BeautifulSoup
- **IA** : Claude (Anthropic) ou GPT (OpenAI), avec fallback par mots-clés
- **Frontend** : Next.js 14, Tailwind CSS
- **Base de données** : SQLite
- **Déploiement suggéré** : backend sur Railway/Render, frontend sur Vercel

## 📝 Licence

Usage personnel. Respecte les CGU de FXStreet et de Telegram.
