"""Package Configuration"""

from setuptools import setup, find_namespace_packages

setup(
    name="pa_quadro",
    version="1.0.0",
    description="Personal assistant for managing contacts and notes",
    url="https://github.com/Matajur/personal_assistant",
    author="Project Team Quadro",
    author_email="project_team.quadro@gmail.com",
    license="Apache License 2.0",
    packages=find_namespace_packages(),
    install_requires=[],
    include_package_data=True,
    entry_points={"console_scripts": ["qbot = personal_assistant.bot:main"]},
)
