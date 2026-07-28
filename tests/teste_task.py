from core.task_manager import TaskManager

task_manager = TaskManager()

task = task_manager.criar_task(
    "Landing Page para Pizzaria"
)

print(task)