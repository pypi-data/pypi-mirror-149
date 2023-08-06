#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: actions.py
#
# Copyright 2021 Costas Tyfoxylos
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
actions package.

Import all parts from actions here

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from art import text2art
from awsapilib.captcha import Terminal
from awsapilib.console import (AccountManager,
                               PasswordManager)
from awsapilib.console.consoleexceptions import (UnableToResolveAccount,
                                                 UnableToRequestResetPassword)
from opnieuw import retry
from rich.console import Console
from rich.text import Text

__author__ = '''Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''24-12-2021'''
__copyright__ = '''Copyright 2021, Costas Tyfoxylos'''
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<ctyfoxylos@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


def show_header():
    """Shows the project header."""
    console = Console()
    text = Text("AWS Account Lifecycle Manager")
    text.stylize("bold magenta")
    console.print(text2art('AWS ALF CLI'))
    console.print(text)


def get_account_manager_arguments(options):
    """Prepares the standard arguments for account manager actions."""
    args = {'email': options.get("account_email"),
            'password': options.get('password'),
            'region': options.get('region'),
            'mfa_serial': options.get('mfa_serial')}
    solver = options.get('solver')
    args['solver'] = solver if solver else Terminal()
    return args


def get_password_manager_arguments(options):
    """Prepares the standard arguments for password manager actions."""
    args = {}
    solver = options.get('solver')
    args['solver'] = solver if solver else Terminal()
    return args


@retry(retry_on_exceptions=UnableToResolveAccount, max_calls_total=5, retry_window_after_first_call_in_seconds=2)
def update_account_name(options, console):
    """Update an account's name.

    Args:
        options: The options provided by click
        console: The console provided by rich

    Returns:
        result (bool): True os success False on failure

    """
    args = get_account_manager_arguments(options)
    account_email = options.get("account_email")
    account_name = options.get('account_name')
    console.log('Please wait while account manager authenticates, it will retry on failure.')
    account_manager = AccountManager(**args)
    console.log(f"Updating account {account_email}'s name to {account_name}")
    result = account_manager.update_account_name(account_name)
    report_message = 'Succeeded' if result else 'Failed'
    console.log(f'{report_message} in updating name to {account_name}.')
    return result


@retry(retry_on_exceptions=UnableToResolveAccount, max_calls_total=5, retry_window_after_first_call_in_seconds=2)
def update_account_email(options, console):
    """Update an account's email.

    Args:
        options: The options provided by click
        console: The console provided by rich

    Returns:
        result (bool): True os success False on failure

    """
    args = get_account_manager_arguments(options)
    account_email = options.get("account_email")
    new_email = options.get('new_account_email')
    console.log('Please wait while account manager authenticates, it will retry on failure.')
    account_manager = AccountManager(**args)
    console.log(f'Updating account {account_email} to {new_email}')
    result = account_manager.update_account_email(new_email)
    report_message = 'Succeeded' if result else 'Failed'
    console.log(f'{report_message} in updating email to {new_email}.')
    return result


@retry(retry_on_exceptions=UnableToResolveAccount, max_calls_total=5, retry_window_after_first_call_in_seconds=2)
def terminate_account(options, console):
    """Terminates an account.

    Args:
        options: The options provided by click
        console: The console provided by rich

    Returns:
        result (bool): True os success False on failure

    """
    args = get_account_manager_arguments(options)
    account_email = options.get("account_email")
    console.log('Please wait while account manager authenticates, it will retry on failure.')
    account_manager = AccountManager(**args)
    console.log(f'Terminating account {account_email}')
    result = account_manager.terminate_account()
    report_message = 'Succeeded' if result else 'Failed'
    console.log(f'{report_message} in terminating account {account_email}.')
    return result


@retry(retry_on_exceptions=(UnableToResolveAccount, UnableToRequestResetPassword),
       max_calls_total=5,
       retry_window_after_first_call_in_seconds=2)
