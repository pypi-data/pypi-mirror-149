=====
Usage
=====


To use aws-account-lifecycle:

.. code-block:: bash

    aws-account-lifecycle --help
    Usage: aws-account-lifecycle [OPTIONS] COMMAND [ARGS]...

      Main entry point of the CLI.

    Options:
      --help  Show this message and exit.

    Commands:
      billing-iam-activate    Activate IAM access to billing console on an...
      create                  Create a new account through Control Tower.
      mfa-activate            Activate virtual MFA on an account.
      mfa-deactivate          Deactivate virtual MFA on an account.
      request-password-reset  Request a password reset for an account.
      reset-password          Reset the password of an account.
      terminate               Terminate (suspend for 90 days first) an account.
      update-email            Update the email of an account.
      update-name             Update the name of an account.


Activating IAM access on billing console

.. code-block:: bash

    aws-account-lifecycle billing-iam-activate --help
    Usage: aws-account-lifecycle billing-iam-activate [OPTIONS]

      Activate IAM access to billing console on an account.

    Options:
      Logging options: [mutually_exclusive]
                                      Sets the level of logging interactively or
                                      accepts a configuration file.
        -l, --log-level [debug|info|warning|error]
                                      Provide the log level. Defaults to info.
                                      Mutually exclusive with providing a logging
                                      configuration file.
        -L, --log-config FILENAME     A config file for logging, mutually
                                      exclusive with setting the logging level
                                      interactively.
      -t, --2captcha-token TEXT       A valid token for the 2captcha service if
                                      automatic captcha solving is required. Can
                                      read from "TWO_CAPTCHA_API_TOKEN"
                                      environment variable
      -m, --mfa-seed TEXT             The original mfa seed of the account if
                                      virtual MFA is enabled.
      -r, --region TEXT               The home region of the account, can read
                                      from "AWS_DEFAULT_REGION" environment
                                      variable  [required]
      -p, --password TEXT             The root password of the account.
                                      [required]
      -e, --email TEXT                The email to use.  [required]
      --help                          Show this message and exit.

Creating an account

.. code-block:: bash

    aws-account-lifecycle create --help
    Usage: aws-account-lifecycle create [OPTIONS]

      Create a new account through Control Tower.

    Options:
      Logging options: [mutually_exclusive]
                                      Sets the level of logging interactively or
                                      accepts a configuration file.
        -l, --log-level [debug|info|warning|error]
                                      Provide the log level. Defaults to info.
                                      Mutually exclusive with providing a logging
                                      configuration file.
        -L, --log-config FILENAME     A config file for logging, mutually
                                      exclusive with setting the logging level
                                      interactively.
      -e, --email TEXT                The email to use.  [required]
      -r, --region TEXT               The home region of the account, can read
                                      from "AWS_DEFAULT_REGION" environment
                                      variable  [required]
      -n, --name TEXT                 The name of the account.  [required]
      -a, --arn TEXT                  The arn of the role that can access Control
                                      Tower.  [required]
      -o, --organizational-unit TEXT  The OU to create the account under. Defaults
                                      to "Custom".  [required]
      -h, --parent-hierarchy TEXT     The parent hierarchy of the OU if any, space
                                      delimited. If you want the OU to be created
                                      under Root/GrandParentOU/ParentOU the
                                      arguments would be `-h Root -h GrandParentOU
                                      -h ParentOU`
      -p, --product-name TEXT         The product name of the account. Defaults to
                                      the account name if not set.
      -se, --sso-email TEXT           The email for an SSO user. It defaults to
                                      the account email if not set.
      -sf, --sso-first-name TEXT      The first name for an SSO user. It defaults
                                      to "Control".
      -sl, --sso-last-name TEXT       The last name for an SSO user. It defaults
                                      to "Tower".
      -f, --force-ou-hierarchy-creation
                                      If set and a parent hierarchy is provided
                                      then then the tool will try to create it
                                      even if it does not exist.
      --help                          Show this message and exit.

Activating MFA

