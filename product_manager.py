import sqlite3
import os
from typing import List, Tuple, Optional

class ProductManager:
    """SQLite 데이터베이스를 사용하여 전자제품 데이터를 관리하는 클래스"""
    
    def __init__(self, db_name: str = "MyProduct.db"):
        """
        데이터베이스 초기화
        
        Args:
            db_name (str): 데이터베이스 파일명
        """
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_table()
    
    def connect(self):
        """데이터베이스 연결"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"✓ '{self.db_name}' 데이터베이스에 연결되었습니다.")
        except sqlite3.Error as e:
            print(f"✗ 데이터베이스 연결 오류: {e}")
    
    def create_table(self):
        """Products 테이블 생성"""
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS Products (
                productID INTEGER PRIMARY KEY AUTOINCREMENT,
                productName TEXT NOT NULL,
                productPrice INTEGER NOT NULL
            );
            """
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("✓ Products 테이블이 준비되었습니다.")
        except sqlite3.Error as e:
            print(f"✗ 테이블 생성 오류: {e}")
    
    def insert(self, product_name: str, product_price: int) -> bool:
        """
        단일 제품 삽입
        
        Args:
            product_name (str): 제품명
            product_price (int): 제품 가격
        
        Returns:
            bool: 성공 여부
        """
        try:
            insert_query = """
            INSERT INTO Products (productName, productPrice)
            VALUES (?, ?)
            """
            self.cursor.execute(insert_query, (product_name, product_price))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"✗ 데이터 삽입 오류: {e}")
            return False
    
    def insert_many(self, products: List[Tuple[str, int]]) -> int:
        """
        다중 제품 삽입 (대량 데이터 추가용)
        
        Args:
            products (List[Tuple[str, int]]): [(제품명, 가격), ...] 형태의 리스트
        
        Returns:
            int: 삽입된 행의 수
        """
        try:
            insert_query = """
            INSERT INTO Products (productName, productPrice)
            VALUES (?, ?)
            """
            self.cursor.executemany(insert_query, products)
            self.connection.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            print(f"✗ 대량 데이터 삽입 오류: {e}")
            return 0
    
    def select_all(self) -> List[Tuple]:
        """
        모든 제품 조회
        
        Returns:
            List[Tuple]: [(productID, productName, productPrice), ...]
        """
        try:
            select_query = "SELECT * FROM Products ORDER BY productID"
            self.cursor.execute(select_query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"✗ 데이터 조회 오류: {e}")
            return []
    
    def select_by_id(self, product_id: int) -> Optional[Tuple]:
        """
        특정 ID의 제품 조회
        
        Args:
            product_id (int): 제품 ID
        
        Returns:
            Optional[Tuple]: (productID, productName, productPrice) 또는 None
        """
        try:
            select_query = "SELECT * FROM Products WHERE productID = ?"
            self.cursor.execute(select_query, (product_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"✗ 데이터 조회 오류: {e}")
            return None
    
    def select_by_name(self, product_name: str) -> List[Tuple]:
        """
        제품명으로 제품 조회
        
        Args:
            product_name (str): 제품명
        
        Returns:
            List[Tuple]: 일치하는 모든 제품
        """
        try:
            select_query = "SELECT * FROM Products WHERE productName LIKE ?"
            self.cursor.execute(select_query, (f"%{product_name}%",))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"✗ 데이터 조회 오류: {e}")
            return []
    
    def select_by_price_range(self, min_price: int, max_price: int) -> List[Tuple]:
        """
        가격 범위로 제품 조회
        
        Args:
            min_price (int): 최소 가격
            max_price (int): 최대 가격
        
        Returns:
            List[Tuple]: 가격 범위에 해당하는 제품
        """
        try:
            select_query = """
            SELECT * FROM Products 
            WHERE productPrice BETWEEN ? AND ?
            ORDER BY productPrice
            """
            self.cursor.execute(select_query, (min_price, max_price))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"✗ 데이터 조회 오류: {e}")
            return []
    
    def update(self, product_id: int, product_name: str = None, product_price: int = None) -> bool:
        """
        제품 정보 업데이트
        
        Args:
            product_id (int): 제품 ID
            product_name (str): 변경할 제품명 (None이면 유지)
            product_price (int): 변경할 가격 (None이면 유지)
        
        Returns:
            bool: 성공 여부
        """
        try:
            if product_name is None and product_price is None:
                print("✗ 수정할 정보를 입력해주세요.")
                return False
            
            if product_name is not None and product_price is not None:
                update_query = """
                UPDATE Products 
                SET productName = ?, productPrice = ?
                WHERE productID = ?
                """
                self.cursor.execute(update_query, (product_name, product_price, product_id))
            elif product_name is not None:
                update_query = """
                UPDATE Products 
                SET productName = ?
                WHERE productID = ?
                """
                self.cursor.execute(update_query, (product_name, product_id))
            else:
                update_query = """
                UPDATE Products 
                SET productPrice = ?
                WHERE productID = ?
                """
                self.cursor.execute(update_query, (product_price, product_id))
            
            self.connection.commit()
            
            if self.cursor.rowcount == 0:
                print(f"✗ ID {product_id}인 제품이 없습니다.")
                return False
            return True
        except sqlite3.Error as e:
            print(f"✗ 데이터 업데이트 오류: {e}")
            return False
    
    def delete(self, product_id: int) -> bool:
        """
        제품 삭제
        
        Args:
            product_id (int): 제품 ID
        
        Returns:
            bool: 성공 여부
        """
        try:
            delete_query = "DELETE FROM Products WHERE productID = ?"
            self.cursor.execute(delete_query, (product_id,))
            self.connection.commit()
            
            if self.cursor.rowcount == 0:
                print(f"✗ ID {product_id}인 제품이 없습니다.")
                return False
            return True
        except sqlite3.Error as e:
            print(f"✗ 데이터 삭제 오류: {e}")
            return False
    
    def delete_all(self) -> bool:
        """
        모든 제품 삭제
        
        Returns:
            bool: 성공 여부
        """
        try:
            delete_query = "DELETE FROM Products"
            self.cursor.execute(delete_query)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"✗ 모든 데이터 삭제 오류: {e}")
            return False
    
    def get_count(self) -> int:
        """
        전체 제품 개수 조회
        
        Returns:
            int: 제품 개수
        """
        try:
            count_query = "SELECT COUNT(*) FROM Products"
            self.cursor.execute(count_query)
            return self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"✗ 개수 조회 오류: {e}")
            return 0
    
    def close(self):
        """데이터베이스 연결 종료"""
        if self.connection:
            self.connection.close()
            print("✓ 데이터베이스 연결을 종료했습니다.")
    
    def __del__(self):
        """소멸자"""
        self.close()


