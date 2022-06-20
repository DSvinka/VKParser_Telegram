from app.utils.vk.base import vk


def group_url_to_short_name(url: str):
    return url.split('/')[-1]


def group_get_by_short_name(short_name: str):
    response = vk.groups.getById(
        group_id=short_name,
    )

    return response[0]
