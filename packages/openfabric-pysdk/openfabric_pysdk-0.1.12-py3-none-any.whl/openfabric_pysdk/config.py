import os
import pickledb


#######################################################
# Json configuration reader
#######################################################
class OpenfabricJsonConfig:
    __db: pickledb.PickleDB = None

    def __init__(self, file_name):
        self.__db = pickledb.load(file_name, False)

    def get(self, key):
        if not self.__db:
            return None
        return self.__db.get(key) if self.__db.exists(key) else None

    def set(self, key, value):
        self.__db.set(key, value)
        self.__db.dump()

    def all(self):
        return self.__db.db


# Global instance
cwd = os.getcwd()

# Manifest configuration
manifest_config = OpenfabricJsonConfig(f"{cwd}/config/manifest.json")

# Execution configuration
execution_config = OpenfabricJsonConfig(f"{cwd}/config/execution.json")

# State configuration
state_config = OpenfabricJsonConfig(f"{cwd}/config/state.json")
