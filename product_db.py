#!/usr/bin/env python3
"""
product_db.py

간단한 SQLite 헬퍼 클래스와 샘플 데이터 생성 스크립트.

생성된 DB 파일: MyProduct.db (현재 작업 디렉토리)
테이블: Products(productID INTEGER PRIMARY KEY AUTOINCREMENT, productName TEXT, productPrice INTEGER)

Usage:
    python d:/work/product_db.py --generate 100000

클래스 메서드: insert_product, bulk_insert, update_product, delete_product, get_product, select_all, count_products
"""
import sqlite3
import os
import random
import time
import argparse
from typing import Iterable, List, Optional, Tuple


class ProductDB:
    def __init__(self, db_path: str = "MyProduct.db"):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            # Performance-friendly pragmas for bulk insert
            cur = self.conn.cursor()
            cur.execute("PRAGMA synchronous = OFF")
            cur.execute("PRAGMA journal_mode = MEMORY")
            cur.close()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def create_table(self):
        self.connect()
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Products (
                productID INTEGER PRIMARY KEY AUTOINCREMENT,
                productName TEXT NOT NULL,
                productPrice INTEGER NOT NULL
            )
            """
        )
        self.conn.commit()
        cur.close()

    def insert_product(self, productName: str, productPrice: int) -> int:
        """Insert single product. Returns the inserted productID."""
        self.connect()
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO Products (productName, productPrice) VALUES (?, ?)",
            (productName, productPrice),
        )
        self.conn.commit()
        last = cur.lastrowid
        cur.close()
        return last

    def bulk_insert(self, items: Iterable[Tuple[str, int]], chunk_size: int = 5000) -> int:
        """Insert many items (iterable of (productName, productPrice)). Returns total inserted."""
        self.connect()
        cur = self.conn.cursor()
        total = 0
        items_iter = iter(items)
        batch: List[Tuple[str, int]] = []
        for it in items_iter:
            batch.append(it)
            if len(batch) >= chunk_size:
                cur.executemany(
                    "INSERT INTO Products (productName, productPrice) VALUES (?, ?)", batch
                )
                total += len(batch)
                self.conn.commit()
                batch.clear()
        if batch:
            cur.executemany(
                "INSERT INTO Products (productName, productPrice) VALUES (?, ?)", batch
            )
            total += len(batch)
            self.conn.commit()
        cur.close()
        return total

    def update_product(self, productID: int, productName: Optional[str] = None, productPrice: Optional[int] = None) -> int:
        """Update fields for a product. Returns number of rows updated."""
        if productName is None and productPrice is None:
            return 0
        self.connect()
        cur = self.conn.cursor()
        parts = []
        params: List = []
        if productName is not None:
            parts.append("productName = ?")
            params.append(productName)
        if productPrice is not None:
            parts.append("productPrice = ?")
            params.append(productPrice)
        params.append(productID)
        sql = f"UPDATE Products SET {', '.join(parts)} WHERE productID = ?"
        cur.execute(sql, params)
        self.conn.commit()
        rowcount = cur.rowcount
        cur.close()
        return rowcount

    def delete_product(self, productID: int) -> int:
        """Delete a product by ID. Returns number of rows deleted."""
        self.connect()
        cur = self.conn.cursor()
        cur.execute("DELETE FROM Products WHERE productID = ?", (productID,))
        self.conn.commit()
        rowcount = cur.rowcount
        cur.close()
        return rowcount

    def get_product(self, productID: int) -> Optional[Tuple[int, str, int]]:
        self.connect()
        cur = self.conn.cursor()
        cur.execute("SELECT productID, productName, productPrice FROM Products WHERE productID = ?", (productID,))
        row = cur.fetchone()
        cur.close()
        return row

    def select_all(self, limit: Optional[int] = None, offset: int = 0) -> List[Tuple[int, str, int]]:
        self.connect()
        cur = self.conn.cursor()
        if limit is None:
            cur.execute("SELECT productID, productName, productPrice FROM Products ORDER BY productID LIMIT -1 OFFSET ?", (offset,))
        else:
            cur.execute("SELECT productID, productName, productPrice FROM Products ORDER BY productID LIMIT ? OFFSET ?", (limit, offset))
        rows = cur.fetchall()
        cur.close()
        return rows

    def count_products(self) -> int:
        self.connect()
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM Products")
        n = cur.fetchone()[0]
        cur.close()
        return n


def generate_sample_items(n: int) -> Iterable[Tuple[str, int]]:
    # predictable-ish but fast generator
    for i in range(1, n + 1):
        name = f"Product_{i:06d}"
        price = random.randint(100, 100000)
        yield (name, price)


def main():
    parser = argparse.ArgumentParser(description="Create MyProduct.db and populate Products table with sample data.")
    parser.add_argument("--db", default="MyProduct.db", help="Database file path (default: MyProduct.db)")
    parser.add_argument("--generate", type=int, default=0, help="How many sample rows to generate (0 = skip)")
    parser.add_argument("--chunk", type=int, default=5000, help="Chunk size for bulk insert")
    args = parser.parse_args()

    db_path = args.db
    generator_count = args.generate

    print(f"DB file: {os.path.abspath(db_path)}")

    pdb = ProductDB(db_path=db_path)
    pdb.create_table()

    if generator_count > 0:
        print(f"Generating and inserting {generator_count} items (chunk={args.chunk})...")
        t0 = time.time()
        items = generate_sample_items(generator_count)
        inserted = pdb.bulk_insert(items, chunk_size=args.chunk)
        t1 = time.time()
        print(f"Inserted {inserted} rows in {t1 - t0:.2f} seconds")

        total = pdb.count_products()
        print(f"Total rows in DB now: {total}")

    # Sample select of first/last
    sample = pdb.select_all(limit=5, offset=0)
    if sample:
        print("Sample rows (first 5):")
        for r in sample:
            print(r)

    pdb.close()


if __name__ == "__main__":
    main()
