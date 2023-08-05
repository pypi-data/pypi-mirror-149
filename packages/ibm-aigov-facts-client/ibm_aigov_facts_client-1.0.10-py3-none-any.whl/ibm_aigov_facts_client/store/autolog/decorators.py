from .autolog_utils import *


_logger = logging.getLogger(__name__)

class clean_payload(object):
    def format_tags():
        def wrapper(func):
            def wrapped(*args, **kwargs):
                _logger.debug(
                    "Current Data....... {}".format(args[0].current_data))
                clean_tags(args[0].current_data.tags, args[0].run_id)
                changed_tags = rename_tags(args[0].current_data.tags)
                args[0].current_data.tags.clear()
                args[0].current_data.tags.update(changed_tags)
                # set_guid_tag(args[0].run_id)
                return func(*args, **kwargs)
            return wrapped
        return wrapper