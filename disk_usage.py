import paramiko

def get_disk_usage(client: paramiko.SSHClient) -> str:
    stdin, stdout, stderr = client.exec_command("df -h --total | grep total")
    return stdout.read().decode().strip()

def generate_report(servers):
    for server in servers:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            key = paramiko.RSAKey.from_private_key_file(r'C:\Users\rohit\OneDrive\Documents\python_project\py.pem')
            client.connect(server, username='ec2-user', pkey=key) 

            usage_info = get_disk_usage(client)
            print(f"Disk usage for {server}: {usage_info}")
            
            client.close()

        except Exception as e:
            print(f"Failed to retrieve disk usage from {server}: {e}")

server_list = ["99.79.128.183", "35.183.26.237"]  
generate_report(server_list)