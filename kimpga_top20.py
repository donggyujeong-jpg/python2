#!/usr/bin/env python3
"""
kimpga_top20.py

웹사이트 https://kimpga.com/ 에서 상위 N개(기본 20) 코인 정보를 가져와
JSON 및 CSV로 저장하고 표준 출력으로도 보여주는 간단한 스크래퍼입니다.

사용법:
    python kimpga_top20.py            # 기본적으로 상위 20개
    python kimpga_top20.py --top 10   # 상위 10개

참고: 사이트 구조 변경에 대비해 여러 파싱 전략(테이블, 리스트, 스크립트 내 JSON)을 시도합니다.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from typing import List, Dict, Optional

import requests
from bs4 import BeautifulSoup


DEFAULT_URL = "https://kimpga.com/"


def fetch_html(url: str, timeout: int = 15) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def _clean_text(s: Optional[str]) -> str:
    if not s:
        return ""
    return re.sub(r"\s+", " ", s).strip()


def parse_table_rows(rows, top_n: int) -> List[Dict]:
    results = []
    for i, r in enumerate(rows[:top_n]):
        cols = r.find_all(["td", "th"]) or []
        texts = [_clean_text(c.get_text(" ", strip=True)) for c in cols]

        # Heuristic mapping: rank/name/price/premium/url
        rank = None
        name = None
        symbol = None
        price = None
        premium = None
        url = None

        # Try to find anchor for name
        a = r.find("a")
        if a:
            name = _clean_text(a.get_text())
            url = a.get("href")

        # Find price-like and percent-like columns
        for t in texts:
            if price is None and re.search(r"[₩$€¥]|\d{1,3}(,\d{3})+(\.\d+)?", t):
                price = t
            if premium is None and ("%" in t or re.search(r"프리미엄|Premium", t, re.I)):
                premium = t
            if rank is None and re.match(r"^\d+$", t):
                rank = t

        if not name and texts:
            # try first textual column that isn't purely numeric
            for t in texts:
                if not re.match(r"^\d+$", t):
                    name = t
                    break

        if not rank:
            rank = str(i + 1)

        results.append({
            "rank": rank,
            "name": name or "",
            "symbol": symbol or "",
            "price": price or "",
            "premium": premium or "",
            "url": url or "",
            "raw_cols": texts,
        })

    return results


def parse_html_for_coins(html: str, top_n: int = 20) -> List[Dict]:
    soup = BeautifulSoup(html, "lxml")

    # 1) 가장 일반적인 경우: <table> 형식으로 상위 코인들이 정리되어 있음
    tables = soup.find_all("table")
    for table in tables:
        try:
            tbody = table.find("tbody") or table
            rows = tbody.find_all("tr")
            if len(rows) >= 1:
                parsed = parse_table_rows(rows, top_n)
                if parsed:
                    return parsed
        except Exception:
            continue

    # 2) div/li 리스트 형식
    selectors = [
        "div.coin", "li.coin", ".coin-row", ".market-row", ".crypto-row", ".coinListRow",
    ]
    for sel in selectors:
        rows = soup.select(sel)
        if rows:
            results = []
            for r in rows[:top_n]:
                text = _clean_text(r.get_text(" ", strip=True))
                a = r.find("a")
                name = _clean_text(a.get_text()) if a else text.split()[0:2]
                price_match = re.search(r"[₩$€¥]\s*[\d,]+(?:\.\d+)?", text)
                pct_match = re.search(r"-?\d+\.?\d*%", text)
                results.append({
                    "rank": "",
                    "name": name if isinstance(name, str) else " ".join(name),
                    "symbol": "",
                    "price": price_match.group(0) if price_match else "",
                    "premium": pct_match.group(0) if pct_match else "",
                    "url": a.get("href") if a else "",
                    "raw_text": text,
                })
            if results:
                return results

    # 3) 페이지에 JSON 데이터가 포함된 경우 (스크립트 변수, window.__INITIAL_STATE__ 등)
    # 매우 일반적인 패턴을 몇 가지 시도
    js_patterns = [r"window\.__INITIAL_STATE__\s*=\s*(\{.*?\})\s*;", r"var\s+initialData\s*=\s*(\[.*?\])\s*;"]
    for p in js_patterns:
        m = re.search(p, html, re.S)
        if m:
            try:
                data = json.loads(m.group(1))
                # 탐색해 코인 목록을 찾아 반환 — 구조가 다를 수 있으므로 간단히 시도
                if isinstance(data, dict):
                    # look for keys with coin/market
                    for k, v in data.items():
                        if isinstance(v, list) and len(v) and isinstance(v[0], dict):
                            # take first list of dicts
                            return [
                                {
                                    "rank": item.get("rank") or item.get("no") or "",
                                    "name": item.get("name") or item.get("coin") or "",
                                    "symbol": item.get("symbol") or item.get("abbr") or "",
                                    "price": item.get("price") or item.get("value") or "",
                                    "premium": item.get("premium") or "",
                                    "url": item.get("url") or "",
                                }
                                for item in v[:top_n]
                            ]
            except Exception:
                pass

    # 실패 시 빈 리스트 반환
    return []


def save_json(data: List[Dict], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_csv(data: List[Dict], path: str) -> None:
    if not data:
        return
    # flatten keys from first item
    keys = list(data[0].keys())
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def main(argv=None):
    p = argparse.ArgumentParser(description="kimpga.com 상위 N개 코인 크롤러")
    p.add_argument("--url", default=DEFAULT_URL, help="크롤링할 URL (기본: kimpga.com)")
    p.add_argument("--top", type=int, default=20, help="가져올 상위 코인 수")
    p.add_argument("--out-json", default="kimpga_top.json", help="저장할 JSON 파일 경로")
    p.add_argument("--out-csv", default="kimpga_top.csv", help="저장할 CSV 파일 경로")
    args = p.parse_args(argv)

    try:
        html = fetch_html(args.url)
    except Exception as e:
        print(f"[ERROR] 페이지를 가져오지 못했습니다: {e}")
        sys.exit(2)

    items = parse_html_for_coins(html, top_n=args.top)

    if not items:
        print("크롤링 결과가 비어있습니다. 사이트 구조가 변경되었을 수 있습니다.")
        sys.exit(1)

    # 출력
    print(json.dumps(items, ensure_ascii=False, indent=2))

    save_json(items, args.out_json)
    save_csv(items, args.out_csv)

    print(f"저장 완료: {args.out_json}, {args.out_csv}")


if __name__ == "__main__":
    main()
