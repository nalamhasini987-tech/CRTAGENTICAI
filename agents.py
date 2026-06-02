from crewai import Agent

campus_info_agent = Agent(
    role="Campus Information Expert",
    goal="Provide accurate information about the campus",
    backstory="You know all details about departments, offices, facilities, and student services.",
    verbose=True
)

navigation_agent = Agent(
    role="Campus Navigation Guide",
    goal="Help students locate buildings and offices",
    backstory="You are an expert guide for navigating the university campus.",
    verbose=True
)

faq_agent = Agent(
    role="Student Support Assistant",
    goal="Answer common student queries",
    backstory="You help students with campus facilities and support services.",
    verbose=True
)

event_agent = Agent(
    role="Campus Event Coordinator",
    goal="Provide information about events and activities",
    backstory="You know all campus events and celebrations.",
    verbose=True
)