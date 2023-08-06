=========
awsapicli
=========

A cli tool exposing capabilities of awsapilib like control tower account creation, account renaming and email updating, account termination and more.


* Documentation: https://awsapicli.readthedocs.org/en/latest


Project Features
================

* Creates an account through Control Tower. Supports nested OU by specifying a parent hierarchy up to 5 levels. It can create the OUs specified automatically if they don't exist with the usage of the force flag
* Requests password reset to activate the root account
* Resets the password of the root, activating the account providing the reset url from the request step.
* Activate IAM access to the billing console with the usage of the root password
* Can update the name and the email of the account
* Can activate and deactivate virtual MFA devices.
