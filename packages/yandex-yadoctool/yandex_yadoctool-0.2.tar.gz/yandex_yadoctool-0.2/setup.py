from setuptools import setup, find_packages

setup(name='yandex_yadoctool',
      python_requires='>3.5.2',
      version='0.2',
      description='Dita-docs tool',
      entry_points={
          'console_scripts':
              ['yadoctool = yandex_yadoctool.main:main'],
      },
      install_requires=[
          "requests"
      ],
      packages=find_packages(),
      author_email='anokhin-b@yandex-team.ru',      
      zip_safe=False)