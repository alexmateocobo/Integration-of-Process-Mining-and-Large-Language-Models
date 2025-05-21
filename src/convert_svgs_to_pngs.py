import os
import cairosvg

def convert_svg_to_png(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith(".svg"):
            svg_path = os.path.join(folder_path, file)
            png_path = os.path.splitext(svg_path)[0] + ".png"
            print(f"Converting {svg_path} → {png_path}")
            cairosvg.svg2png(url=svg_path, write_to=png_path)

if __name__ == "__main__":
    convert_svg_to_png("data/process_models/04-Self-service-restaurant")