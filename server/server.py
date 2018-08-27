import boto3
import uuid

class Server:
    versionName = ''
    dockerTag = ''
    cfStackName = ''
    liveELBName = ''
    deploymentStackName = ''

    region = 'us-east-1'
    AWSCloudFormationClient = None
    AWSAutoScalingClient = None
    AWSS3Client = None
    AWSElasticLoadBalancingClient = None
    AWSECSClient = None
    AWSEC2Client = None
    AWSAIMClient = None

    def __init__(self, region=""):
        self.AWSCloudFormationClient = boto3.client('cloudformation', region_name=self.region)
        self.AWSAutoScalingClient = boto3.client('autoscaling', region_name=self.region)
        self.AWSS3Client = boto3.client('s3', region_name=region)
        self.AWSElasticLoadBalancingClient = boto3.client('elb', region_name=self.region)
        self.AWSECSClient = boto3.client('ecs', region_name=self.region)
        self.AWSEC2Client = boto3.client('ec2', region_name=self.region)
        self.AWSAIMClient = boto3.client('iam', region_name=self.region)

    def ecsInfrastracture(self):
        print(":ecsInfrastracture:")
        available_services = self.AWSECSClient.list_services()
        available_task = self.AWSECSClient.list_tasks()
        # available_elb = self.AWSEC2Client.describe_load_balancers()
        for service in available_services["serviceArns"]:
            print(":service:" + service)
        for task in available_task["taskArns"]:
            print(":task:" + task)
        self.createTask("redis_programming_version")

    def createServie(self):
        pass

    def createTask(self, name):
        executionRoleArn = self.getExecutionRole("ecsTaskExecutionRole")
        response = self.AWSECSClient.register_task_definition(
            family=name+uuid.uuid4().hex,
            requiresCompatibilities=['FARGATE'],
            networkMode="awsvpc",
            executionRoleArn=executionRoleArn,
            containerDefinitions=self.getContainers(),
            cpu='512',
            memory='2048'
        )
        print(response)

    def getExecutionRole(self, name):
        return self.AWSAIMClient.get_role(RoleName=name)['Role']['Arn']

    def getContainers(self):
        logConfiguration = {"logDriver": "awslogs",
                            "options": {
                                "awslogs-group": "/ecs/redis_20_08_3",
                                "awslogs-region": self.region,
                                "awslogs-stream-prefix": "ecs"
                            }}
        redisPortMappings = list()
        redisPortMappings.append(
            {
                "hostPort": 6379,
                "protocol": "tcp",
                "containerPort": 6379
            }
        ),
        clientportMappings = list()
        clientportMappings.append(
            {
                "hostPort": 80,
                "protocol": "tcp",
                "containerPort": 80
            }),
        clientContainerInit = {
            "logConfiguration": logConfiguration,
            "portMappings": clientportMappings,
            "image": "563665212661.dkr.ecr.us-east-1.amazonaws.com/vadik:latest",
            "memoryReservation": 1024,
            "name": "vadik"}

        redisContainerInit = {
            "logConfiguration": logConfiguration,
            "portMappings": redisPortMappings,
            "image": "redis:latest",
            "memoryReservation": 1024,
            "name": "redis"}
        client = self.generateTask(clientContainerInit)
        redis = self.generateTask(redisContainerInit)
        return [client,redis]

    def atachTaskToService(self):
        pass

    def detachTaskFromService(self):
        pass

    def attachServiceToELB(self):
        pass

    def generateTask(self, dockerInit):
        return {"dnsSearchDomains": [],
                "logConfiguration": dockerInit["logConfiguration"],
                "entryPoint": [],
                "portMappings": dockerInit["portMappings"],
                "command": [],
                "linuxParameters": {},
                "cpu": 0,
                "environment": [],
                "ulimits": [],
                "dnsServers": [],
                "mountPoints": [],
                "workingDirectory": "/usr/app",
                "dockerSecurityOptions": [],
                "memory": dockerInit["memoryReservation"],
                "memoryReservation": dockerInit["memoryReservation"],
                "volumesFrom": [],
                "image": dockerInit["image"],
                "disableNetworking": False,
                "healthCheck": {"command": [""]},
                "essential": True,
                "links": [],
                # "hostname": None,
                "extraHosts": [],
                # "user": "",
                "readonlyRootFilesystem": False,
                "dockerLabels": {},
                "privileged": False,
                "name": dockerInit["name"]
                }


def main():
    serv = Server('us-east-1')
    serv.ecsInfrastracture()


if __name__ == "__main__":
    main()
