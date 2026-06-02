from crewai import Task

def create_task(question, agent, campus_data):

    task = Task(
        description=f"""
        Use the following campus information:

        {campus_data}

        Student Question:
        {question}

        Provide a clear and helpful answer.
        """,
        expected_output="A detailed answer for the student's query.",
        agent=agent
    )

    return task