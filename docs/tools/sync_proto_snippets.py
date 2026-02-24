#!/usr/bin/env python3
"""Sync protobuf snippets and macro references in docs markdown.

This script does two things:
1. Replaces `%%% alias.message.Name %%%` placeholders with snippet includes.
2. Writes snippet files under `src/assets/snippets/proto/` from `../protos/*.proto`.
"""

from __future__ import annotations

import argparse
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

MACRO_RE = re.compile(r"%%%\s*([A-Za-z0-9_.]+)\s*%%%")
TOKEN_RE = re.compile(
    r"//[^\n]*|/\*.*?\*/|\"(?:\\.|[^\"\\])*\"|\bmessage\s+([A-Za-z_][A-Za-z0-9_]*)\s*\{|[{}]",
    re.DOTALL,
)


@dataclass(frozen=True)
class MessageDef:
    full_name: str
    short_name: str
    snippet: str


def parse_proto_messages(proto_file: Path) -> list[MessageDef]:
    text = proto_file.read_text(encoding="utf-8")
    pkg_match = re.search(r"^\s*package\s+([A-Za-z0-9_.]+)\s*;", text, flags=re.MULTILINE)
    package = pkg_match.group(1) if pkg_match else ""

    messages: list[MessageDef] = []
    stack: list[dict[str, object]] = []
    depth = 0

    for match in TOKEN_RE.finditer(text):
        token = match.group(0)
        message_name = match.group(1)

        if token.startswith("//") or token.startswith("/*") or token.startswith('"'):
            continue

        if message_name:
            parents = [scope["name"] for scope in stack]
            depth += 1
            stack.append(
                {
                    "name": message_name,
                    "parents": parents,
                    "start": match.start(),
                    "start_depth": depth,
                }
            )
            continue

        if token == "{":
            depth += 1
            continue

        if token == "}":
            if stack and stack[-1]["start_depth"] == depth:
                scope = stack.pop()
                name_parts = [*scope["parents"], scope["name"]]
                full_name = ".".join(name_parts)
                if package:
                    full_name = f"{package}.{full_name}"
                snippet = text[scope["start"] : match.end()].strip()
                messages.append(
                    MessageDef(
                        full_name=full_name,
                        short_name=str(scope["name"]),
                        snippet=snippet,
                    )
                )
            depth = max(0, depth - 1)

    return messages


def load_messages(proto_dir: Path) -> list[MessageDef]:
    messages: list[MessageDef] = []
    for proto_file in sorted(proto_dir.glob("*.proto")):
        messages.extend(parse_proto_messages(proto_file))
    return messages


def resolve_macro(macro: str, messages: list[MessageDef]) -> MessageDef | None:
    if ".message." not in macro:
        return None
    alias, target = macro.split(".message.", 1)
    target = target.strip()
    if not target:
        return None

    candidates: list[tuple[int, MessageDef]] = []
    for message in messages:
        score = 0
        full = message.full_name
        short = message.short_name

        if "." in target:
            if full == target:
                score += 100
            if full.endswith(f".{target}"):
                score += 90
        else:
            if short == target:
                score += 60
            if full.endswith(f".{target}"):
                score += 40

        if alias == "proto" and full.startswith("lance."):
            score += 10
        if alias == "mem_wal" and full.startswith("lance.table."):
            score += 10

        if score > 0:
            candidates.append((score, message))

    if not candidates:
        return None

    candidates.sort(key=lambda item: (item[0], len(item[1].full_name)), reverse=True)
    return candidates[0][1]


def rewrite_markdown_markers(docs_dir: Path, messages: list[MessageDef]) -> tuple[int, set[MessageDef]]:
    rewritten_files = 0
    unresolved: list[tuple[Path, str]] = []
    used_messages: set[MessageDef] = set()

    for md_file in docs_dir.rglob("*.md"):
        original = md_file.read_text(encoding="utf-8")
        out_lines: list[str] = []
        changed = False

        for line in original.splitlines(keepends=True):
            macro_match = MACRO_RE.search(line)
            if not macro_match:
                out_lines.append(line)
                continue

            macro = macro_match.group(1)
            resolved = resolve_macro(macro, messages)
            if resolved is None:
                unresolved.append((md_file, macro))
                out_lines.append(line)
                continue

            used_messages.add(resolved)
            indent = line[: len(line) - len(line.lstrip(" \t"))]
            newline = "\n" if line.endswith("\n") else ""
            include = f'{indent}--8<-- "assets/snippets/proto/{resolved.full_name}.proto"{newline}'
            out_lines.append(include)
            changed = True

        updated = "".join(out_lines)
        if changed and updated != original:
            md_file.write_text(updated, encoding="utf-8")
            rewritten_files += 1

    if unresolved:
        lines = [f"  - {path}: {macro}" for path, macro in unresolved]
        raise RuntimeError("Unresolved protobuf macros:\n" + "\n".join(lines))

    return rewritten_files, used_messages


def write_snippets(output_dir: Path, used_messages: set[MessageDef]) -> int:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for message in sorted(used_messages, key=lambda x: x.full_name):
        path = output_dir / f"{message.full_name}.proto"
        path.write_text(f"{message.snippet}\n", encoding="utf-8")

    return len(used_messages)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "src",
        help="Path to markdown docs root",
    )
    parser.add_argument(
        "--proto-dir",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "protos",
        help="Path to proto files root",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "src/assets/snippets/proto",
        help="Path to generated snippet directory",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    messages = load_messages(args.proto_dir.resolve())
    rewritten_files, used_messages = rewrite_markdown_markers(args.docs_dir.resolve(), messages)
    snippet_count = write_snippets(args.output_dir.resolve(), used_messages)
    print(f"Updated {rewritten_files} markdown files and wrote {snippet_count} protobuf snippets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
