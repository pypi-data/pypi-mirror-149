from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
    include_package_data=True,
    name='mkdocs-izsam-video',
    version='1.0.2',
    description='MkDocs plugin to insert videos in documentation.',
    long_description_content_type='text/markdown',
    long_description=README + '\n\n' + HISTORY,
    keywords=['MkDocs', 'Video', 'HTML5 video tag'],
    license='MIT',
    packages=find_packages(),
    url='',
    download_url='',
    author='Alessandro De Luca',
    author_email='al.deluca@izs.it',
    python_requires='>=3.8',    
    install_requires=[
        'mkdocs>=1.0.4'
    ],
    entry_points={
        'mkdocs.plugins': [
            'mkdocs-izsam-video = mkdocs_izsam_video.plugin:Plugin',
        ]
    }

)
