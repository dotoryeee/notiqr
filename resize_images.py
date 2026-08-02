"""
이미지 리사이징 스크립트
모바일 청첩장용으로 이미지를 적절한 크기로 축소합니다.
"""
import os
from PIL import Image

# 설정
INPUT_DIR = "img"
OUTPUT_DIR = "gallery"
MAX_WIDTH = 1200  # 모바일에서 충분히 고화질로 보이는 크기
JPEG_QUALITY = 85  # JPEG 품질 (0-100)

def resize_image(input_path, output_path, max_width=MAX_WIDTH):
    """이미지를 지정된 최대 너비로 리사이즈"""
    with Image.open(input_path) as img:
        # EXIF 방향 정보 처리
        try:
            from PIL import ExifTags
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = img._getexif()
            if exif is not None:
                orientation_value = exif.get(orientation)
                if orientation_value == 3:
                    img = img.rotate(180, expand=True)
                elif orientation_value == 6:
                    img = img.rotate(270, expand=True)
                elif orientation_value == 8:
                    img = img.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            pass
        
        # RGB로 변환 (RGBA나 P 모드일 경우)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # 리사이즈
        width, height = img.size
        if width > max_width:
            ratio = max_width / width
            new_size = (max_width, int(height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # 저장
        img.save(output_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)
        return img.size

def main():
    # 출력 디렉토리 생성
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 처리할 이미지 파일 목록
    image_extensions = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')
    
    # 파일명으로 정렬하여 순서대로 처리
    image_files = []
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(image_extensions):
            image_files.append(filename)
    
    # 파일명으로 정렬
    image_files.sort()
    
    # 순서대로 처리하여 img_1.jpg, img_2.jpg 형식으로 저장
    for index, filename in enumerate(image_files, start=1):
        input_path = os.path.join(INPUT_DIR, filename)
        
        # 출력 파일명 (img_1.jpg, img_2.jpg 형식)
        output_filename = f"img_{index}.jpg"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        # 원본 파일 크기
        original_size = os.path.getsize(input_path)
        
        # 리사이즈
        new_dimensions = resize_image(input_path, output_path)
        
        # 새 파일 크기
        new_size = os.path.getsize(output_path)
        
        print(f"{filename} -> {output_filename}: {original_size/1024/1024:.1f}MB -> {new_size/1024:.0f}KB ({new_dimensions[0]}x{new_dimensions[1]})")

if __name__ == "__main__":
    main()
    print("\n이미지 최적화 완료!")

