ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

def allowed_file(filename: str) -> bool:
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )