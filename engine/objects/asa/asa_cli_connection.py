from netmiko import ConnectHandler


def asa_cli_command(ip_addr: str, username: str, password: str, secret: str, command: str) -> str:
    device_params = {
        'device_type': 'cisco_asa',
        'ip': ip_addr,
        'username': username,
        'password': password,
        'secret': secret
    }

    with ConnectHandler(**device_params) as ssh:
        ssh.enable()
        result = ssh.send_command(command)

    return result
