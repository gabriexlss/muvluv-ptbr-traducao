#!/usr/bin/env python3
"""
Valida os arquivos de traducao PT-BR em Message-JSON contra metadata.json.

Uso:
  python3 scripts/validate_repo.py                 # Validacao completa (inclui SHA-256)
  python3 scripts/validate_repo.py --skip-hash     # Para PRs (valida estrutura/contagens/tags sem exigir hash atualizado)
  python3 scripts/validate_repo.py --update-hashes # Recalcula SHA-256 em metadata.json apos validar tudo
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys

ALLOWED_TAG_RE = re.compile(r"<WAIT>|<CTRL[0-9A-Fa-f]{2}>")
ALLOWED_KEYS = {"name", "message"}


def check_text(value: str, label: str, errors: list[str]) -> None:
    if "\x00" in value:
        errors.append(f"{label}: contem byte NUL (\\u0000), proibido pelo motor rUGP (InternalError 8311)")
        return
    for ch in value:
        code = ord(ch)
        if code < 0x20 and ch != "\n":
            errors.append(f"{label}: caractere de controle invalido U+{code:04X}")
            break
    stripped = ALLOWED_TAG_RE.sub("", value)
    if "<" in stripped or ">" in stripped:
        errors.append(f"{label}: sinal '<' ou '>' inesperado fora de tag <WAIT>/<CTRLxx>")


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida o repositorio de traducao PT-BR do Muv-Luv.")
    parser.add_argument(
        "--root",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().parent.parent,
        help="Raiz do repositorio (padrao: pasta pai de scripts/)",
    )
    parser.add_argument(
        "--skip-hash",
        action="store_true",
        help="Nao falha se os SHA-256 dos JSONs divergirem de metadata.json (util em Pull Requests)",
    )
    parser.add_argument(
        "--update-hashes",
        action="store_true",
        help="Atualiza os campos sha256 (e version se combinado manualmente) em metadata.json se todas as demais checagens passarem",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    meta_path = root / "metadata.json"
    if not meta_path.is_file():
        print(f"ERRO: metadata.json nao encontrado em {meta_path}", file=sys.stderr)
        return 1

    meta_raw = meta_path.read_bytes()
    if meta_raw.startswith(b"\xef\xbb\xbf"):
        print("ERRO: metadata.json contem BOM UTF-8 (use UTF-8 sem BOM)", file=sys.stderr)
        return 1

    try:
        meta = json.loads(meta_raw.decode("utf-8"))
    except Exception as exc:
        print(f"ERRO: falha ao ler metadata.json: {exc}", file=sys.stderr)
        return 1

    trans_rel = meta.get("translation_dir", "translation")
    trans_dir = root / trans_rel
    if not trans_dir.is_dir():
        print(f"ERRO: pasta de traducao '{trans_dir}' nao existe", file=sys.stderr)
        return 1

    expected_files = meta.get("files")
    if not isinstance(expected_files, list) or not expected_files:
        print("ERRO: metadata.json sem lista valida 'files'", file=sys.stderr)
        return 1

    actual_items = sorted(trans_dir.iterdir(), key=lambda p: p.name)
    actual_names = {p.name for p in actual_items if p.is_file()}
    non_files = [p.name for p in actual_items if not p.is_file()]
    expected_names = {entry["filename"] for entry in expected_files}

    errors: list[str] = []
    if non_files:
        errors.append(f"Subpastas ou itens nao regulares inesperados em {trans_rel}/: {non_files}")

    missing = sorted(expected_names - actual_names)
    extra = sorted(actual_names - expected_names)
    if missing:
        errors.append(f"Arquivos ausentes em {trans_rel}/ ({len(missing)}): {missing[:10]}")
    if extra:
        errors.append(f"Arquivos extras nao listados em metadata.json ({len(extra)}): {extra[:10]}")

    total_entries = 0
    total_wait_tags = 0
    hash_updates = 0

    for fmeta in expected_files:
        fname = fmeta["filename"]
        fpath = trans_dir / fname
        if not fpath.is_file():
            continue

        raw = fpath.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            errors.append(f"{fname}: arquivo contem BOM UTF-8 (salve como UTF-8 sem BOM)")
            continue

        try:
            text = raw.decode("utf-8")
            data = json.loads(text)
        except Exception as exc:
            errors.append(f"{fname}: JSON/UTF-8 invalido: {exc}")
            continue

        if not isinstance(data, list):
            errors.append(f"{fname}: raiz JSON deve ser um array ([...])")
            continue

        if len(data) != fmeta["entry_count"]:
            errors.append(
                f"{fname}: quantidade de itens alterada ({len(data)} encontrado vs {fmeta['entry_count']} esperado)"
            )

        wait_count = 0
        for idx, item in enumerate(data):
            loc = f"{fname}[{idx}]"
            if not isinstance(item, dict):
                errors.append(f"{loc}: item nao e objeto JSON")
                continue
            bad_keys = set(item.keys()) - ALLOWED_KEYS
            if bad_keys:
                errors.append(f"{loc}: chaves inesperadas {sorted(bad_keys)}")
            if "message" not in item or not isinstance(item["message"], str):
                errors.append(f"{loc}: campo 'message' ausente ou nao-string")
                continue
            if "name" in item and not isinstance(item["name"], str):
                errors.append(f"{loc}: campo 'name' deve ser string quando presente")
            if "name" in item:
                check_text(item["name"], f"{loc}.name", errors)
            check_text(item["message"], f"{loc}.message", errors)
            wait_count += item["message"].count("<WAIT>")

        if wait_count != fmeta["wait_tag_count"]:
            errors.append(
                f"{fname}: quantidade de tags <WAIT> alterada ({wait_count} encontrado vs {fmeta['wait_tag_count']} esperado)"
            )

        actual_sha = hashlib.sha256(raw).hexdigest().lower()
        expected_sha = str(fmeta.get("sha256", "")).lower()
        if actual_sha != expected_sha:
            if args.update_hashes:
                fmeta["sha256"] = actual_sha
                hash_updates += 1
            elif not args.skip_hash:
                errors.append(
                    f"{fname}: SHA-256 diverge de metadata.json (got {actual_sha}, want {expected_sha}). "
                    f"Rode 'python3 scripts/validate_repo.py --update-hashes' ao fechar uma versao."
                )

        total_entries += len(data)
        total_wait_tags += wait_count

    if len(expected_files) != meta.get("file_count"):
        errors.append(f"metadata.json: file_count={meta.get('file_count')} mas len(files)={len(expected_files)}")
    if total_entries != meta.get("total_entries"):
        errors.append(f"Total de entradas ({total_entries}) diverge de metadata.json ({meta.get('total_entries')})")

    if errors:
        print(f"VALIDACAO FALHOU ({len(errors)} erro(s)):", file=sys.stderr)
        for err in errors[:50]:
            print(f"  - {err}", file=sys.stderr)
        if len(errors) > 50:
            print(f"  ... e mais {len(errors) - 50} erro(s).", file=sys.stderr)
        return 1

    if args.update_hashes and hash_updates > 0:
        formatted = json.dumps(meta, indent=2, ensure_ascii=False) + "\n"
        meta_path.write_bytes(formatted.encode("utf-8"))
        print(f"Atualizados {hash_updates} hash(es) em metadata.json.")

    mode = "skip-hash" if args.skip_hash else ("update-hashes" if args.update_hashes else "strict-sha256")
    print(
        f"OK ({mode}): {len(expected_files)} arquivos validados, "
        f"{total_entries} entradas, {total_wait_tags} tags <WAIT>."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
