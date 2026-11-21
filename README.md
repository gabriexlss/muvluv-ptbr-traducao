# Muv-Luv: Tradução PT-BR (Steam 2016 + Director's Cut)

Quando fui jogar **Muv-Luv** (*Extra* e *Unlimited*), me deparei com um problema: não existia nenhuma tradução do jogo para o português, nem oficial, nem feita por fãs. Como projetos gigantescos como esse costumam levar meses ou até anos para serem concluídos, decidi usar a IA para acelerar o processo e conseguir jogar o jogo, e como já estava feito e eu estava curtindo, ajudar também pessoas na mesma situação que a minha!

Este é um projeto de tradução para **Português Brasileiro (PT-BR)** da visual novel **Muv-Luv** (**Extra** e **Unlimited**), com suporte ao patch **Director's Cut 18+**.

> **Nota sobre a tradução:** Como os textos foram traduzidos utilizando Inteligência Artificial, espere encontrar algumas imprecisões ou frases estranhas de vez em quando. Esse projeto foi feito para pessoas ansiosas como eu, que não conseguem esperar uma tradução tradicional feita por uma equipe especializada de fãs e só querem aproveitar a história no nosso idioma!

> **Importante:** este repositório contém **apenas** os textos traduzidos em PT-BR (`translation/*.json`), metadados (`metadata.json`) e scripts de validação. Nenhum arquivo proprietário do jogo (`muvluv16.exe`, `.rio*`, DLLs, áudio, imagens, vídeos ou scripts originais em inglês/japonês) é redistribuído aqui.

## Cobertura da Tradução

- **Rotas cobertas**: **Muv-Luv Extra** + **Muv-Luv Unlimited** (todas as cenas em `CRsa` e avisos de sistema em script).
- **Arquivos de cena**: `102` arquivos JSON organizados em ordem cronológica (`000_UI_System_Menus.json` até `101_Scene_FC842B22.json`).
- **Volume total**: `63.242` entradas no formato Message-JSON (`[{ "name": "...", "message": "..." }]`).

## Requisitos do Jogo

- Cópia original de **Muv-Luv (versão Steam 2016, motor rUGP)**.
- **Patch Director's Cut 18+ aplicado** (o jogo precisa possuir o overlay `muvluv16.rio.drcruo1` ativo na pasta de instalação).
  - Hash SHA-256 de referência do `muvluv16.rio.drcruo1` original: `57a9cc354300a3f4ac680332b3c0cb6a3ef751823a1622f6f95644ac3ad83765` (`359.226.836` bytes).
  - Hash SHA-256 de referência do `muvluv16.exe`: `0bfb31f2127d1ac4039f13097a137471838256128a63012c9ff44e5dac7f4b71`.

## Como Instalar (Recomendado, já que instala com um único clique)

> **[Baixe aqui o Instalador Gráfico em 1 Clique (muvluv-ptbr-instalador)](https://github.com/gabriexlss/muvluv-ptbr-instalador/releases/latest)**

## Limitações Conhecidas

- **Menus gráficos, imagens/CGs e vídeos**: botões visuais de menu (Tela de Título, botões gráficos de *Save / Load / Config / Backlog / Auto / Skip*), imagens e vídeos usam texturas/codecs proprietários do rUGP (`Cr6Ti`, `CRip007`, `CRip008`, `CS5i`) e permanecem no idioma original. *(Os diálogos de confirmação em script, como Sim/Não e avisos de save/load, estão traduzidos em `000_UI_System_Menus.json`.)*
- **Janelas nativas do Windows / *Advanced Settings***: strings embutidas diretamente no `muvluv16.exe` e `Ages3ResT.dll` permanecem em inglês por padrão.
- **Fonte especial `.5RF` embutida**: os diálogos normais usam Windows GDI (`Arial` + `ＭＳ Ｐゴシック`) com suporte nativo aos acentos PT-BR. Uma fonte bitmap especial embutida no `muvluv16.rio` (`ＤＦＧ平成明朝体W9`) não contém glifos acentuados nativamente (o instalador oferece um patch opcional no `.exe` para ativar fallback GDI).

## Créditos e Agradecimentos

- **LinguaGacha**, pipeline de tradução com LLM em Message-JSON.
- **muvluv-voice-tools**, pesquisa de descifragem do formato TOC/ICI/RIO *schema-4* do `muvluv16`.
- **AgeReVerse (rUGP)**, documentação e arquitetura reversa dos overlays `.ruo` e registros `CRsa`.

## Aviso Legal

Tradução feita por fã, gratuita e sem fins lucrativos. **Muv-Luv** é propriedade de **aNchor Inc. / âge**. Apoie os criadores comprando o jogo oficial.
