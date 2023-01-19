from subprocess import run, PIPE
import os
import gitlab
from time import sleep


def wait_for_pipeline(project, pipeline_id):
    while 1:
        pipeline = project.pipelines.get(pipeline_id)
        if pipeline.status == 'success':
            break
        elif pipeline.status == 'failed':
            assert str(project + pipeline_id) == ''
        sleep(1)


def test_gryphon():
    process = run(['pipenv', 'run', 'python3', '-m', 'build', os.path.abspath("tests/data/pygryphon")])
    assert process.stderr is None
    # Alice
    gl = gitlab.Gitlab('http://localhost:4000', private_token="998b5802ec365e17665d832f3384e975")
    pygryphon_project = gl.projects.get("pygryphon/pygryphon")
    pygryphon_project.packages.get(pygryphon_project.packages.list()[0].id).delete()
    process = run(
        ['pipenv', 'run', 'python3', '-m', 'twine', 'upload', '-r', 'gitlab',
         os.path.abspath("tests/data/pygryphon/dist/*"),
         '--config-file', os.path.abspath("tests/data/pygryphon/.pypirc")])
    assert process.stderr is None
    # Root
    # gl = gitlab.Gitlab('http://localhost:4000', private_token="60b6c7ba41475b2ebdded2c0d3b079f0")
    # awesome_app_project = gl.projects.get("wonderland/awesome-app")
    # awesome_app_pipeline = awesome_app_project.pipelines.create({'ref': 'main'})
    # wait_for_pipeline(awesome_app_project, awesome_app_pipeline.get_id())
    # sleep(2)
    # nest_of_gold_project = gl.projects.get("wonderland/nest-of-gold")
    # nest_of_gold_pipeline = nest_of_gold_project.pipelines.create({'ref': 'main'})
    # wait_for_pipeline(nest_of_gold_project, nest_of_gold_pipeline.get_id())
    # sleep(2)
    sleep(240)
    process = run('docker exec -e DOCKER_HOST=localhost:2376 prod docker logs web', stdout=PIPE, shell=True)
    assert process.stderr is None
    assert "7ED44218-C9CC-4824-BC85-C9841305A642" in str(process.stdout)
