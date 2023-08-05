MP4A_PROFILES = {
    'LC': '2',
    'SBR': '5',
    'PS': '29',
}


def get_mp4a_profile(profile: str) -> str:
    return MP4A_PROFILES[profile]
