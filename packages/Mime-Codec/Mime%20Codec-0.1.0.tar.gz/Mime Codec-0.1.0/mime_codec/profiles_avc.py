from typing import Tuple

AVC_PROFILES = {
    'Constrained Baseline': ('42', '40'),
    'Baseline': ('42', '00'),
    'Extended': ('58', '00'),
    'Main': ('4D', '00'),
    'Constrained Main': ('4D', '40'),
    'High': ('64', '00'),
    'Progressive High': ('64', '08'),
    'Constrained High': ('64', '0C'),
    'High 10': ('6E', '00'),
    'High 4:2:2': ('7A', '00'),
    'High 4:4:4 Predictive': ('F4', '00'),
    'High 10 Intra': ('6E', '10'),
    'High 4:2:2 Intra': ('7A', '10'),
    'High 4:4:4 Intra': ('F4', '10'),
    'CAVLC 4:4:4 Intra': ('44', '00'),
    'Scalable Baseline': ('53', '00'),
    'Scalable Constrained Baseline': ('53', '04'),
    'Scalable High': ('56', '00'),
    'Scalable Constrained High': ('56', '04'),
    'Scalable High Intra': ('56', '20'),
    'Stereo High': ('80', '00'),
    'Multiview High': ('76', '00'),
    'Multiview Depth High': ('8A', '00')
}


def get_avc_profile(profile: str) -> Tuple[str, str]:
    return AVC_PROFILES[profile]