def password_reset_request(options, console):
    """Requests a password reset link.

    Args:
        options: The options provided by click
        console: The console provided by rich

    Returns:
        result (bool): True os success False on failure

    """
    args = get_password_manager_arguments(options)
    if args.get('solver'):
        console.log('Please wait while password manager resolves the captchas, '
                    'it will retry on failure.')
    password_manager = PasswordManager(**args)
    console.log('Requesting password reset.')
    result = password_manager.request_password_reset(options.get("account_email"))
    report_message = 'Succeeded' if result else 'Failed'
    console.log(f'{report_message} in requesting password reset.')
    return result


@retry(retry_on_exceptions=UnableToResolveAccount, max_calls_total=5, retry_window_after_first_call_in_seconds=2)
def password_reset(options, console):
    """Resets an account root password.

    Args:
        options: The options provided by click
        console: The console provided by rich

    Returns:
        result (bool): True os success False on failure

    """
    args = get_password_manager_arguments(options)
    if args.get('solver'):
        console.log('Please wait while password manager resolves the captchas, '
                    'it will retry on failure.')
    password_manager = PasswordManager(**args)
    console.log('Resetting password.')
    result = password_manager.reset_password(options.get('reset_url'),
                                             options.get('password'))
    report_message = 'Succeeded' if result else 'Failed'
    console.log(f'{report_message} in resetting password.')
    return result


@retry(retry_on_exceptions=UnableToResolveAccount, max_calls_total=5, retry_window_after_first_call_in_seconds=2)
def activate_mfa(options, console):
    """Activates virtual MFA on an account.

    Args:
        options: The options provided by click
        console: The console provided by rich

    Returns:
        device (VirtualMFADevice): The device representation returned by the activation process.

    """
    device_name = options.get('device_name')
    args = get_account_manager_arguments(options)
    account_email = options.get("account_email")
    console.log('Please wait while account manager authenticates, it will retry on failure.')
    account_manager = AccountManager(**args)
    console.log(f'Activating MFA device {device_name} on account {account_email}.')
    account_manager.iam.billing_console_access = True
    device = account_manager.mfa.create_virtual_device(device_name)
    console.log(f'Succeeded in activating MFA device "{device_name}".')
    return device


@retry(retry_on_exceptions=UnableToResolveAccount, max_calls_total=5, retry_window_after_first_call_in_seconds=2)
def deactivate_mfa(options, console):
    """Deactivates the virtual MFA of an account.

    Args:
        options: The options provided by click
        console: The console provided by rich

    Returns:
        result (bool): True os success False on failure

    """
    device_serial = options.get('device_serial')
    args = get_account_manager_arguments(options)
    account_email = options.get("account_email")
    console.log('Please wait while account manager authenticates, it will retry on failure.')
    account_manager = AccountManager(**args)
    console.log(f'Deleting MFA device {device_serial} on account {account_email}.')
    mfa_deleted = account_manager.mfa.delete_virtual_device(device_serial)
    report_message = 'Succeeded' if mfa_deleted else 'Failed'
    console.log(f'{report_message} in deleting MFA device "{device_serial}".')
    return mfa_deleted


@retry(retry_on_exceptions=UnableToResolveAccount, max_calls_total=5, retry_window_after_first_call_in_seconds=2)
def activate_iam_billing(options, console):
    """Activates IAM access to the billing console.

    Args:
        options: The options provided by click
        console: The console provided by rich

    Returns:
        result (bool): True os success False on failure

    """
    args = get_account_manager_arguments(options)
    account_email = options.get("account_email")
    console.log('Please wait while account manager authenticates, it will retry on failure.')
    account_manager = AccountManager(**args)
    console.log(f'Activating IAM access on billing console of account {account_email}.')
    account_manager.iam.billing_console_access = True
    result = account_manager.iam.billing_console_access
    report_message = 'Succeeded' if result else 'Failed'
    console.log(f'{report_message} in activating IAM access.')
    return result
