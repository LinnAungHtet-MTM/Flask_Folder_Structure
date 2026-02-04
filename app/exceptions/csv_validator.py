
from app.dao.postdao import PostDao
from app.exceptions.business_exception import BusinessException

REQUIRED_HEADERS = {"title", "description", "status"}


class PostCsvValidator:

    # Validate CSV Header
    @staticmethod
    def validate_headers(headers: list[str]):
        if not headers:
            raise BusinessException(
                field="file",
                message="CSV file has no header row"
            )

        if not REQUIRED_HEADERS.issubset(set(headers)):
            raise BusinessException(
                field="file",
                message=f"CSV headers must contain: {', '.join(REQUIRED_HEADERS)}"
            )

    # Validate CSV Row
    @staticmethod
    def validate_row(row: dict, row_number: int):
        title = (row.get("title") or "").strip()
        description = (row.get("description") or "").strip()

        if not title:
            raise BusinessException(
                field="file",
                message="Title is required",
                row=row_number
            )

        if not description:
            raise BusinessException(
                field="file",
                message="Description is required",
                row=row_number
            )

        if len(title) > 255:
            raise BusinessException(
                field="file",
                message="Title must not exceed 255 characters",
                row=row_number
            )

        # DB duplicate check
        if PostDao.find_by_title(title):
            raise BusinessException(
                field="file",
                message="Title already exists",
                row=row_number
            )

        # Status
        raw_status = row.get("status", 1)
        try:
            status = int(raw_status)
        except (TypeError, ValueError):
            raise BusinessException(
                field="file",
                message="Status must be an integer",
                row=row_number
            )

        if status not in (0, 1):
            raise BusinessException(
                field="file",
                message="Status must be 0 or 1",
                row=row_number
            )

        return {
            "title": title,
            "description": description,
            "status": status
        }
