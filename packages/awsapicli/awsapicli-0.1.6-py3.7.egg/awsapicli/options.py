#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: options.py
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
options package.

Import all parts from options here

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

import functools

import click
from click_option_group import MutuallyExclusiveOptionGroup

from .validators import (validate_email,
                         validate_region,
                         validate_token,
                         validate_account_name,
                         validate_account_password,
                         validate_mfa_device_name,
                         validate_mfa_device_serial)

__author__ = '''Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''24-12-2021'''
__copyright__ = '''Copyright 2021, Costas Tyfoxylos'''
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<ctyfoxylos@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


email_option = click.option('-e',
                            '--email',
                            'account_email',
                            required=True,
                            type=str,
                            callback=validate_email,
                            help='The email to use.')

device_name_option = click.option('-d',
                                  '--device-name',
                                  'device_name',
                                  required=True,
                                  default='root-account-mfa-device',
                                  type=str,
                                  callback=validate_mfa_device_name,
                                  help='The name of the virtual device. Defaults to "root-account-mfa-device"')

device_serial_option = click.option('-d',
                                    '--device-serial',
                                    'device_serial',
                                    required=True,
                                    type=str,
                                    callback=validate_mfa_device_serial,
                                    help='The serial of the virtual device in the form'
                                         ' of arn:aws:iam::ACCOUNTID:mfa/DEVICE_NAME.')

password_option = click.option('-p',
                               '--password',
                               'password',
                               hide_input=True,
                               prompt=True,
                               confirmation_prompt=True,
                               required=True,
                               type=str,
                               callback=validate_account_password,
                               help='The root password of the account.')

region_option = click.option('-r',
                             '--region',
                             'region',
                             required=True,
                             type=str,
                             envvar='AWS_DEFAULT_REGION',
                             callback=validate_region,
                             help=('The home region of the account, can read from "AWS_DEFAULT_REGION" environment '
                                   'variable'))

captcha_option = click.option('-t',
                              '--2captcha-token',
                              'captcha_token',
                              required=False,
                              envvar='TWO_CAPTCHA_API_TOKEN',
                              callback=validate_token,
                              help='A valid token for the 2captcha service if automatic captcha solving is required. '
                                   'Can read from "TWO_CAPTCHA_API_TOKEN" environment variable')

account_name_option = click.option('-n',
                                   '--name',
                                   'account_name',
                                   required=True,
                                   type=str,
                                   callback=validate_account_name,
                                   help='The name of the account.')


def common_options(function):
    """Options common to all commands."""
    logging_options = MutuallyExclusiveOptionGroup('Logging options',
                                                   help='Sets the level of logging interactively or accepts a '
                                                        'configuration file.')
    options = [logging_options.option('-L',
                                      '--log-config',
                                      'log_config',
                                      type=click.File(),
                                      help='A config file for logging, mutually exclusive with setting the logging '
                                           'level interactively.'),
               logging_options.option('-l',
                                      '--log-level',
                                      'log_level',
                                      type=click.Choice(['debug', 'info', 'warning', 'error']),
                                      default='info',
                                      help='Provide the log level. Defaults to info. Mutually exclusive with providing '
                                           'a logging configuration file.')]
    return functools.reduce(lambda x, option: option(x), options, function)


def common_account_manager_options(function):
    """Options common to account manager commands."""
    options = [email_option,
               password_option,
               region_option,
               click.option('-m',
                            '--mfa-seed',
                            'mfa_serial',
                            required=False,
                            type=str,
                            help='The original mfa seed of the account if virtual MFA is enabled.'),
               captcha_option]
    return functools.reduce(lambda x, option: option(x), options, function)
