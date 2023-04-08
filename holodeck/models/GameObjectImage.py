from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
import uuid as uuid_pkg
import PIL.Image as Image

from ..generate.generate_image import generate_image



class GameObjectImage(SQLModel, table=True):
    __tablename__ = "image"

    id: Optional[int] = Field(default=None, primary_key=True)

    # id: uuid_pkg.UUID = Field(
    #     default_factory=uuid_pkg.uuid4,
    #     primary_key=True,
    #     index=True,
    #     nullable=False,
    # )
    prompt: str = Field()
    removed: bool = Field(default=False, nullable=True)
    generated: bool = Field(default=False, nullable=True)


    async def generate(self):
        print(f">> requesting image for prompt: '{self.prompt}'<<<")
        image_bytes = await generate_image(prompt=self.prompt)
        print(">> received image!")
        image = Image.open(image_bytes)
        image_file_name = f".images/{self.id}.png"
        image.save(image_file_name)
        image.close()
        image_bytes.close()
        del image_bytes
        self.generated = True
        return self