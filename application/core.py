import logging
import os
from enum import Enum

from PIL import Image, ImageDraw, ImageFont


logger = logging.getLogger(__name__)


class Coordinates:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"{self.latitude:.6f}, {self.longitude:.6f}"


class DrugType(Enum):
    marijuana = "шш"


class Unit(Enum):
    g = "г"


class Product:
    def __init__(self, amount: float, drug: DrugType = DrugType.marijuana, unit: Unit = Unit.g):
        self.amount = amount
        self.drug = drug
        self.unit = unit

    def __str__(self):
        return f"{self.drug.value} {self.amount}{self.unit.value}"


class Photo:
    def __init__(self, photo_id: str, coordinates: Coordinates, product: Product = None, area: str = None):
        self.photo_id = photo_id
        self.coordinates = coordinates
        self.product = product
        self.area = area
        self.input_path = f"resources/photos/input/{self.photo_id}.jpg"
        self.output_path = f"resources/photos/output/{self.photo_id}.jpg"

    def save(self) -> str:
        image = Image.open(self.input_path)
        draw = ImageDraw.Draw(image)
        font_size = 35

        try:
            font = ImageFont.truetype("/Library/Fonts/Arial.ttf", size=font_size)
        except IOError:
            font = ImageFont.load_default(size=font_size)

        text = str(self.coordinates)
        if self.product:
            text += f" | {self.product}"
        if self.area:
            text += f" | {self.area}"

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        padding = 10
        rect_height = text_height + padding * 2
        rect_y = image.height - rect_height

        background_coords = [
            (0, rect_y),
            (image.width, image.height)
        ]
        draw.rectangle(background_coords, fill="black")

        text_x = (image.width - text_width) // 2
        text_y = rect_y + padding

        draw.text((text_x, text_y), text, fill="white", font=font)

        image.save(self.output_path)
        logger.info(f"Photo saved: {self.output_path}")
        return self.output_path

    @staticmethod
    def delete(path: str):
        try:
            os.remove(path)

        except FileNotFoundError:
            logger.warning(f"File not found: {path}")

        else:
            logger.info(f"File deleted: {path}")


    def __del__(self):
        self.delete(self.input_path)
        self.delete(self.output_path)
