import os
import shutil
from pathlib import Path

# 다운로드 폴더 경로
DOWNLOADS_FOLDER = r"C:\Users\USER\Downloads"

# 파일 분류 규칙
FILE_CATEGORIES = {
    r"\images": [".jpg", ".jpeg"],
    r"\data": [".csv", ".xlsx"],
    r"\docs": [".txt", ".doc", ".pdf"],
    r"\archive": [".zip"]
}

def create_folders_if_not_exist(base_path, folders):
    """필요한 폴더가 없으면 생성"""
    for folder in folders:
        folder_path = os.path.join(base_path, folder.lstrip("\\"))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"✓ 폴더 생성: {folder_path}")
        else:
            print(f"✓ 폴더 이미 존재: {folder_path}")

def get_destination_folder(file_extension, base_path):
    """파일 확장자에 따라 목적지 폴더 결정"""
    file_extension = file_extension.lower()
    
    for category_folder, extensions in FILE_CATEGORIES.items():
        if file_extension in extensions:
            return os.path.join(base_path, category_folder.lstrip("\\"))
    
    return None

def organize_files(downloads_path):
    """다운로드 폴더의 파일들을 분류해서 이동"""
    
    # 경로 유효성 확인
    if not os.path.exists(downloads_path):
        print(f"오류: {downloads_path} 폴더가 존재하지 않습니다.")
        return
    
    print(f"대상 폴더: {downloads_path}\n")
    
    # 필요한 폴더 생성
    print("=" * 50)
    print("1단계: 필요한 폴더 생성 중...")
    print("=" * 50)
    create_folders_if_not_exist(downloads_path, FILE_CATEGORIES.keys())
    
    print("\n" + "=" * 50)
    print("2단계: 파일 이동 중...")
    print("=" * 50)
    
    # 다운로드 폴더의 모든 파일 순회
    move_count = 0
    skip_count = 0
    
    for filename in os.listdir(downloads_path):
        file_path = os.path.join(downloads_path, filename)
        
        # 폴더는 제외하고 파일만 처리
        if os.path.isdir(file_path):
            continue
        
        # 파일 확장자 추출
        file_extension = os.path.splitext(filename)[1]
        
        # 목적지 폴더 결정
        destination_folder = get_destination_folder(file_extension, downloads_path)
        
        if destination_folder:
            destination_path = os.path.join(destination_folder, filename)
            
            try:
                # 파일이 이미 목적지에 있으면 스킵
                if os.path.exists(destination_path):
                    print(f"⊘ 이미 존재 (스킵): {filename}")
                    skip_count += 1
                else:
                    shutil.move(file_path, destination_path)
                    print(f"✓ 이동 완료: {filename} → {destination_folder}")
                    move_count += 1
            except Exception as e:
                print(f"✗ 오류 발생 ({filename}): {str(e)}")
        else:
            skip_count += 1
            if file_extension:
                print(f"⊘ 미분류 파일: {filename} (확장자: {file_extension})")
            else:
                print(f"⊘ 확장자 없는 파일: {filename}")
    
    print("\n" + "=" * 50)
    print("작업 완료!")
    print("=" * 50)
    print(f"이동된 파일: {move_count}개")
    print(f"처리되지 않은 파일: {skip_count}개")

if __name__ == "__main__":
    organize_files(DOWNLOADS_FOLDER)
