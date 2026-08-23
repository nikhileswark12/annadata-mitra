class PipelineManager:
    def __init__(self):
        self.steps = []

    def add_step(self, func):
        self.steps.append(func)

    def execute(self, initial_data):
        data = initial_data
        for step in self.steps:
            data = step(data)
        return data
