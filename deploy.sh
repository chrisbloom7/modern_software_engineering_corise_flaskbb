zip -r "flaskbb_deploy-$1.zip" ./flaskbb ./.ebextensions wsgi.py setup.py setup.cfg requirements.txt flaskbb.cfg celery_worker.py

aws s3 cp "flaskbb_deploy-$1.zip" s3://${DEPLOY_S3_BUCKET_NAME}

aws elasticbeanstalk create-application-version --application-name flaskbb --source-bundle S3Bucket="${DEPLOY_S3_BUCKET_NAME}",S3Key="flaskbb_deploy-$1.zip" --version-label "ver-$1" --description "Manual application build @ $1" --region "us-east-1"

aws elasticbeanstalk update-environment --environment-name flaskbb-environment --version-label "ver-$1" --region "us-east-1"
