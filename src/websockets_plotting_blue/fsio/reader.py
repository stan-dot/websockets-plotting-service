

class IOManager:
    def __init__(self):
        self.cache = {}

    def read_image(self, path: str) -> bytes | None:
        """
        Reads an image file from the given path and caches it.

        Args:
            path (str): The path to the image file.

        Returns:
            bytes: The binary content of the image file if successful, else None.
        """
        if path in self.cache:
            return self.cache[path]  # Return cached image if it exists

        try:
            with open(path, "rb") as file:
                image_data = file.read()
                self.cache[path] = image_data  # Cache the result
                return image_data
        except FileNotFoundError:
            print(f"File not found: {path}")
            return None
        except Exception as e:
            print(f"Error reading image from {path}: {e}")
            return None
