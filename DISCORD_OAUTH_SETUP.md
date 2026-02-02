# 🎮 Configurare Discord OAuth

## Pași pentru a activa login cu Discord

### 1. Creează o aplicație pe Discord Developer Portal

1. Accesează: https://discord.com/developers/applications
2. Apasă **New Application**
3. Dă un nume aplicației (ex: "Money Manager")
4. Accept terms și creează

### 2. Copiază Client ID și Client Secret

1. În tab-ul **General Information**:
   - Copiază **CLIENT ID**
   - Copiază **CLIENT SECRET**

### 3. Setează OAuth2 Redirect URLs

1. Mergi la **OAuth2** > **General**
2. Sub **Redirects**, adaugă:
   ```
   http://127.0.0.1:9512/accounts/discord/login/callback/
   ```
   (inlocuieste 9512 cu portul tău dacă e diferit)

3. Salvează

### 4. Adaugă pe admin

1. Mergi la http://127.0.0.1:9512/admin/
2. Login cu superuser-ul
3. Merge la **Sites** și schimbă:
   - Domain name: `127.0.0.1:9512`
   - Display name: `Money Manager`

### 5. Adaugă credențialele Discord

1. În admin, merge la **Social applications**
2. Creează nou:
   - Provider: **Discord**
   - Name: **Discord OAuth**
   - Client id: (paste CLIENT ID)
   - Secret key: (paste CLIENT SECRET)
   - Sites: selectează Money Manager
3. Salvează

### 6. Gata! 🎉

Acum utilizatorii pot să se conecteze cu Discord!

## Teste

1. Mergi la http://127.0.0.1:9512/accounts/login/
2. Apasă **Conectează-te cu Discord**
3. Autorizează aplicația
4. Vei fi logat și redirectat la dashboard

## Probleme Frecvente

### "Invalid OAuth redirect URI"
- Asigură-te că URL-ul din Discord Developer Portal coincide EXACT cu cel din aplicație
- Include portul dacă folosești dev server

### "Application not found"
- Mergi la /admin/socialaccount/socialapp/
- Asigură-te că aplicația Discord este adăugată cu Sites-ul corect

### Redirect la login după autorizare
- Verifică dacă utilizatorul a fost creat corect
- Check logs pentru erori