def generate_sample_data(count: int = 100000) -> List[Tuple[str, int]]:
    """
    샘플 전자제품 데이터 생성
    
    Args:
        count (int): 생성할 데이터 개수
    
    Returns:
        List[Tuple[str, int]]: [(제품명, 가격), ...] 형태의 리스트
    """
    import random
    
    product_types = [
        "노트북", "데스크톱", "태블릿", "스마트폰", "이어폰",
        "마우스", "키보드", "모니터", "프린터", "스캐너",
        "카메라", "드론", "라우터", "허브", "외장하드"
    ]
    
    brands = [
        "삼성", "LG", "HP", "델", "에이수스",
        "레노버", "소니", "캐논", "파나소닉", "필립스"
    ]
    
    products = []
    for i in range(count):
        product_type = random.choice(product_types)
        brand = random.choice(brands)
        model_num = random.randint(1000, 9999)
        product_name = f"{brand} {product_type} {model_num}"
        product_price = random.randint(50000, 5000000)  # 50,000 ~ 5,000,000 원
        products.append((product_name, product_price))
    
    return products


# === 실행 예제 ===
if __name__ == "__main__":
    print("=" * 60)
    print("SQLite 전자제품 데이터 관리 시스템")
    print("=" * 60)
    
    # 1. 데이터베이스 및 테이블 생성
    manager = ProductManager("MyProduct.db")
    
    # 2. 기존 데이터 확인 및 초기화
    existing_count = manager.get_count()
    print(f"\n현재 데이터베이스의 제품 개수: {existing_count}")
    
    if existing_count > 0:
        manager.delete_all()
        print("✓ 기존 데이터가 삭제되었습니다.")
    
    # 3. 샘플 데이터 생성 및 삽입
    print("\n샘플 데이터 생성 중...")
    sample_products = generate_sample_data(100000)
    
    print("데이터 삽입 중... (이 과정은 시간이 걸릴 수 있습니다)")
    inserted_count = manager.insert_many(sample_products)
    print(f"✓ {inserted_count:,}개의 제품 데이터가 삽입되었습니다.")
    
    # 4. 전체 제품 개수 확인
    total_count = manager.get_count()
    print(f"\n총 제품 개수: {total_count:,}")
    
    # 5. SELECT 테스트 - 처음 5개 제품 조회
    print("\n[SELECT 테스트] 처음 5개 제품:")
    products = manager.select_all()[:5]
    for product in products:
        print(f"  ID: {product[0]}, 제품명: {product[1]}, 가격: {product[2]:,}원")
    
    # 6. SELECT 테스트 - ID로 조회
    print("\n[SELECT 테스트] ID 1인 제품 조회:")
    product = manager.select_by_id(1)
    if product:
        print(f"  ID: {product[0]}, 제품명: {product[1]}, 가격: {product[2]:,}원")
    
    # 7. SELECT 테스트 - 제품명으로 조회
    print("\n[SELECT 테스트] 제품명에 '삼성'이 포함된 제품 (처음 3개):")
    products = manager.select_by_name("삼성")[:3]
    for product in products:
        print(f"  ID: {product[0]}, 제품명: {product[1]}, 가격: {product[2]:,}원")
    
    # 8. SELECT 테스트 - 가격 범위로 조회
    print("\n[SELECT 테스트] 가격이 100,000 ~ 200,000원인 제품 (처음 3개):")
    products = manager.select_by_price_range(100000, 200000)[:3]
    for product in products:
        print(f"  ID: {product[0]}, 제품명: {product[1]}, 가격: {product[2]:,}원")
    
    # 9. UPDATE 테스트
    print("\n[UPDATE 테스트] ID 1인 제품 정보 수정:")
    success = manager.update(1, product_name="테스트 제품", product_price=999999)
    if success:
        product = manager.select_by_id(1)
        print(f"  수정됨: ID: {product[0]}, 제품명: {product[1]}, 가격: {product[2]:,}원")
    
    # 10. DELETE 테스트
    print("\n[DELETE 테스트] ID 2인 제품 삭제:")
    success = manager.delete(2)
    if success:
        print("  ✓ ID 2인 제품이 삭제되었습니다.")
    
    # 11. 최종 개수 확인
    final_count = manager.get_count()
    print(f"\n최종 제품 개수: {final_count:,}")
    
    # 12. 데이터베이스 연결 종료
    manager.close()
    
    print("\n" + "=" * 60)
    print("작업 완료!")
    print("=" * 60)
