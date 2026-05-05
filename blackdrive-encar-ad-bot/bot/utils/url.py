from urllib.parse import parse_qs, urlparse


def is_encar_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.netloc.endswith("encar.com") and "/cars/detail/" in parsed.path


def extract_car_id(url: str) -> str | None:
    parsed = urlparse(url)
    query_car_id = parse_qs(parsed.query).get("carid")
    if query_car_id and query_car_id[0].isdigit():
        return query_car_id[0]

    path_parts = [p for p in parsed.path.split("/") if p]
    try:
        detail_idx = path_parts.index("detail")
        candidate = path_parts[detail_idx + 1]
        if candidate.isdigit():
            return candidate
    except (ValueError, IndexError):
        return None
    return None
