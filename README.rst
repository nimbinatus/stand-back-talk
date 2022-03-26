Note that I've added a requirements.txt file for people who don't use Pipenv. If you run into any trouble, though, please let me know!

Stand Back!
-----------

This talk was given at PyTexas 2022. Here's how you can set this up yourself!

Prerequirements
===============

* Python 3.9+
* A GCP account (free tier should be able to do this)
* A Pulumi account

Configuration
=============

When you run Pulumi, you'll need to provide configuration values, namely your GCP project name, your GCP region, and your GCP zone.

Result
======

Once you run the program, you'll get an output of a GCP CloudFunctions URL in your terminal. Open that link, and you should get a graph after a moment of the function running! It answers a burning question for Austinites in early March 2022...
