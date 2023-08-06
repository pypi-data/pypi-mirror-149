import os


def scp(
        ip: str,
        source: str,
        dest: str,
        port: int = None,
        ) -> int:
    """
    :param ip: destination ip address
    :param source: source file
    :param dest: destination file
    :param port: port on the destination
    :return status:

    Transfer a file with scp protocol. Warning: this function requires passwordless ssh.
    """

    if port is None:
        status = os.system(f'scp {source} {ip}:{dest}')
    elif port is not None:
        status = os.system(f'scp -P {port} {source} {ip}:{dest}')
    else:
        status = os.system(f'scp {source} {ip}:{dest}')
    print('Returning status: {0}'.format(status))

    return  status


def ssh_command(
                ip: str,
                port: int = None,
                command: str = 'ls'
                ) -> int:
    """
    :param ip: ip address
    :param port: (Optional) port on destination
    :param command: command to execute
    :return state:

    Execute a command on a remote server with ssh protocol. Warning: this function requires passwordless ssh.
    """
    if port is None:
        status = os.system(f'ssh {ip} {command}')
    elif port is not None:
        status = os.system(f'ssh {ip} -p {port} {command}')
    else:
        status = os.system(f'ssh {ip} {command}')

    print('Returning status: {0}'.format(status))

    return status


if __name__ == '__main__':
    print(os.listdir())
    # scp('marco@192.168.XX.YY', 'basic.py', 'DELETEME.py', port=2204)
    # ssh_command('marco@192.168.XX.YY', port=2204, command='rm -r DELETEME.py; ls')
