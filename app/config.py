import os


class Settings:
    MEDIA_DIR = "media"
    SUPPORTED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    SUPPORTED_VIDEO_TYPES = ["video/mp4", "video/webm", "video/ogg"]

    def __init__(self):
        os.makedirs(self.MEDIA_DIR, exist_ok=True)


settings = Settings()
