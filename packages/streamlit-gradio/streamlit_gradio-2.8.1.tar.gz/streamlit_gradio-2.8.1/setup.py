try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='streamlit_gradio',
    version='2.8.1',
    include_package_data=True,
    description='A streamlit wrapper for gradio',
    author='Rishikesh Anand',
    author_email='rishi1998@gmail.com',
    url='https://github.com/truefoundry/streamlit-gradio',
    packages=['streamlit_gradio'],
    license='Apache License 2.0',
    keywords=['machine learning', 'visualization', 'reproducibility'],
    install_requires=[
        'streamlit',
        'numpy',
        'pydub',
        'matplotlib',
        'pandas',
        'pillow',
        'ffmpy',
        'markdown2',
        'pycryptodome',
        'requests',
        'paramiko',
        'analytics-python',
    ],
)
