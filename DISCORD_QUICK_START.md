---
# Se poți face ca aplicația să trimită pe Discord când apar modificări?

**DA! ✅ Sistemul de notificări Discord este acum disponibil!**

## ⚡ Setup Rapid (1 Minut)

### 1️⃣ Creează Webhook pe Discord
- Serverul tău Discord → Channel → Click dreapta → Edit Channel
- Integrations → Webhooks → Create Webhook
- Copy URL

### 2️⃣ Completează discord.ini
```ini
WEBHOOK_URL = paste-url-here
```

### 3️⃣ Restartează Django
```bash
py manage.py runserver
```

**GATA!** 🎉 Acum vei primi notificări pe Discord!

---

## 📬 Ce Notificări Primești?

| Event | Emoji | Culoare | Info |
|-------|-------|---------|------|
| Tranzacție Nouă | 💸/💰 | Roșu/Verde | Suma, Categorie, Cont |
| Cont Nou | 🏦 | Albastru | Tip, Valută, Sold |
| Buget Nou | 📊 | Portocaliu | Categorie, Mărime |
| User Nou | 👤 | Purpuriu | Username, Email |
| Discord Connected | 🔗 | Discord Blue | Discord Username |

---

## 🧪 Test Setup

```bash
py test_discord_notifications.py
```

---

## 📖 Documentație Completă

- Ghid detaliat: [DISCORD_NOTIFICATIONS.md](DISCORD_NOTIFICATIONS.md)
- Implementation info: [DISCORD_NOTIFICATIONS_SETUP.md](DISCORD_NOTIFICATIONS_SETUP.md)

---

## ❓ FAQ

**Q: Ce se întâmplă dacă nu am webhook?**
A: Sistemul se dezactivează silențios. Fără erori, fără notificări.

**Q: Pot modifica template-ul notificărilor?**
A: Da! Edit `finance/discord_notifications.py`

**Q: Sigus sunt datele mele?**
A: Da. Webhook-ul este privat și doar din contul tău Discord.

**Q: Care e rata limitare?**
A: Discord permite ~10 mesaje/secundă (plenty!)

**Q: Pot trimite notificări în alte canale?**
A: Da! Crea mai multe webhook-uri cu URL-uri diferite.

---

**Status: 🟢 LIVE - Gata de configurare!**
