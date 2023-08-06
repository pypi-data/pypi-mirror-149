# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['plasticorigins',
 'plasticorigins.detection',
 'plasticorigins.detection.centernet',
 'plasticorigins.detection.centernet.networks',
 'plasticorigins.serving',
 'plasticorigins.tools',
 'plasticorigins.tracking']

package_data = \
{'': ['*'], 'plasticorigins.serving': ['templates/*']}

install_requires = \
['Flask==2.0.3',
 'Werkzeug==2.0.3',
 'debugpy==1.5.1',
 'gunicorn==19.10.0',
 'imgaug==0.4.0',
 'opencv-python==4.5.5.62',
 'psycopg2-binary==2.9.3',
 'pycocotools==2.0.4',
 'pykalman>=0.9.5,<0.10.0',
 'scikit-video>=1.1.11,<2.0.0',
 'scipy==1.7.3',
 'torch>=1.11.0,<2.0.0',
 'torchvision>=0.12.0,<0.13.0',
 'tqdm==4.62.3']

setup_kwargs = {
    'name': 'plastic-origins',
    'version': '1.1.2a0',
    'description': 'A package containing methods commonly used to make inferences',
    'long_description': "# Automated object counting on riverbanks\n\n## Project Branches:\n\n### release:\n\nThis is the main/production branch (DO NOT PUSH DIRECTLY TO RELEASE)\n### dev: \n\nThis is the developpement branch (DO NOT PUSH DIRECTLY TO DEV)\n### Feature Branches\n\nThese are the branches where you can develop new features for the project. In order to create a feature branch:\n\n- Make sure that your **dev** branch is up to date\n    ```shell\n    git checkout dev\n    git pull dev\n    ```\n- Create a new branch from **dev** with the name **feature/name_of_your_feature**\n    ```shell\n    git checkout -b feature/name_of_your_feature\n    ```\n- Once your feature developpement is complete, make a Pull Request of your feature branch to **dev**\n### Research Branches: \n\nThese are branches made for research purposes and they are named **research/name_of_your_subject**\n## Release Branch - Installation\n\nFollow these steps in that order exactly:\n\n### Clone the project\n```shell\ngit clone https://github.com/surfriderfoundationeurope/surfnet.git <folder-for-surfnet> -b release\ncd <folder-for-surfnet>\n```\n### Install Poetry\n```shell\npip install poetry\n```\n\n### Create your virtual environment\nHere we use python version 3.8\n```shell\npoetry use 3.8\n```\n\n### Install dependencies\n```shell\npoetry install\n```\n\n### Code Linting and Formatting:\n\npre-commits have been added to format and check the linting of the code before any commit. This process will run:\n- PyUpgrade: to make sure that the code syntax is up to date with the latest python versions\n- Black: which is a code formatter \n- Flake8: to check that the code is properly formatted.\n\nAll this process is automatic to ensure the commited code quality. So as a good measure, prior to committing any code it is highly recommended to run:\n```shell\npoetry run black path/to/the/changed/code/directory(ies)\n```\nThis will format the code that has been written and:\n```shell\npoetry run flake8 path/to/the/changed/code/directory(ies)\n```\nto check if there is any other issues to fix.\n## Downloading pretrained models\n\nYou can download MobileNetV3 model with the following script:\n```shell\ncd models\nsh download_pretrained_base.sh\n```\nThe file will be downloaded into [models](models).\n\n## Validation videos\n\nIf you want to download the 3 test videos on the 3 portions of the Auterrive riverbank, run:\n\n```\ncd data\nsh download_validation_videos.sh\n```\n\nThis will download the 3 videos in distinct folders of [data/validation_videos](data/validation_videos).\n\n## Serving\n\n### Development\nSetting up the server and testing: from surfnet/ directory, you may run a local flask developement server with the following command:\n\n```shell\nexport FLASK_APP=src/plasticorigins/serving/app.py\npoetry run flask run\n```\n\n### Production\nSetting up the server and testing: from surfnet/ directory, you may run a local wsgi gunicorn production server with the following command:\n\n```shell\nPYTHONPATH=./src gunicorn -w 5 --threads 2 --bind 0.0.0.0:8001 --chdir ./src/serving/ wsgi:app\n```\n\n### Test surfnet API\nThen, in order to test your local dev server, you may run:\n```shell\ncurl -X POST http://127.0.0.1:5000/ -F 'file=@/path/to/video.mp4' # flask\n```\nChange port 5000 to 8001 to test on gunicorn or 8000 to test with Docker and gunicorn.\n\n### Docker\nYou can build and run the surfnet AI API within a Docker container.\n\nDocker Build:\n```shell\ndocker build -t surfnet/surfnet:latest .\n```\n\nDocker Run:\n```shell\ndocker run --env PYTHONPATH=/src -p 8000:8000 --name surfnetapi surfnet/surfnet:latest\n```\n\n### Makefile\nYou can use the makefile for convenience purpose to launch the surfnet API:\n```shell\nmake surfnet-dev-local # with flask\nmake surfnet-prod-local # with gunicorn\nmake surfnet-prod-build-docker # docker build\nmake surfnet-prod-run-docker # docker run\n```\n\n### Kubernetes\nTo ease production operation, the surfnet API can be deployed on top of kubernetes (k8s) cluster. A pre-built Docker image is available on ghcr.io to be deployed using the surfnet.yaml k8s deployment file. To do so, change directory to k8s/, then once you are connected to your k8s cluster simply enter:\n```shell\nkubectl apply -y surfnet.yaml\n```\nRemark: we use a specific surfnet k8s node pool label for our Azure production environment on aks. If you want to test deployment on a default k8s cluster using system nodes, you have either to use default surfnet.yaml file or remove the nodeSelector section from others deployment files (aks, gke).\n\nAfter the deployment is done, create a service to expose the surfnet API to be publicly accessible over the Internet.\n```shell\nkubectl expose deployment surfnet --type=LoadBalancer --name=surfnet-api\nkubectl get service surfnet-api\n```\n\n## Release plasticorigins to pypi:\n\n### Prerelease: (Pull Request to Dev branch)\n#### Check or Bump version:\n\nCheck the current version of the product:\n\nDocker Build:\n```shell\npoetry version\n```\n\nBump the version to the product:\n\n```shell\npoetry version <bump-rule>\n```\nbump rules can be found in : https://python-poetry.org/docs/cli/#:~:text=with%20concrete%20examples.-,RULE,-BEFORE\n**choose carefully the one that corresponds to your bump: for the prerelease we will use:**\n- **prepatch**\n- **preminor**\n- **premajor**\n\nmake sure that in you pyproject.toml your version ends with **-alpha.0**\n\n#### Publish the prerelease to pypi:\n\nIn order to publish your prerelease to PyPi, all you need to do is open a Pull Request of your current branch to **Dev** branch. Once the PR is approved and merged, the Prerelease will be done automatically with a github workflow.\n\n### Release: (Pull Request to Release branch):\nIn order to publish a release version to PyPi, all you have to do is open a Pull Request of the **Dev** branch into the **Release** branch. Once the PR is approved and merged, the Release will be done automatically with a github workflow.\n\n## Testing:\nTo launch the tests you can run this command\n```shell\npoetry run coverage run -m pytest -s && poetry run coverage report -m\n```\n## Configuration\n\n`src/serving/inference.py` contains a Configuration dictionary that you may change:\n- `skip_frames` : `3` number of frames to skip. Increase to make the process faster and less accurate.\n- `kappa`: `7` the moving average window. `1` prevents the average, avoid `2` which is ill-defined.\n- `tau`: `4` the number of consecutive observations necessary to keep a track. If you increase `skip_frames`, you should lower `tau`.\n\n## Datasets and Training\n\nConsider other branches for that!\n",
    'author': 'Chayma Mesbahi',
    'author_email': 'chayma.mesbahi@neoxia.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.plasticorigins.eu/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
