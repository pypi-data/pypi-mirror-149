from JuMonC.tasks import Plugin

class NvidiaPlugin(Plugin.Plugin):
    
    def _isWorking(self) -> bool:
        return False