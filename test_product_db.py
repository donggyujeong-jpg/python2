import sys
sys.path.insert(0, 'd:\\work')

from product_manager import ProductManager, generate_sample_data

print("=" * 60)
print("SQLite 전자제품 데이터 관리 시스템")
print("=" * 60)

# 1. 데이터베이스 및 테이블 생성
print("\n[1단계] 데이터베이스 생성...")
manager = ProductManager("MyProduct.db")

# 2. 기존 데이터 확인 및 초기화
existing_count = manager.get_count()
print(f"현재 데이터베이스의 제품 개수: {existing_count}")

if existing_count > 0:
    print("기존 데이터를 삭제합니다.")
    manager.delete_all()
    print("✓ 기존 데이터가 삭제되었습니다.")

# 3. 샘플 데이터 생성 및 삽입
print("\n[2단계] 샘플 데이터 생성 중...")
sample_products = generate_sample_data(100000)
print(f"✓ {len(sample_products):,}개의 샘플 데이터가 생성되었습니다.")

print("\n[3단계] 데이터 삽입 중... (이 과정은 1-2분 정도 소요됩니다)")
inserted_count = manager.insert_many(sample_products)
print(f"✓ {inserted_count:,}개의 제품 데이터가 삽입되었습니다.")

# 4. 전체 제품 개수 확인
total_count = manager.get_count()
print(f"\n[4단계] 총 제품 개수: {total_count:,}")

# 5. SELECT 테스트 - 처음 5개 제품 조회
print("\n[5단계] SELECT 테스트 - 처음 5개 제품:")
all_products = manager.select_all()
first_five = all_products[:5]
first_id = first_five[0][0]  # 첫 번째 ID 저장
second_id = first_five[1][0]  # 두 번째 ID 저장

for product in first_five:
    print(f"  ID: {product[0]}, 제품명: {product[1]}, 가격: {product[2]:,}원")

# 6. SELECT 테스트 - ID로 조회
print("\n[6단계] SELECT 테스트 - 첫 번째 제품 ID로 조회:")
product = manager.select_by_id(first_id)
if product:
    print(f"  ID: {product[0]}, 제품명: {product[1]}, 가격: {product[2]:,}원")

# 7. SELECT 테스트 - 제품명으로 조회
print("\n[7단계] SELECT 테스트 - 제품명에 '삼성'이 포함된 제품 (처음 3개):")
products = manager.select_by_name("삼성")[:3]
print(f"  검색 결과: {len(manager.select_by_name('삼성'))}개")
for product in products:
    print(f"  ID: {product[0]}, 제품명: {product[1]}, 가격: {product[2]:,}원")

# 8. SELECT 테스트 - 가격 범위로 조회
print("\n[8단계] SELECT 테스트 - 가격이 100,000 ~ 200,000원인 제품:")
products = manager.select_by_price_range(100000, 200000)
print(f"  검색 결과: {len(products)}개")
for product in products[:3]:
    print(f"  ID: {product[0]}, 제품명: {product[1]}, 가격: {product[2]:,}원")

# 9. UPDATE 테스트
print(f"\n[9단계] UPDATE 테스트 - ID {first_id}인 제품 정보 수정:")
success = manager.update(first_id, product_name="🔥 특가상품! 테스트 제품", product_price=999999)
if success:
    product = manager.select_by_id(first_id)
    print(f"  수정됨: ID: {product[0]}, 제품명: {product[1]}, 가격: {product[2]:,}원")

# 10. DELETE 테스트
print(f"\n[10단계] DELETE 테스트 - ID {second_id}인 제품 삭제:")
success = manager.delete(second_id)
if success:
    print(f"  ✓ ID {second_id}인 제품이 삭제되었습니다.")
    remaining = manager.get_count()
    print(f"  현재 제품 개수: {remaining:,}")

# 11. 최종 개수 확인
final_count = manager.get_count()
print(f"\n[11단계] 최종 제품 개수: {final_count:,}")

# 12. 데이터베이스 연결 종료
manager.close()

print("\n" + "=" * 60)
print("✓ 모든 작업이 완료되었습니다!")
print("=" * 60)
