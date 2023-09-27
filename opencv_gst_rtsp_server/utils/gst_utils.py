import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst


class GstUtilities:
    @staticmethod
    def is_element_exist(element_name: str) -> bool:
        """Check if element exist
        Init and get registry before check: 

        import gi
        gi.require_version('Gst', '1.0')
        from gi.repository import Gst

        Gst.init(None)

        """
        element_exists = Gst.ElementFactory.find(element_name) is not None
        return element_exists