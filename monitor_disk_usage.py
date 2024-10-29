import paramiko
import sys
import logging

def check_disk_usage(server_ip):
    """Connect to the server and check disk usage."""
    usage_info = {}
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        key = paramiko.RSAKey.from_private_key_file(r'C:\Users\rohit\OneDrive\Documents\python_project\py.pem')
        ssh.connect(server_ip, username='ec2-user', pkey=key)

        # Execute command to get disk usage
        stdin, stdout, stderr = ssh.exec_command("df -h --total | grep total")
        output = stdout.read().decode().strip()

        if output:
            # Parse the output
            _, total, used, free, percent, _ = output.split()
            usage_info['total'] = total
            usage_info['used'] = used
            usage_info['free'] = free
            usage_info['percent'] = percent.strip('%')

        logging.info(f"Successfully retrieved disk usage for {server_ip}: {usage_info}")
        ssh.close()
    except Exception as e:
        logging.error(f"Error connecting to {server_ip}: {e}")
    
    return usage_info

def monitor_servers(input_file, output_file):
    """Monitor disk usage for each server listed in the input file."""
    logging.basicConfig(filename='disk_usage.log', level=logging.INFO,
                        format='%(asctime)s - %(message)s')
    results = []

    try:
        with open(input_file, 'r') as file:
            servers = file.read().splitlines()

        for server in servers:
            usage_info = check_disk_usage(server)
            if usage_info:
                results.append((server, usage_info))

        # Write output to file with detailed information
        if results:
            with open(output_file, 'w') as outfile:
                outfile.write("Server Name, Total Disk, Used Disk, Free Disk, Usage Percentage\n")
                for server, info in results:
                    outfile.write(f"{server}, {info['total']}, {info['used']}, {info['free']}, {info['percent']}%\n")
            print(f"Results written to {output_file}.")
        else:
            print("No server information available.")
            with open(output_file, 'w') as outfile:
                outfile.write("No server information available.\n")

    except FileNotFoundError:
        logging.error(f"Input file {input_file} not found.")
        print(f"Error: Input file {input_file} not found.")
    except Exception as e:
        logging.error(f"An error occurred while processing the servers: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python monitor_disk_usage.py <input_file> <output_file>")
    else:
        monitor_servers(sys.argv[1], sys.argv[2])