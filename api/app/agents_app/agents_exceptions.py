class OrchestratorError(Exception):
	def __init__(self, message: str):
		super().__init__(message)

class SubAgentError(Exception):
	def __init__(self, message: str, agent: str, action: str, step: str):
		super().__init__(message)
		self.agent = agent
		self.action = action
		self.step = step