import os
from PIL import Image
import sys

def get_sticker_image(main_folder):
    supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    for filename in os.listdir(main_folder):
        if filename.lower().endswith(supported_formats):
            return os.path.join(main_folder, filename)
    return None

def apply_stickers():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_folder = os.path.join(script_dir, "main")
    input_folder = os.path.join(script_dir, "needed_picture")
    output_folder = os.path.join(script_dir, "finish_picture")
    
    print("=" * 60)
    print("              批量贴纸工具")
    print("=" * 60)
    print()
    
    if not os.path.exists(main_folder):
        os.makedirs(main_folder)
        print(f"❌ 已创建 main 文件夹")
        print(f"请把贴纸图片放入 main 文件夹")
        return
    
    sticker_path = get_sticker_image(main_folder)
    if not sticker_path:
        print(f"❌ 在 main 文件夹中没有找到图片")
        print(f"请把贴纸图片放入 main 文件夹")
        return
    
    print(f"✅ 找到贴纸: {os.path.basename(sticker_path)}")
    
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
        print(f"❌ 已创建 needed_picture 文件夹")
        print(f"请把需要添加贴纸的图片放入 needed_picture 文件夹")
        return
    
    os.makedirs(output_folder, exist_ok=True)
    
    try:
        sticker = Image.open(sticker_path).convert('RGBA')
    except Exception as e:
        print(f"❌ 无法打开贴纸图片: {e}")
        return
    
    supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    images = [f for f in os.listdir(input_folder) if f.lower().endswith(supported_formats)]
    
    if len(images) == 0:
        print(f"❌ 在 needed_picture 文件夹中没有找到图片")
        print(f"请把需要添加贴纸的图片放入 needed_picture 文件夹")
        return
    
    print(f"✅ 找到 {len(images)} 张待处理图片")
    print(f"✅ 开始添加贴纸到左下角...")
    print()
    
    count = 0
    for filename in images:
        try:
            background = Image.open(os.path.join(input_folder, filename)).convert('RGBA')
            bg_width, bg_height = background.size
            
            sticker_ratio = 0.2
            sticker_width = int(bg_width * sticker_ratio)
            sticker_height = int(sticker.height * (sticker_width / sticker.width))
            sticker_resized = sticker.resize((sticker_width, sticker_height), Image.Resampling.LANCZOS)
            
            padding = 0
            x = padding
            y = bg_height - sticker_height - padding
            
            result = Image.new('RGBA', background.size)
            result.paste(background, (0, 0))
            result.paste(sticker_resized, (x, y), sticker_resized)
            
            if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
                result = result.convert('RGB')
            
            output_path = os.path.join(output_folder, filename)
            result.save(output_path)
            print(f"✓ {filename}")
            count += 1
            
        except Exception as e:
            print(f"✗ {filename} 处理失败: {e}")
    
    print()
    print("=" * 60)
    print(f"✅ 处理完成! 共 {count} 张图片")
    print(f"输出位置: {output_folder}")
    print("=" * 60)

if __name__ == "__main__":
    apply_stickers()
    input("\n按回车键退出...")