.. code-block:: bash

    aws-account-lifecycle mfa-activate --help
    Usage: aws-account-lifecycle mfa-activate [OPTIONS]

      Activate virtual MFA on an account.

    Options:
      Logging options: [mutually_exclusive]
                                      Sets the level of logging interactively or
                                      accepts a configuration file.
        -l, --log-level [debug|info|warning|error]
                                      Provide the log level. Defaults to info.
                                      Mutually exclusive with providing a logging
                                      configuration file.
        -L, --log-config FILENAME     A config file for logging, mutually
                                      exclusive with setting the logging level
                                      interactively.
      -t, --2captcha-token TEXT       A valid token for the 2captcha service if
                                      automatic captcha solving is required. Can
                                      read from "TWO_CAPTCHA_API_TOKEN"
                                      environment variable
      -m, --mfa-seed TEXT             The original mfa seed of the account if
                                      virtual MFA is enabled.
      -r, --region TEXT               The home region of the account, can read
                                      from "AWS_DEFAULT_REGION" environment
                                      variable  [required]
      -p, --password TEXT             The root password of the account.
                                      [required]
      -e, --email TEXT                The email to use.  [required]
      -d, --device-name TEXT          The name of the virtual device. Defaults to
                                      "root-account-mfa-device"  [required]
      --help                          Show this message and exit.


Deactivating MFA

.. code-block:: bash

    aws-account-lifecycle mfa-deactivate --help
    Usage: aws-account-lifecycle mfa-deactivate [OPTIONS]

      Deactivate virtual MFA on an account.

    Options:
      Logging options: [mutually_exclusive]
                                      Sets the level of logging interactively or
                                      accepts a configuration file.
        -l, --log-level [debug|info|warning|error]
                                      Provide the log level. Defaults to info.
                                      Mutually exclusive with providing a logging
                                      configuration file.
        -L, --log-config FILENAME     A config file for logging, mutually
                                      exclusive with setting the logging level
                                      interactively.
      -t, --2captcha-token TEXT       A valid token for the 2captcha service if
                                      automatic captcha solving is required. Can
                                      read from "TWO_CAPTCHA_API_TOKEN"
                                      environment variable
      -m, --mfa-seed TEXT             The original mfa seed of the account if
                                      virtual MFA is enabled.
      -r, --region TEXT               The home region of the account, can read
                                      from "AWS_DEFAULT_REGION" environment
                                      variable  [required]
      -p, --password TEXT             The root password of the account.
                                      [required]
      -e, --email TEXT                The email to use.  [required]
      -d, --device-serial TEXT        The serial of the virtual device in the form
                                      of arn:aws:iam::ACCOUNTID:mfa/DEVICE_NAME.
                                      [required]
      --help                          Show this message and exit.

Request a password reset

.. code-block:: bash

    aws-account-lifecycle request-password-reset --help
    Usage: aws-account-lifecycle request-password-reset [OPTIONS]

      Request a password reset for an account.

    Options:
      Logging options: [mutually_exclusive]
                                      Sets the level of logging interactively or
                                      accepts a configuration file.
        -l, --log-level [debug|info|warning|error]
                                      Provide the log level. Defaults to info.
                                      Mutually exclusive with providing a logging
                                      configuration file.
        -L, --log-config FILENAME     A config file for logging, mutually
                                      exclusive with setting the logging level
                                      interactively.
      -e, --email TEXT                The email to use.  [required]
      -t, --2captcha-token TEXT       A valid token for the 2captcha service if
                                      automatic captcha solving is required. Can
                                      read from "TWO_CAPTCHA_API_TOKEN"
                                      environment variable
      --help                          Show this message and exit.

Reset password

.. code-block:: bash

    aws-account-lifecycle reset-password --help
    Usage: aws-account-lifecycle reset-password [OPTIONS]

      Reset the password of an account.

    Options:
      Logging options: [mutually_exclusive]
                                      Sets the level of logging interactively or
                                      accepts a configuration file.
        -l, --log-level [debug|info|warning|error]
                                      Provide the log level. Defaults to info.
                                      Mutually exclusive with providing a logging
                                      configuration file.
        -L, --log-config FILENAME     A config file for logging, mutually
                                      exclusive with setting the logging level
                                      interactively.
      -r, --reset-url TEXT            [required]
      -p, --password TEXT             The root password of the account.
                                      [required]
      --help                          Show this message and exit.

