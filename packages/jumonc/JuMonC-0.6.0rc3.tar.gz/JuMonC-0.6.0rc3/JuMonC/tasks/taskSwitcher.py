import logging

from queue import Queue

from typing import List, Optional


from JuMonC.tasks import taskID
from JuMonC import settings



logger = logging.getLogger(__name__)



def notyetdefined(data: List[int]) -> None:
    print(data)

class taskSwitcher:
    pending_tasks: Queue = Queue(settings.PENDING_TASKS_SOFT_LIMIT + settings.MAX_THREADS_PER_TASK * settings.MAX_WORKER_THREADS + 1)
    
    def __init__(self) -> None:
        """Singelton class that switches taks depending on id."""
        self.switch_dic = {
            # General commands

            taskID.finalize : notyetdefined,


            # Job commands



            # CPU commands

            taskID.meassure_cpu_load : notyetdefined,
            taskID.retrieve_cpu_load : notyetdefined,

            taskID.meassure_cpu_frequency : notyetdefined,


            # GPU commands

            taskID.meassure_gpu_load : notyetdefined,
            taskID.retrieve_gpu_load : notyetdefined,

            taskID.meassure_gpu_frequency : notyetdefined,


            # Network commands



            # IO commands



            # General application commands



            # Alya commands
            
            
        }
        
    def executeNextTask(self) -> None:
        data = self.pending_tasks.get()
        logging.debug("Executing task: %s", str(data))
        task = self.switch_dic.get(data[0], lambda data: logging.warning("Invalid taskID: %s", str(data[0])))
        task(data)
        self.pending_tasks.task_done()
        
    def addTask(self, data: Optional[List[int]]) -> None:
        if data is not None:
            self.pending_tasks.put(data)

        
tasks = taskSwitcher()