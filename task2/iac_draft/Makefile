.PHONY: deploy delete

CF_STACK_NAME_1=mobile-app-api-lambda-kinesis-processing-database
CF_STACK_NAME_2=carpark-data-s3-lambda-sns
CF_STACK_NAME_3=mobile-app-api-lambda-carpark-availability-details-database
CF_STACK_NAME_4=mobile-app-api-lambda-eventbridge-data-sync-external-api
CF_STACK_NAME_5=mobile-app-api-ecs-fargate-database
CF_STACK_NAME_6=mobile-app-alb-ecs-ec2-database
CF_STACK_NAME_7=mobile-app-api-elastic-beanstalk-database
CF_STACK_NAME_8=mobile-app-appsync-ecs-fargate-database
CF_STACK_NAME_9=mobile-app-api-lambda-database
CF_STACK_NAME_10=mobile-app-api-lambda-storage-caching

deploy:
	aws cloudformation create-stack --stack-name $(CF_STACK_NAME_1) --template-body file://mobile-app-api-lambda-kinesis-processing-database.yaml
	aws cloudformation wait stack-create-complete --stack-name $(CF_STACK_NAME_1)
	aws cloudformation create-stack --stack-name $(CF_STACK_NAME_2) --template-body file://carpark-data-s3-lambda-sns.yaml
	aws cloudformation wait stack-create-complete --stack-name $(CF_STACK_NAME_2)
	aws cloudformation create-stack --stack-name $(CF_STACK_NAME_3) --template-body file://mobile-app-api-lambda-carpark-availability-details-database.yaml
	aws cloudformation wait stack-create-complete --stack-name $(CF_STACK_NAME_3)
	aws cloudformation create-stack --stack-name $(CF_STACK_NAME_4) --template-body file://mobile-app-api-lambda-eventbridge-data-sync-external-api.yaml
	aws cloudformation wait stack-create-complete --stack-name $(CF_STACK_NAME_4)
	aws cloudformation create-stack --stack-name $(CF_STACK_NAME_5) --template-body file://mobile-app-api-ecs-fargate-database.yaml
	aws cloudformation wait stack-create-complete --stack-name $(CF_STACK_NAME_5)
	aws cloudformation create-stack --stack-name $(CF_STACK_NAME_6) --template-body file://mobile-app-alb-ecs-ec2-database.yaml
	aws cloudformation wait stack-create-complete --stack-name $(CF_STACK_NAME_6)
	aws cloudformation create-stack --stack-name $(CF_STACK_NAME_7) --template-body file://mobile-app-api-elastic-beanstalk-database.yaml
	aws cloudformation wait stack-create-complete --stack-name $(CF_STACK_NAME_7)
	aws cloudformation create-stack --stack-name $(CF_STACK_NAME_8) --template-body file://mobile-app-appsync-ecs-fargate-database.yaml
	aws cloudformation wait stack-create-complete --stack-name $(CF_STACK_NAME_8)
	aws cloudformation create-stack --stack-name $(CF_STACK_NAME_9) --template-body file://mobile-app-api-lambda-database.yaml
	aws cloudformation wait stack-create-complete --stack-name $(CF_STACK_NAME_9)
	aws cloudformation create-stack --stack-name $(CF_STACK_NAME_10) --template-body file://mobile-app-api-lambda-storage-caching.yaml
	aws cloudformation wait stack-create-complete --stack-name $(CF_STACK_NAME_10)

delete:
	aws cloudformation delete-stack --stack-name $(CF_STACK_NAME_1)
	aws cloudformation delete-stack --stack-name $(CF_STACK_NAME_2)
	aws cloudformation delete-stack --stack-name $(CF_STACK_NAME_3)
	aws cloudformation delete-stack --stack-name $(CF_STACK_NAME_4)
	aws cloudformation delete-stack --stack-name $(CF_STACK_NAME_5)
	aws cloudformation delete-stack --stack-name $(CF_STACK_NAME_6)
	aws cloudformation delete-stack --stack-name $(CF_STACK_NAME_7)
	aws cloudformation delete-stack --stack-name $(CF_STACK_NAME_8)
	aws cloudformation delete-stack --stack-name $(CF_STACK_NAME_9)
	aws cloudformation delete-stack --stack-name $(CF_STACK_NAME_10)
