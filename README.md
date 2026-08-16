# Vitória — Solaris Residencial

Aplicação pública da Évora Urbanismo para atendimento inteligente do Solaris Residencial.

A produção combina um frontend estático na Vercel com Supabase Edge Functions, PostgreSQL/RLS e OpenAI no ambiente server-side. A experiência consulta estoque, preços e política comercial em tempo real e permite solicitar o bloqueio temporário de um lote, sempre sujeito à aprovação administrativa.

O diretório `bundle/` contém o artefato estático da publicação dividido em partes Base64. Durante o build, `build.mjs` reúne as partes, valida tamanho e SHA-256, descompacta o conteúdo e materializa o diretório `dist` sem dependências externas.
