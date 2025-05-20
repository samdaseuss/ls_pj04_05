# 'modules' 디렉토리가 없을 경우를 대비하여 생성하는 코드 예시
import os
from pathlib import Path

# 프로젝트 루트 디렉토리 찾기
def find_project_root():
    current_dir = Path(os.getcwd())
    
    while current_dir.name != 'ls_pj04_5' and current_dir.parent != current_dir:
        current_dir = current_dir.parent
    
    if current_dir.parent == current_dir:
        print("경고: 프로젝트 루트 디렉토리를 찾지 못했습니다. 현재 디렉토리를 사용합니다.")
        current_dir = Path(os.getcwd())
    
    return current_dir

# 모듈 디렉토리 생성
def create_modules_directory():
    root_dir = find_project_root()
    modules_dir = root_dir / "modules"
    
    if not modules_dir.exists():
        try:
            # 디렉토리 생성
            modules_dir.mkdir(parents=True, exist_ok=True)
            print(f"모듈 디렉토리가 생성되었습니다: {modules_dir}")
        except Exception as e:
            print(f"모듈 디렉토리 생성 중 오류가 발생했습니다: {str(e)}")
    else:
        print(f"모듈 디렉토리가 이미 존재합니다: {modules_dir}")
    
    return modules_dir

if __name__ == "__main__":
    # 모듈 디렉토리 생성
    modules_dir = create_modules_directory()
    
    # __init__.py 파일 생성 (모듈로 인식하기 위함)
    init_file = modules_dir / "__init__.py"
    if not init_file.exists():
        try:
            with open(init_file, 'w') as f:
                f.write("# 모듈 패키지 초기화 파일")
            print(f"__init__.py 파일이 생성되었습니다: {init_file}")
        except Exception as e:
            print(f"__init__.py 파일 생성 중 오류가 발생했습니다: {str(e)}")
    else:
        print(f"__init__.py 파일이 이미 존재합니다: {init_file}")
    
    print("\n모듈 디렉토리 설정이 완료되었습니다.")
    print("이제 map_utils.py 파일을 modules 디렉토리에 복사하거나 이동시키세요.")