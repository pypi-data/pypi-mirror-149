""" AWS Lambda Python Module """
import os
import logging
import boto3

SSM_PREFIX = 'ssm:'

log = logging.getLogger(__name__)
log_level = os.environ.get('LOG_LEVEL')

if log_level:
    log.setLevel(log_level)

def lambda_env(env=None):
    """ AWS Lambda Function """

    aws = boto3.client('ssm')

    new_env = dict(env) if env else dict(os.environ)

    if 'loaded' in new_env:
        return new_env

    ssm_vars = {k: v.strip(SSM_PREFIX) for k, v in new_env.items() if v.startswith(SSM_PREFIX)}

    if not ssm_vars:
        return new_env

    resp = aws.get_parameters(Names=list(ssm_vars.values()), WithDecryption=True)['Parameters']

    for var_name, full_path in ssm_vars.items():
        for param in resp:
            if param['Name'] + param.get('Selector', '') == full_path:
                new_env[var_name] = param['Value']
                break

    new_env['loaded'] = True
    return new_env

if __name__ == "__main__":
    print(lambda_env())