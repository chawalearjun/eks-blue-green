import subprocess
import sys

DOCKER_USER = "<your-dockerhub-username>"
AWS_REGION = "us-east-1"
CLUSTER_NAME = "blue-green-eks"

def run_cmd(cmd):
    print(f"\n[Running] {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def create_eks():
    run_cmd("cd terraform && terraform init")
    run_cmd("cd terraform && terraform apply -auto-approve")
    run_cmd(f"aws eks update-kubeconfig --region {AWS_REGION} --name {CLUSTER_NAME}")

def deploy_jenkins():
    run_cmd("kubectl apply -f jenkins/jenkins-deployment.yaml")
    run_cmd("kubectl apply -f jenkins/jenkins-service.yaml")

def build_and_push_images():
    run_cmd(f"docker build -t {DOCKER_USER}/blue-app:latest app/blue")
    run_cmd(f"docker push {DOCKER_USER}/blue-app:latest")
    run_cmd(f"docker build -t {DOCKER_USER}/green-app:latest app/green")
    run_cmd(f"docker push {DOCKER_USER}/green-app:latest")

def deploy_apps():
    run_cmd("kubectl apply -f app/deployment-blue.yaml")
    run_cmd("kubectl apply -f app/deployment-green.yaml")
    run_cmd("kubectl apply -f app/service.yaml")

def switch_traffic(version):
    if version not in ["blue", "green"]:
        print("Error: version must be blue or green")
        sys.exit(1)
    run_cmd(f"kubectl patch service demo-service -p '{{\"spec\":{{\"selector\":{{\"app\":\"demo\",\"version\":\"{version}\"}}}}}}'")
    print(f"✅ Traffic switched to {version}")

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--switch":
        switch_traffic(sys.argv[2])
    elif len(sys.argv) == 1:
        create_eks()
        deploy_jenkins()
        build_and_push_images()
        deploy_apps()
        switch_traffic("blue")
    else:
        print("Usage: python scripts/setup_all.py           # Full setup")
        print("       python scripts/setup_all.py --switch blue|green  # Switch traffic")
