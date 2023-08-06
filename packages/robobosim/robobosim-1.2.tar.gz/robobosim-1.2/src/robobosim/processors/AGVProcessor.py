from robobosim.processors.AbstractProcessor import AbstractProcessor
from robobosim.utils.Message import Message

class AGVProcessor(AbstractProcessor):
    def __init__(self, state):
        super().__init__(state)

    def process(self, status):
        name = status["name"]
        value = status["value"]

    def loadItem(self, robot_id):
        name = "SIM-LOAD-ITEM"
        values = {
            "id" : robot_id
        }
        id = self.state.getId()
        return Message(name, values, id)
    
    def unloadItem(self, robot_id):
        name = "SIM-UNLOAD-ITEM"
        values = {
            "id" : robot_id
        }
        id = self.state.getId()
        return Message(name, values, id)
