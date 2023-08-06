from . import runbot_docker
def main():
    result = runbot_docker.RunbotResult()
    for line in open("./src/alfred_docker_compose/log_sample.log").readlines():
        result.test_line(line.removesuffix("\n"))

    print(result)
    print(result.res_num)