# Diário de Vinhos

App para celular (PWA). Cada pessoa escolhe seu nome na primeira abertura, dá sua própria nota e comentário, e o app mostra a média. Não exige conta Claude nem login.

## 1. Banco de dados gratuito (Supabase), uma vez só
1. Crie uma conta em supabase.com e um projeto novo (plano Free).
2. Menu SQL Editor > New query. Cole o conteúdo de `schema.sql` e clique em Run.
3. Menu Project Settings > API. Copie a Project URL e a chave pública (anon / publishable).
4. Abra `config.js` e preencha SUPABASE_URL, SUPABASE_KEY e os dois nomes em USUARIOS.

## 2. Colocar no ar
Suba a pasta `vinhos` em qualquer hospedagem estática (Vercel, Netlify, GitHub Pages). Neste repositório, a pasta sai em `seu-site/vinhos/` pela Vercel.

## 3. Usar
Abra o link no celular. iPhone: Safari > Compartilhar > Adicionar à Tela de Início. Android: Chrome > menu > Adicionar à tela inicial. Mande o mesmo link ao seu namorado.

## Observação de segurança
Não há senha. Quem tiver o link do app consegue ver e editar os vinhos. Não divulgue o link.
