def get_extension(page):
    return mime_lookup(get_mime_type(page))

def get_mime_type(page):
    """
    Extracts the Content-Type header from the headers returned by page.
    """
    try:
        doc_type = str(page.headers['Content-Type'], 'utf-8')
        return doc_type
    except KeyError:  # If no Content-Type was returned, return blank
        return ''


def mime_lookup(value):
    """
    Finds the correct file extension for a MIME type using the MIME_TYPES dictionary.
    If the MIME type is blank it defaults to .html,
    and if the MIME type is not in the dictionary it raises a HeaderError.
    """
    value = value.lower()  # Reduce to lowercase
    value = value.split(';')[0]  # Remove possible encoding
    if value in MIME_TYPES:
        return MIME_TYPES[value]
    elif value == '':
        return '.html'
    else:
        # pass
        raise Exception('Unknown MIME type: {0}'.format(value))

# Sourced mainly from https://www.iana.org/assignments/media-types/media-types.xhtml
# Added by hand after being discovered by the crawler to reduce lookup times.
MIME_TYPES = {
    'application/atom+xml': '.atom',
    'application/epub+zip': '.epub',
    'application/font-woff': '.woff',
    'application/font-woff2': '.woff2',
    'application/force-download': '.bin',  # No idea what this is so saving as .bin
    'application/gzip': '.gz',
    'application/java-archive': '.jar',
    'application/javascript': '.js',
    'application/js': '.js',  # Should be application/javascript
    'application/json': '.json',
    'application/json+oembed': '.json',
    'application/ld+json': '.jsonld',
    'application/marcxml+xml': '.mrcx',
    'application/msword': '.doc',
    'application/n-triples': '.nt',
    'application/octet-stream': '.exe',  # Sometimes .bin
    'application/ogg': '.ogx',
    'application/opensearchdescription+xml': '.osdx',
    'application/pdf': '.pdf',
    'application/postscript': '.eps',  # Also .ps
    'application/rdf+xml': '.rdf',
    'application/rsd+xml': '.rsd',
    'application/rss+xml': '.rss',
    'application/txt': '.txt',
    'application/vnd.ms-cab-compressed': '.cab',
    'application/vnd.ms-excel': '.',
    'application/vnd.ms-fontobject': '.eot',
    'application/x-endnote-refer': '.enw',
    'application/x-www-form-urlencoded': '.png',
    'application/vnd.android.package-archive': '.apk',
    'application/vnd.oasis.opendocument.text': '.odt',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
    'application/vnd.oasis.opendocument.formula-template': '.otf',
    'application/vnd.php.serialized': '.php',
    'application/x-bibtex': '.bib',
    'application/x-font-ttf': '.ttf',
    'application/x-font-woff': '.woff',
    'application/x-gzip': '.gz',
    'application/x-javascript': '.js',
    'application/x-mobipocket-ebook': '.mobi',
    'application/x-mpegurl': '.m3u8',
    'application/x-msi': '.msi',
    'application/x-research-info-systems': '.ris',
    'application/x-rss+xml': '.rss',
    'application/x-shockwave-flash': '.swf',
    'application/x-tar': '.tar.gz',  # Tarballs aren't official IANA types
    'application/xhtml+xml': '.xhtml',
    'application/xml': '.xml',
    'application/zip': '.zip',
    'audio/mpeg': '.mp3',
    'audio/mp3': '.mp3',
    'applicaton/octet-stream': '.mp3',
    'audio/mp4': '.mp4',
    'audio/x-m4a': '.m4a',
    'binary/octet-stream': '.exe',  # Should be application/octet-stream
    'font/woff': '.woff', 'font/woff2': '.woff2',
    'font/ttf': '.ttf',
    'font/otf': '.otf',
    'html': '.html',  # Incorrect
    'image/gif': '.gif',
    'image/jpeg': '.jpg',
    'image/jpg': '.jpg',
    'image/pjpeg': '.jpg',
    'image/png': '.png',
    'image/ico': '.ico',
    'image/svg+xml': '.svg',
    'image/tiff': '.tif',
    'image/vnd.djvu': '.djvu',
    'image/vnd.microsoft.icon': '.ico',
    'image/webp': '.webp',
    'image/x-bitmap': '.xbm',
    'image/x-icon': '.ico',
    'image/x-ms-bmp': '.bmp',
    'text/calendar': '.ics',
    'text/css': '.css',
    'text/csv': '.csv',
    'text/directory': '.vcf',
    'text/html': '.html',
    'text/html,application/xhtml+xml,application/xml': '.html',  # Misunderstood 'Accept' header?
    'text/javascript': '.js',
    'text/n3': '.n3',
    'text/plain': '.txt',
    'text/turtle': '.ttl',
    'text/vnd.wap.wml': '.xml',  # or .wml
    'text/vtt': '.vtt',
    'text/x-c': '.c',
    'text/x-wiki': '.txt',  # Doesn't seem to have a filetype of its own
    'text/xml charset=utf-8': '.xml',  # Shouldn't have encoding
    'text/xml': '.xml',  # Incorrect
    'video/3gpp': '.3gp',
    'video/3gp': '.3gp',
    'video/mp4': '.mp4',
    'video/webm': '.webp',
    'video/mpeg': '.mpeg',
    'video/x-flv': '.flv',
    'vnd.ms-fontobject': '.eot'  # Incorrect
}

