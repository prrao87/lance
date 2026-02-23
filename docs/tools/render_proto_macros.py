#!/usr/bin/env python3
"""Render `%%% proto.message.X %%%` macros into static protobuf code blocks."""

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
FENCE_OPEN_RE = re.compile(r"^(\s*)```([^\s`]*)\s*$")
FENCE_CLOSE_RE = re.compile(r"^\s*```\s*$")


@dataclass
class MessageDef:
    full_name: str
    short_name: str
    snippet: str
    source: Path


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
                        short_name=scope["name"],
                        snippet=snippet,
                        source=proto_file,
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


def render_markdown(markdown: str, messages: list[MessageDef]) -> tuple[str, list[str]]:
    unresolved: list[str] = []
    output_lines: list[str] = []
    fence_lang: str | None = None

    for line in markdown.splitlines(keepends=True):
        open_match = FENCE_OPEN_RE.match(line.rstrip("\n"))
        if fence_lang is None and open_match:
            fence_lang = open_match.group(2).strip().lower()
            output_lines.append(line)
            continue
        if fence_lang is not None and FENCE_CLOSE_RE.match(line.rstrip("\n")):
            fence_lang = None
            output_lines.append(line)
            continue

        macro_match = MACRO_RE.search(line)
        if not macro_match:
            output_lines.append(line)
            continue

        macro = macro_match.group(1)
        resolved = resolve_macro(macro, messages)
        if not resolved:
            unresolved.append(macro)
            output_lines.append(line)
            continue

        indent = line[: len(line) - len(line.lstrip(" \t"))]
        if fence_lang and fence_lang.startswith("protobuf"):
            body = resolved.snippet.splitlines()
            output_lines.extend(f"{indent}{snippet_line}\n" for snippet_line in body)
        else:
            output_lines.append(f"{indent}```protobuf\n")
            output_lines.extend(f"{indent}{snippet_line}\n" for snippet_line in resolved.snippet.splitlines())
            output_lines.append(f"{indent}```\n")

    return "".join(output_lines), unresolved


def transform_docs(input_dir: Path, output_dir: Path | None, proto_dir: Path) -> int:
    if output_dir is None:
        work_dir = input_dir
    else:
        output_dir.parent.mkdir(parents=True, exist_ok=True)
        if output_dir.exists():
            shutil.rmtree(output_dir)
        shutil.copytree(input_dir, output_dir)
        work_dir = output_dir

    messages = load_messages(proto_dir)
    unresolved_total: list[tuple[Path, str]] = []

    for md_file in work_dir.rglob("*.md"):
        original = md_file.read_text(encoding="utf-8")
        updated, unresolved = render_markdown(original, messages)
        if unresolved:
            unresolved_total.extend((md_file, item) for item in unresolved)
        if updated != original:
            md_file.write_text(updated, encoding="utf-8")

    if unresolved_total:
        print("Found unresolved protobuf macros:")
        for path, macro in unresolved_total:
            print(f"  - {path}: {macro}")
        return 1

    print(f"Rendered protobuf macros in {work_dir}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Input docs directory")
    parser.add_argument("--output", type=Path, help="Optional output docs directory")
    parser.add_argument(
        "--proto-dir",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "protos",
        help="Directory containing proto files",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return transform_docs(args.input.resolve(), args.output.resolve() if args.output else None, args.proto_dir.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
