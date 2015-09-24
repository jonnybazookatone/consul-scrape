[![Build Status](https://travis-ci.org/jonnybazookatone/consul-scrape.svg?branch=master)](https://travis-ci.org/jonnybazookatone/consul-scrape)
[![Coverage Status](https://coveralls.io/repos/jonnybazookatone/consul-scrape/badge.svg?branch=master&service=github)](https://coveralls.io/github/jonnybazookatone/consul-scrape?branch=master)
# consul-scrape
Scrape the contents of consul and dump to AWS s3

# production
You need to modify the following two values in `config.py`
  * ENVIRONMENT: the type of environment you are interested in: staging/production
  * S3_BUCKET: name of the S3 bucket to store the output

# development
You can run unit tests in the following way:
```bash
nosetests cs/tests/unittests
```

A Vagrantfile and puppet manifest are available for development within a virtual machine. To use the vagrant VM defined here you will need to install *Vagrant* and *VirtualBox*. 

  * [Vagrant](https://docs.vagrantup.com)
  * [VirtualBox](https://www.virtualbox.org)

To load and enter the VM: `vagrant up && vagrant ssh`