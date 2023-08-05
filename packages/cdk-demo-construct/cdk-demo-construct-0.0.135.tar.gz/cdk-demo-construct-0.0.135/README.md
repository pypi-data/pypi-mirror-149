[![NPM version](https://badge.fury.io/js/cdk-demo-construct.svg)](https://badge.fury.io/js/cdk-demo-construct)
[![PyPI version](https://badge.fury.io/py/cdk-demo-construct.svg)](https://badge.fury.io/py/cdk-demo-construct)
![Release](https://github.com/neilkuan/cdk-demo-construct/workflows/release/badge.svg)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/cdk-demo-construct?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/cdk-demo-construct?label=pypi&color=blue)

# Welcome to `cdk-demo-construct`

The Constructs for the CDK Demo.

## To Use

```python
import * as ec2 from '@aws-cdk/aws-ec2';
import * as cdk from '@aws-cdk/core';
import { AlarmInstance } from 'cdk-demo-construct';
const app = new cdk.App();
const stack = new cdk.Stack(app, 'integ-default');
const vpc = new ec2.Vpc(stack, 'VPC');
new AlarmInstance(stack, 'AlarmInstance', { vpc, notifyMail: ['mail@example.com'] });
```
