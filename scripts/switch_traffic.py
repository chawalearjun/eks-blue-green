import subprocess
import sys

if len(sys.argv) != 2 or sys.argv[1] not in ["blue", "green"]:
    print("Usage: python scripts/switch_traffic.py [blue|green]")
    sys.exit(1)

version = sys.argv[1]
cmd = f"kubectl patch service demo-service -p '{{\"spec\":{{\"selector\":{{\"app\":\"demo\",\"version\":\"{version}\"}}}}}}'"
subprocess.run(cmd, shell=True, check=True)
print(f"Switched traffic to {version}")
