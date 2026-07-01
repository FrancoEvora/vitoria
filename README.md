# Évora LeadFlow

MVP funcional do **Évora LeadFlow**, um CRM ativo via WhatsApp com a agente **Vitória**.

A plataforma entrega:

- Conversa com corretores por WhatsApp/webhook.
- Cadastro guiado de leads.
- Classificação quente/morno/frio.
- Próxima melhor ação sugerida pela Vitória.
- Scripts comerciais por perfil e objeção.
- Follow-up diário para corretores.
- Dashboard web para gestão comercial.
- APIs administrativas para leads, corretores, empreendimentos e materiais.
- Configuração pronta para GitHub e deploy na Vercel.

## Arquitetura do MVP

```text
WhatsApp do corretor
        ↓
Meta WhatsApp Cloud API / Webhook
        ↓
FastAPI Backend
        ↓
PostgreSQL
        ↓
Agente Vitória + regras comerciais + OpenAI opcional
        ↓
Dashboard web server-rendered
```

Esta versão usa **FastAPI + Jinja2** para entregar API, webhook e dashboard em uma única aplicação. Isso simplifica o MVP e já permite deploy na Vercel usando runtime Python/FastAPI.

Para uma versão SaaS mais robusta, o próximo passo recomendado é separar frontend, backend, worker e banco gerenciado.

## Pastas principais

```text
evora-leadflow/
├── app/                  # FastAPI, banco, agente Vitória, webhook e dashboard
├── docs/                 # Instruções de configuração e operação
├── scripts/              # Simulações e comandos úteis
├── tests/                # Testes automatizados
├── docker-compose.yml    # Subida local completa
├── vercel.json           # Configuração para Vercel
├── pyproject.toml        # Entrypoint FastAPI para Vercel
├── .env.example          # Variáveis de ambiente
└── Makefile              # Atalhos de setup
```

## Subida rápida local

1. Copie o arquivo de ambiente:

```bash
cp .env.example .env
```

2. Suba a plataforma:

```bash
docker compose up --build
```

3. Acesse:

- Dashboard: http://localhost:8000
- Backend/API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Healthcheck público: http://localhost:8000/health

4. Teste a Vitória sem WhatsApp real:

```bash
python scripts/simulate_message.py
```

Ou envie uma mensagem manual:

```bash
curl -X POST http://localhost:8000/api/simulate-message \
  -u evora:troque_esta_senha \
  -H "Content-Type: application/json" \
  -d '{"from_phone":"5516999990001","text":"tenho um lead","profile_name":"Carlos"}'
```

## Credenciais do MVP

O painel usa autenticação básica HTTP.

No `.env` local:

```env
DASHBOARD_USERNAME=evora
DASHBOARD_PASSWORD=troque_esta_senha
```

Em produção, troque a senha e, antes de liberar para equipe grande, substitua por autenticação real com usuários, papéis e permissões.

## GitHub e Vercel

Leia o guia completo:

```text
docs/DEPLOY_GITHUB_VERCEL.md
```

Resumo:

```bash
git init
git add .
git commit -m "Initial Évora LeadFlow MVP"
git branch -M main
gh repo create evora-leadflow --private --source=. --remote=origin --push
```

Depois importe o repositório na Vercel, configure `DATABASE_URL` com um PostgreSQL gerenciado e coloque `ENABLE_SCHEDULER=false`.

## WhatsApp real

Leia `docs/WHATSAPP_SETUP.md`.

Resumo:

- Criar app no Meta for Developers.
- Configurar WhatsApp Business Platform / Cloud API.
- Expor o backend em HTTPS.
- Cadastrar callback URL: `https://seu-dominio.com/webhooks/whatsapp`.
- Usar o mesmo `WHATSAPP_VERIFY_TOKEN` no `.env` e no painel da Meta.
- Preencher `WHATSAPP_ACCESS_TOKEN` e `WHATSAPP_PHONE_NUMBER_ID`.

## OpenAI opcional

A Vitória funciona com regras locais. Para melhorar scripts e diagnósticos com modelo de linguagem, configure:

```env
OPENAI_API_KEY=sua-chave
OPENAI_MODEL=gpt-5.5
```

## Próximos incrementos recomendados

1. Autenticação real com login e papéis.
2. Templates WhatsApp aprovados para mensagens proativas.
3. Upload de materiais em storage próprio.
4. Transcrição de áudio.
5. Integração com CRM legado, RD Station, Meta Ads ou formulários.
6. BI avançado com conversão por origem, empreendimento e corretor.
7. Motor de permissões por empreendimento/equipe.
8. Multiempresa para transformar em SaaS.
