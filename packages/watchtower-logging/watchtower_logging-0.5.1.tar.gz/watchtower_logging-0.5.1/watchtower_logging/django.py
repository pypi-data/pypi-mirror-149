import watchtower_logging

class DjangoWatchTowerHandler(watchtower_logging.watchtower_logging.WatchTowerHandler):

    def __init__(self):

        from django.conf import settings

        token = getattr(settings, 'WT_TOKEN', None)
        protocol = getattr(settings, 'WT_PROTOCOL', 'https')
        dev = getattr(settings, 'WT_DEV', False)
        timeout = getattr(settings, 'WT_TIMEOUT', 1.0)
        retry_count = getattr(settings, 'WT_NUM_RETRY', 1)

        super().__init__(
            beam_id=settings.WT_BEAM_ID,
            token=token,
            protocol=protocol,
            host=settings.WT_HOST,
            flush_interval=-1,
            dev=dev,
            timeout=timeout,
            retry_count=retry_count)