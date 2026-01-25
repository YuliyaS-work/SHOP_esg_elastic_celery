from PIL import Image, ImageOps
import os

input_folder = "media_origin/electro"
output_folder = "media/electro"
target_size1 = (800, 800)  # размер для карточек
target_size2 = (300, 300)  # размер для карточек

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        img_path = os.path.join(input_folder, filename)
        try:
            img = Image.open(img_path)

            # Приведение к квадрату с белым фоном
            img_square1 = ImageOps.pad(img, target_size1, color="white")
            img_square2 = ImageOps.pad(img, target_size2, color="white")

            # Новое имя файла с расширением .webp
            base_name = os.path.splitext(filename)[0]
            output_path1 = os.path.join(output_folder, "800_" + base_name + ".webp")
            output_path2 = os.path.join(output_folder, "300_" + base_name + ".webp")

            # Сохранение в формате WebP
            img_square1.save(output_path1, format="WEBP", quality=95)
            img_square2.save(output_path2, format="WEBP", quality=95)
        except Exception as e:
            print(f"Ошибка при обработке {filename}: {e}")

print("Все изображения приведены к единому виду и сохранены в формате WebP!")

