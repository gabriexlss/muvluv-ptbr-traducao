# Muv-Luv — Tradução PT-BR (Steam 2016 + Director's Cut)

Projeto de tradução para **Português Brasileiro (PT-BR)** da visual novel **Muv-Luv** (**Extra** e **Unlimited**), build **Steam 2016** com o patch **Director's Cut 18+** (`muvluv16.exe` + `muvluv16.rio.drcruo1`).

> **Importante:** este repositório contém **apenas** os textos traduzidos em PT-BR (`translation/*.json`), metadados (`metadata.json`) e scripts de validação. Nenhum arquivo proprietário do jogo (`muvluv16.exe`, `.rio*`, DLLs, áudio, imagens, vídeos ou scripts originais em inglês/japonês) é redistribuído aqui.

---

## Cobertura da Tradução

- **Rotas cobertas**: **Muv-Luv Extra** + **Muv-Luv Unlimited** (todas as cenas em `CRsa` e avisos de sistema em script).
- **Arquivos de cena**: `102` arquivos JSON organizados em ordem cronológica (`000_UI_System_Menus.json` até `101_Scene_FC842B22.json`).
- **Volume total**: `63.242` entradas no formato Message-JSON (`[{ "name": "...", "message": "..." }]`).

## Requisitos do Jogo

- Cópia original de **Muv-Luv (versão Steam 2016 — motor rUGP)**.
- **Patch Director's Cut 18+ aplicado** (o jogo precisa possuir o overlay `muvluv16.rio.drcruo1` ativo na pasta de instalação).
  - Hash SHA-256 de referência do `muvluv16.rio.drcruo1` original: `57a9cc354300a3f4ac680332b3c0cb6a3ef751823a1622f6f95644ac3ad83765` (`359.226.836` bytes).
  - Hash SHA-256 de referência do `muvluv16.exe`: `0bfb31f2127d1ac4039f13097a137471838256128a63012c9ff44e5dac7f4b71`.

---

## Como Instalar (Recomendado — 1 Clique)

> **[Baixe aqui o Instalador Gráfico em 1 Clique (muvluv-ptbr-instalador)](https://github.com/<SEU_USUARIO_GITHUB>/muvluv-ptbr-instalador/releases/latest)** *(substitua pelo link do repositório do instalador quando publicado)*.

O instalador:
1. Localiza automaticamente a pasta do jogo (Steam / registro / seleção manual).
2. Faz backup permanente e intocável do seu `muvluv16.rio.drcruo1` original.
3. Baixa automaticamente o pacote mais recente (`muvluv-ptbr-translation.zip`) das **Releases** deste repositório.
4. Descriptografa, aplica as traduções nos registros `CRsa`, recalcula os checksums rUGP e verifica tudo byte a byte no disco antes de concluir.
5. Permite **restaurar o inglês original** com 1 clique a qualquer momento.

---

## Estrutura para Desenvolvedores e para o Instalador

Este repositório expõe um contrato simples nas **GitHub Releases**:

- **Asset oficial por release**: `muvluv-ptbr-translation.zip` (gerado automaticamente por [release-package.yml](.github/workflows/release-package.yml) sempre que uma tag `v*` é publicada), acompanhado de `muvluv-ptbr-translation.zip.sha256`.
- **`metadata.json`**: contém versão, hashes de referência do jogo, parâmetros do overlay rUGP (`unit_size: 2`, `file_count: 102`, `total_entries: 63242`) e a lista ordenada com `filename`, `entry_count`, `wait_tag_count` e `sha256` de cada arquivo em `translation/`.
- **`translation/*.json`**: arrays UTF-8 (sem BOM, LF) no formato Message-JSON compatível com mapeamento posicional 1:1 com a extração rUGP.
- **Validação**:
  ```bash
  python3 scripts/validate_repo.py           # Validação estrita (incluindo SHA-256)
  python3 scripts/validate_repo.py --skip-hash  # Validação estrutural (PRs)
  ```

---

## Limitações Conhecidas

- **Menus gráficos, imagens/CGs e vídeos**: botões visuais de menu (Tela de Título, botões gráficos de *Save / Load / Config / Backlog / Auto / Skip*), imagens e vídeos usam texturas/codecs proprietários do rUGP (`Cr6Ti`, `CRip007`, `CRip008`, `CS5i`) e permanecem no idioma original. *(Os diálogos de confirmação em script — Sim/Não, avisos de save/load — estão traduzidos em `000_UI_System_Menus.json`.)*
- **Janelas nativas do Windows / *Advanced Settings***: strings embutidas diretamente no `muvluv16.exe` e `Ages3ResT.dll` permanecem em inglês por padrão.
- **Fonte especial `.5RF` embutida**: os diálogos normais usam Windows GDI (`Arial` + `ＭＳ Ｐゴシック`) com suporte nativo aos acentos PT-BR. Uma fonte bitmap especial embutida no `muvluv16.rio` (`ＤＦＧ平成明朝体W9`) não contém glifos acentuados nativamente (o instalador oferece um patch opcional no `.exe` para ativar fallback GDI).

---

## Créditos e Agradecimentos

- **LinguaGacha** — pipeline de tradução com LLM em Message-JSON.
- **muvluv-voice-tools** — pesquisa de descifragem do formato TOC/ICI/RIO *schema-4* do `muvluv16`.
- **AgeReVerse (rUGP)** — documentação e arquitetura reversa dos overlays `.ruo` e registros `CRsa`.

## Aviso Legal

Tradução feita por fã, gratuita e sem fins lucrativos. **Muv-Luv** é propriedade de **aNchor Inc. / âge**. Apoie os criadores comprando o jogo oficial.
