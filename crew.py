from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# Initialize tools
search_tool = SerperDevTool()

# Agents
task_breakdown_agent = Agent(
    role='Project Task Breakdown Specialist',
    goal="Understand the student's project topic and description,"
         "break it into detailed, actionable tasks, and communicate this to other agents.",
    verbose=True,
    memory=True,
    tools=[],
    backstory="You are an expert at decomposing complex projects"
              "into manageable tasks. You ensure projects start with a"
              "clear and organized plan."
)

technology_research_agent = Agent(
    role='Technology Research Expert',
    goal='Identify the best technologies for the project tasks.',
    verbose=True,
    memory=True,
    tools=[search_tool],
    backstory="Enthusiastic about exploring the latest open-source technologies."
)

analysis_agent = Agent(
    role='Technology Selection Specialist',
    goal='Your goal is to serve as the primary decision-maker in evaluating and'
        'selecting the most suitable technologies for project tasks.',
    verbose=True,
    memory=True,
    tools=[],
    backstory='With years of experience in technology evaluation'
            'and a reputation for precision and insight, you are the' 
            'cornerstone of informed decision-making in the organization.'
            'Your deep understanding of current and emerging technologies,' 
            'combined with a structured approach to critical analysis, allows' 
            'you to identify the best tools for every challenge. You pride yourself' 
            'on staying ahead of industry trends and translating complex technological' 
            'assessments into clear, actionable decisions. Whether the task is optimizing' 
            'existing workflows or innovating entirely new systems, your expertise ensures' 
            'the selection of technologies that maximize efficiency, adaptability, and long-term success.'
)

architecture_agent = Agent(
    role='Project Architecture Designer',
    goal='To craft a project architecture and roadmap that guides the execution team through each phase of the project.',
    verbose=True,
    memory=True,
    tools=[],
    backstory="As the final decision-maker for the project's design framework,"
            "you are a master at translating diverse inputs into a unified plan."
            "With a sharp understanding of system workflows and a talent for orchestrating"
            "complex processes, you bridge the gap between strategy and execution."
            "You thrive on collaboration, leveraging insights from agents specializing in"
            "task decomposition, technology research, and analysis to ensure every design decision"
            "aligns with the project's overarching goals."
            "Your deep knowledge of architecture principles and process optimization enables you"
            "to anticipate challenges and create robust, future-proof systems."
)

project_management_agent = Agent(
    role='Project Management Coordinator',
    goal='Compile a final, guided project plan for students.',
    verbose=True,
    memory=True,
    tools=[],
    backstory="Orchestrates and delivers polished project plans."
)

# Tasks
task_breakdown = Task(
    description="Break the student's project into detailed, actionable tasks.",
    expected_output="A structured list of tasks with descriptions.",
    agent=task_breakdown_agent,
)

technology_research = Task(
    description="Research the latest technologies relevant to the tasks.",
    expected_output="A comprehensive list of technologies categorized by relevance.",
    agent=technology_research_agent,
)

analysis = Task(
    description='You have the task of systematically analyzing options provided by the research agent,'
        'assessing each technology\'s capabilities, compatibility, scalability,'
        'cost-efficiency, and alignment with project ({project_topic}) and ({project_description}) requirements. Your recommendations'
        'are backed by thorough analysis and insights, ensuring that every choice enhances'
        'project outcomes and aligns with project goals.',
    expected_output="A detailed technology analysis report that includes: "
        "1) A prioritized list of technologies evaluated for each task with justifications for selections. "
        "2) Final technology recommendations aligned with project requirements, ensuring clarity and actionable insights.",
    agent=analysis_agent,
)

architecture_design = Task(
    description="Design the overall architecture and process flow of the project ({project_topic}) and ({project_description})."
        "You will synthesize all prior research and decisions into a cohesive and actionable project architecture."
        "Using the detailed task breakdown from the Task Breakdown Agent,"
        "and the technology selections made by the Technology Analysis Specialist,"
        "you design the flow, structure, and integration points of the project."
        "Your primary responsibility is to establish a seamless process that optimally connects tasks,"
        "technologies, and dependencies, ensuring that every component works in harmony to meet the project objectives.",
    expected_output= "A detailed project architecture document that includes two components: "
        "1) A structured task table with columns for task name, assigned technology, dependencies, "
        "and priority, providing a clear breakdown of all project tasks. "
        "2) A visual flow diagram illustrating the sequential flow of tasks, dependencies, "
        "technology integration, decision points, and grouped phases such as Planning, Execution, "
        "Testing, and Deployment. "
        "The document should ensure clarity, consistency, and alignment with the project's goals, "
        "serving as both a blueprint for execution and a reference for stakeholders.",
    agent=architecture_agent,
)

project_plan_compilation = Task(
    description="Compile all outputs into a cohesive project plan.",
    expected_output="A complete project plan in Markdown format.",
    agent=project_management_agent,
)

# Crew
crew = Crew(
    agents=[task_breakdown_agent, technology_research_agent, analysis_agent, architecture_agent, project_management_agent],
    tasks=[task_breakdown, technology_research, analysis, architecture_design, project_plan_compilation],
    process=Process.sequential
)

# Kick off the crew with student inputs
inputs = {
    'project_topic': 'AI-based Sentiment Analysis for Social Media',
    'project_description': 'A tool to analyze user sentiment on social media using AI and provide detailed insights.'
}
result = crew.kickoff(inputs=inputs)
print(result)
