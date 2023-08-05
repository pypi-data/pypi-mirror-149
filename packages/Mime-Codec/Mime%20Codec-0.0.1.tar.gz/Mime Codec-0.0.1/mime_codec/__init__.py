import mimetypes
import ffmpeg


def get_codecs(file_path: str):
    probe = ffmpeg.probe(file_path)
    return list(map(lambda x: x['codec_name'], probe['streams']))


def get_mime_type(file_path: str, fallback: str = 'video/mp4'):
    mime_type = mimetypes.guess_type(file_path)[0]
    if mime_type is None:
        mime_type = fallback
    return mime_type


def get_mime_codec(file_path: str):
    mime_type = get_mime_type(file_path)
    codecs = get_codecs(file_path)

    return '{0}; codecs="{1}"'.format(mime_type, ','.join(codecs))
