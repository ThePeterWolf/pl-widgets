

import os


class resourceLoader():
    base_folder = os.path.split(__file__)[0]
    
    @classmethod
    def getIconPath(cls, icon_name: str) -> str:
        return os.path.join(cls.base_folder,"resources", "icons", icon_name)

