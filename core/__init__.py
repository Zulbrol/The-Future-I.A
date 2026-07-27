class OrchestratorBrain:

    def __init__(self, file_manager):

        self.file_manager = file_manager

        self.llm = LLMManager()

        self.prompt_builder = PromptBuilder()

        self.task_manager = TaskManager()
        
        self.agent_manager = AgentManager()