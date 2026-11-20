# Como Contribuir com Correções na Tradução

Por ter sido feito com IA, Toda ajuda para revisar erros de digitação, concordância, gênero ou fluidez nos diálogos é bem-vinda!

## Regras obrigatórias ao editar os JSONs

Os arquivos em `translation/*.json` seguem o formato **Message-JSON** e são recompilados diretamente para os blocos binários `CRsa` do motor rUGP. Para não quebrar o jogo nem a validação:

1. **Nunca adicione nem remova itens do array JSON**, cada arquivo precisa manter exatamente a mesma quantidade e ordem de objetos `{ "name": "...", "message": "..." }`.
2. **Preserve o campo `"name"` como está** (ou omitido na narração), a menos que haja decisão explícita de revisão global.
3. **Nunca remova nem traduza a tag `<WAIT>`**, ela controla pausas de clique no meio do texto em cena.
4. **Não use `U+0000` (`\u0000`)** nem caracteres de controle invisíveis (quebras de linha reais dentro do texto devem usar `\n` dentro da string JSON).
5. **Mantenha UTF-8 sem BOM e quebras de linha LF (`\n`)**.
6. **Não altere `metadata.json` manualmente em Pull Requests**, o workflow de PR roda `--skip-hash` automaticamente; apenas mantenedores atualizam os hashes antes de publicar uma nova tag/release.

## Como validar suas alterações localmente

```bash
python3 scripts/validate_repo.py --skip-hash
```

Se você for mantenedor preparando uma nova release:

```bash
# 1. Atualize a versão em metadata.json (ex.: "1.0.1")
# 2. Atualize os SHA-256 automaticamente e valide tudo:
python3 scripts/validate_repo.py --update-hashes
python3 scripts/validate_repo.py
```
