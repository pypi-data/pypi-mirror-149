#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: validation.py
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
validation package.

Import all parts from validation here

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

import re
import string
import random

import click
from awsapilib import ControlTower
from awsapilib.captcha import Captcha2, InvalidOrNoBalanceApiToken

__author__ = '''Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''24-12-2021'''
__copyright__ = '''Copyright 2021, Costas Tyfoxylos'''
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<ctyfoxylos@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


ACCOUNT_NAME_MAXIMUM_LENGTH = 50
ACCOUNT_EMAIL_MINIMUM_LENGTH = 6
ACCOUNT_EMAIL_MAXIMUM_LENGTH = 64


def generate_random_string(length):
    """Generates a random string according to the length provided."""
    pool = string.ascii_letters + string.digits
    return ''.join(random.choice(pool) for _ in range(length))


def get_random_account_name(account_name):
    """Generates a random name up to the maximum size allowed."""
    length = ACCOUNT_NAME_MAXIMUM_LENGTH - len(account_name)
    if not length > 2:
        raise ValueError('Name is too long to generate a random name for it.')
    return account_name + generate_random_string(length)


def get_random_account_email(account_email):
    """Generates a random email up to the maximum size allowed."""
    length = ACCOUNT_EMAIL_MAXIMUM_LENGTH - len(account_email)
    if not length > 2:
        raise ValueError('Email is too long to generate a new random one for it.')
    host, domain = account_email.split('@')
    return f'{host}+{generate_random_string(length-1)}@{domain}'


def validate_email(ctx, param, value):
    """Validates an email option."""
    if not value:
        return value
    try:
        if not all([re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", value),
                    ACCOUNT_EMAIL_MINIMUM_LENGTH <= len(value) <= ACCOUNT_EMAIL_MAXIMUM_LENGTH]):
            raise ValueError(value)
        return value
    except ValueError as msg:
        click.echo(f'Incorrect email given, it must be a valid email'
                   f' between 6 and 64 characters: {msg}')
        value = click.prompt(param.name)
        return validate_email(ctx, param, value)


def validate_region(ctx, param, value):
    """Validates a AWS region option."""
    try:
        if value not in ControlTower.get_available_regions():
            raise ValueError(value)
        return value
    except ValueError as msg:
        click.echo(f'Incorrect {param.name} given: {msg}')
        value = click.prompt(param.name)
        return validate_region(ctx, param, value)


def validate_arn(ctx, param, value):
    """Validates an AWS ARN option."""
    conditions = [value.startswith('arn:aws:iam::'),
                  value[13:25].isnumeric(),
                  value[25:31] == ':role/']
    try:
        if not all(conditions):
            raise ValueError(value)
        return value
    except ValueError as msg:
        click.echo(f'Incorrect {param.name} given: {msg}')
        value = click.prompt(param.name)
        return validate_arn(ctx, param, value)


def validate_token(ctx, param, value):  # pylint: disable=unused-argument
    """Validates a 2Captcha Token option and inserts an active 2Captcha instance in the options."""
    if not value:
        return None
    try:
        captcha = Captcha2(value)
        _ = captcha.solver.balance()
    except InvalidOrNoBalanceApiToken:
        raise click.BadParameter('The api token provided is not valid or no balance left of the account.')
    ctx.params['solver'] = captcha
    return value


def validate_reset_link(ctx, param, value):  # pylint: disable=unused-argument
    """Validates a reset link."""
    valid_prefix = 'https://signin.aws.amazon.com/resetpassword?type=RootUser&token='
    if not value.startswith(valid_prefix):
        raise click.BadParameter('The reset link provided is not valid.')
    return value


def validate_account_name(ctx, param, value):
    """Validates an account name."""
    try:
        if not all([re.match(r"[\s\S]*", value), 1 <= len(value) <= ACCOUNT_NAME_MAXIMUM_LENGTH]):
            raise ValueError(value)
        return value
    except ValueError:
        click.echo('Invalid account name given, only ASCII characters are allowed with a length between 1 and 50.')
        value = click.prompt(param.name)
        return validate_account_name(ctx, param, value)


def validate_account_password(ctx, param, value):
    """Validates an account password."""
    lower = set(string.ascii_lowercase)
    upper = set(string.ascii_uppercase)
    digits = set(string.digits)
    punctuation_string = '! @ # $ % ^ & * ( ) < > [ ] { } | _ + - ='
    punctuation = set(punctuation_string.split())
    all_characters = set(string.ascii_lowercase +
                         string.ascii_uppercase +
                         string.digits +
                         punctuation_string.replace(' ', ''))
    try:
        matches = [int(bool(group.intersection(value))) for group in (lower, upper, digits, punctuation)]
        conditions = [sum(matches) >= 3,
                      8 <= len(value) <= 128,
                      all_characters.issuperset(set(value))]
        if not all(conditions):
            raise ValueError
        return value
    except ValueError:
        print(f'Invalid password provided, password should be ascii lower, upper and digits and one of '
              f'{punctuation_string} and it should match at least three of these categories and be between 8 and 128 '
              f'characters.')
        value = click.prompt(param.name)
        return validate_account_password(ctx, param, value)


def validate_mfa_device_name(ctx, param, value):
    """Validates a virtual MFA device name."""
    try:
        if not all([re.match(r"[\w+=/:,.@-]+", value), 9 <= len(value) <= 256]):
            raise ValueError(value)
        return value
    except ValueError:
        click.echo('Invalid device name given, only ASCII characters and + = / : , . @ - are allowed with a length '
                   'between 9 and 256 with no spaces.')
        value = click.prompt(param.name)
        return validate_mfa_device_name(ctx, param, value)


def validate_mfa_device_serial(ctx, param, value):
    """Validates a reset link."""
    conditions = [value.startswith('arn:aws:iam::'),
                  value[13:25].isnumeric(),
                  value[25:30] == ':mfa/']
    try:
        if not all(conditions):
            raise ValueError(value)
        return value
    except ValueError as msg:
        click.echo(f'Incorrect {param.name} given: {msg}')
        value = click.prompt(param.name)
        return validate_mfa_device_serial(ctx, param, value)
