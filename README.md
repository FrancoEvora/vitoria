# Vitória — Solaris Residencial

Aplicação pública da Évora Urbanismo para atendimento inteligente do Solaris Residencial.

A produção combina um frontend estático na Vercel com Supabase Edge Functions, PostgreSQL/RLS e OpenAI no ambiente server-side. A experiência consulta estoque, preços e política comercial em tempo real e permite solicitar o bloqueio temporário de um lote, sempre sujeito à aprovação administrativa.

O arquivo `site.tar.gz` é o artefato estático versionado da publicação; `build.mjs` o valida e materializa em `dist` durante o build, sem dependências externas.
