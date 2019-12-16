#!/usr/bin/env python3
"""Install pattoo."""

# Main python libraries
import sys
import os
import locale
import subprocess


# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(EXEC_DIR, os.pardir))
if EXEC_DIR.endswith('/pattoo/setup') is True:
    sys.path.append(ROOT_DIR)
else:
    print(
        'This script is not installed in the "pattoo/bin" directory. '
        'Please fix.')
    sys.exit(2)


def check_pip3():
    """Ensure PIP3 packages are installed correctly.

    Args:
        None

    Returns:
        None

    """
    # Initialze key variables
    lines = []

    # Read pip_requirements file
    filepath = '{}{}pip_requirements.txt'.format(ROOT_DIR, os.sep)
    if os.path.isfile(filepath) is False:
        _log('Cannot find PIP3 requirements file {}'.format(filepath))

    with open(filepath, 'r') as _fp:
        line = _fp.readline()
        while line:
            # Strip line
            _line = line.strip()

            # Read line
            if True in [_line.startswith('#'), bool(_line) is False]:
                pass
            else:
                lines.append(_line)
            line = _fp.readline()

    # Try to import the modules listed in the file
    for line in lines:
        # Determine the package
        package = line.split('=', 1)[0]
        package = package.split('>', 1)[0]
        print('??: Checking package {}'.format(package))
        command = 'pip3 show {}'.format(package)
        (returncode, _, _) = _run_script(command, die=False)
        if bool(returncode) is True:
            log_message = ('''\
Python3 "{}" package not installed or pip3 command not found. Please fix.\
'''.format(package))
            _log(log_message)
        print('OK: package {}'.format(line))


def check_config():
    """Ensure configuration is correct.

    Args:
        None

    Returns:
        None

    """
    # Print Status
    print('??: Checking configuration')

    # Make sure the PATTOO_CONFIGDIR environment variable is set
    if 'PATTOO_CONFIGDIR' not in os.environ:
        log_message = ('''\
Set your PATTOO_CONFIGDIR to point to your configuration directory like this:

$ export PATTOO_CONFIGDIR=/path/to/configuration/directory

Then run this command again.
''')
        _log(log_message)

    # Make sure the PATTOO_CONFIGDIR environment variable is set
    if os.path.isdir(os.environ['PATTOO_CONFIGDIR']) is False:
        log_message = ('''\
Set your PATTOO_CONFIGDIR cannot be found. Set the variable to point to an \
existing directory:

$ export PATTOO_CONFIGDIR=/path/to/configuration/directory

Then run this command again.
''')
        _log(log_message)

    #  Check parameters in the configuration
    filepath = '{}{}setup/_check_config.py'.format(ROOT_DIR, os.sep)
    _run_script(filepath)
    print('OK: Configuration check passed')


def check_database():
    """Ensure database is installed correctly.

    Args:
        None

    Returns:
        None

    """
    #  Check database
    print('??: Setting up database.')
    filepath = '{}{}setup/_check_database.py'.format(ROOT_DIR, os.sep)
    _run_script(filepath)
    print('OK: Database setup complete.')


def _run_script(cli_string, die=True):
    """Run the cli_string UNIX CLI command and record output.

    Args:
        cli_string: String of command to run
        die: Exit with error if True

    Returns:
        (returncode, stdoutdata, stderrdata):
            Execution code, STDOUT output and STDERR output.

    """
    # Initialize key variables
    encoding = locale.getdefaultlocale()[1]
    pattoo_returncode = ('----- pattoo Return Code '
                         '----------------------------------------')
    pattoo_stdoutdata = ('----- pattoo Test Output '
                         '----------------------------------------')
    pattoo_stderrdata = ('----- pattoo Test Error '
                         '-----------------------------------------')

    # Say what we are doing
    string2print = 'Running Command: "{}"'.format(cli_string)
    print(string2print)

    # Run update_targets script
    do_command_list = list(cli_string.split(' '))

    # Create the subprocess object
    process = subprocess.Popen(
        do_command_list,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    stdoutdata, stderrdata = process.communicate()
    returncode = process.returncode

    # Crash if the return code is not 0
    if die is True and bool(returncode) is True:
        # Print the Return Code header
        string2print = '\n{}'.format(pattoo_returncode)
        print(string2print)

        # Print the Return Code
        string2print = '\n{}'.format(returncode)
        print(string2print)

        # Print the STDOUT header
        string2print = '\n{}\n'.format(pattoo_stdoutdata)
        print(string2print)

        # Print the STDOUT
        for line in stdoutdata.decode(encoding).split('\n'):
            string2print = '{}'.format(line)
            print(string2print)

        # Print the STDERR header
        string2print = '\n{}\n'.format(pattoo_stderrdata)
        print(string2print)

        # Print the STDERR
        for line in stderrdata.decode(encoding).split('\n'):
            string2print = '{}'.format(line)
            print(string2print)

        # All done
        sys.exit(2)

    # Return
    return (returncode, stdoutdata, stderrdata)


def next_steps():
    """Print what needs to be done after successful installation.

    Args:
        None

    Returns:
        None

    """
    # Print
    message = ('''
Hooray successful installation! Panna Cotta Time!

Next Steps:
    1) Start the 'bin/pattoo_api_agentd.py' script to accept agent data.
    2) Configure your agents to post data to this server.

Other steps:
    1) You can make pattoo a system daemon by running the scripts in the
       'setup/systemd' directory. Visit this link for details:

       https://github.com/PalisadoesFoundation/pattoo/tree/master/setup/systemd

''')
    print(message)


def _log(message):
    """Log messages and exit abnormally.

    Args:
        message: Message to print

    Returns:
        None

    """
    # exit
    print('\nPATTOO Error: {}'.format(message))
    sys.exit(3)


def main():
    """Setup pattoo.

    Args:
        None

    Returns:
        None

    """
    # Check PIP3 packages
    check_pip3()

    # Check configuration
    check_config()

    # Check database
    check_database()

    # Print next steps
    next_steps()


if __name__ == '__main__':
    # Run setup
    main()
