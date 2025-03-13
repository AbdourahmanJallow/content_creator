from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, callback
from crewai_tools import (
	WebsiteSearchTool,
	SerperDevTool,
	DirectoryReadTool,
	FileReadTool
)
import os

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# MODEL = os.getenv("MODEL")

# tools
search_tool = SerperDevTool()
# web_rag_tool = WebsiteSearchTool()
file_tool = FileReadTool()

@CrewBase
class ContentCreator():
	"""ContentCreator crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def trend_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['trend_researcher'],
			tools=[search_tool],
			verbose=True
		)

	@agent
	def concept_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['concept_analyst'],
			verbose=True
		)

	@agent
	def content_creator(self) -> Agent:
		return Agent(
			config=self.agents_config['content_creator'],
			tools=[file_tool],
			verbose=True
		)


	@task
	def trend_research_task(self) -> Task:
		return Task(
			config=self.tasks_config['trend_research_task'],
		)

	@task
	def concept_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['concept_analysis_task'],
		)

	@task
	def content_creation_task(self) -> Task:
		return Task(
			config=self.tasks_config['content_creation_task'],
			output_file='output/backend_trends.md'
		)

	@callback
	def log_task_completion(self, task: Task):
		print(f"Task {task.description} completed")
		print(f"Agent used: {task.agent.name}")


	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)
