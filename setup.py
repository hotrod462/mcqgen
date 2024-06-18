from setuptools import find_packages,setup

setup(
	name='mcqgenerator',
	version='0.0.1',
	author='hotrod46',
	author_email='aryanjain4623@gmail.com',
	install_requires=["langchain","streamlit","python-dotenv","PyPDF2","langchain-google-genai","langchain-groq"],
	packages=find_packages()
)
