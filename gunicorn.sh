#!/bin/bash
cd /sites/drewlustro
source /sites/envs/drewlustro/bin/activate
export AWS_ACCESS_KEY_ID=AKIAJIRHFLNDAK4USTTQ
export AWS_SECRET_ACCESS_KEY=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
gunicorn production:application -b unix:/tmp/drewlustro.sock