Terminate an account

.. code-block:: bash

    aws-account-lifecycle terminate --help
    Usage: aws-account-lifecycle terminate [OPTIONS]

      Terminate (suspend for 90 days first) an account.

    Options:
      Logging options: [mutually_exclusive]
                                      Sets the level of logging interactively or
                                      accepts a configuration file.
        -l, --log-level [debug|info|warning|error]
                                      Provide the log level. Defaults to info.
                                      Mutually exclusive with providing a logging
                                      configuration file.
        -L, --log-config FILENAME     A config file for logging, mutually
                                      exclusive with setting the logging level
                                      interactively.
      -t, --2captcha-token TEXT       A valid token for the 2captcha service if
                                      automatic captcha solving is required. Can
                                      read from "TWO_CAPTCHA_API_TOKEN"
                                      environment variable
      -m, --mfa-seed TEXT             The original mfa seed of the account if
                                      virtual MFA is enabled.
      -r, --region TEXT               The home region of the account, can read
                                      from "AWS_DEFAULT_REGION" environment
                                      variable  [required]
      -p, --password TEXT             The root password of the account.
                                      [required]
      -e, --email TEXT                The email to use.  [required]
      --help                          Show this message and exit.

Update an account email

.. code-block:: bash

    aws-account-lifecycle update-email --help
    Usage: aws-account-lifecycle update-email [OPTIONS]

      Update the email of an account.

    Options:
      Logging options: [mutually_exclusive]
                                      Sets the level of logging interactively or
                                      accepts a configuration file.
        -l, --log-level [debug|info|warning|error]
                                      Provide the log level. Defaults to info.
                                      Mutually exclusive with providing a logging
                                      configuration file.
        -L, --log-config FILENAME     A config file for logging, mutually
                                      exclusive with setting the logging level
                                      interactively.
      -t, --2captcha-token TEXT       A valid token for the 2captcha service if
                                      automatic captcha solving is required. Can
                                      read from "TWO_CAPTCHA_API_TOKEN"
                                      environment variable
      -m, --mfa-seed TEXT             The original mfa seed of the account if
                                      virtual MFA is enabled.
      -r, --region TEXT               The home region of the account, can read
                                      from "AWS_DEFAULT_REGION" environment
                                      variable  [required]
      -p, --password TEXT             The root password of the account.
                                      [required]
      -e, --email TEXT                The email to use.  [required]
      -n, --new-email TEXT            The email to update to.  [required]
      --help                          Show this message and exit.


Update an account name

.. code-block:: bash

    aws-account-lifecycle update-name --help
    Usage: aws-account-lifecycle update-name [OPTIONS]

      Update the name of an account.

    Options:
      Logging options: [mutually_exclusive]
                                      Sets the level of logging interactively or
                                      accepts a configuration file.
        -l, --log-level [debug|info|warning|error]
                                      Provide the log level. Defaults to info.
                                      Mutually exclusive with providing a logging
                                      configuration file.
        -L, --log-config FILENAME     A config file for logging, mutually
                                      exclusive with setting the logging level
                                      interactively.
      -t, --2captcha-token TEXT       A valid token for the 2captcha service if
                                      automatic captcha solving is required. Can
                                      read from "TWO_CAPTCHA_API_TOKEN"
                                      environment variable
      -m, --mfa-seed TEXT             The original mfa seed of the account if
                                      virtual MFA is enabled.
      -r, --region TEXT               The home region of the account, can read
                                      from "AWS_DEFAULT_REGION" environment
                                      variable  [required]
      -p, --password TEXT             The root password of the account.
                                      [required]
      -e, --email TEXT                The email to use.  [required]
      -n, --name TEXT                 The name of the account.  [required]
      --help                          Show this message and exit.
