# AWS GameTech Cohort Modeler Code Sample

## Introduction

The GameTech Cohort Modeler is a deployable solution for developers to map out and classify player relationships and classify like behavior within a player base. Within the code sample, we are releasing a SAM (Serverless Application Module) (https://aws.amazon.com/serverless/sam/) template to stand up the infrastructure, a sample Sagemaker Note to visualize the data and a API’s to programmatically interact with the back-end data store.




![](assets/architecture.png?raw=true "Cohort Modeler Architecture")


## Deploy the Cohort Modeler code sample

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools:
* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided --capabilities CAPABILITY_NAMED_IAM
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Parameter DBInstanceClass**: Default db.r4.large can be modified to supported Neptune instances in your selected region. Instance availabiultiy by region can be found here: https://aws.amazon.com/neptune/pricing/
* **Parameter IpAddress**: Enter the IP address of your local computer. This is used to allowlist access to the Neptune Jupyter notebook.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Api may not have authorization defined**: You will be prompted 1 time for every API deployed. The base repository has 10. Enter 'Y' for each.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

## Explore the sample dataset

1. Navigate to the Amazon SageMaker Console 
2. Select the Notebooks from the menu on the left (you may need to click the 3 horitzonal bars to expand this menu) 
3. Click "Open Jupyter" for the notebook that begins with "CohortJupyterNotebook". This will redirect you to a new tab.
4. Click "CohortModelerSampleNotebook.ipynb" to open the Python sample notebook. 
5. Work through this notebook, following all steps to explore the same dataset.


## Cohort Model API

The Cohort Modeler deploys several APIs to interact with and better understand your player cohorts. In the first section below, you have CRUD APIs for interacting with our default defined data model. We define three types of vertices - `player`, `action`, and `campaign`. Documentation for each API is below. 

As you cannot define schemas in TinkerPop, we implement schema control and API validation in code using Lamabda Layers. This can be found in `layers/validation.py`. Each API function uses that shared layer in accordance with an intended purpose. For example, `GET player` uses the validation layer to vefiy the vertex exists; `PUT interaction` calls use the layer to validate API parameters in accordance with your cohort schema. 

You can modify the existing code or add new APIs by creating `AWS::Serverless::Function` resources in `template.yaml`.


### Data APIs

[Create player](docs/data-player-put.md) : `PUT /data/player/{player}`

[Delete player](docs/data-player-delete.md) : `DELETE /data/player/{player}`

[Get player](docs/data-player-put.md) : `GET /data/player/{player}`

[Update player attributes](docs/data-player-post.md) : `POST /data/player/{player}`

[Create interaction](docs/data-player-interaction-put.md) : `PUT /data/player/{player}/interaction`

[Get interaction](docs/data-player-interaction-get.md) : `GET /data/player/{player}/interaction`

[Get relationships](docs/data-player-relationship-get.md) : `GET /data/player/{player}/interaction`

[Create campaign](docs/data-campaign-put.md) : `PUT /data/campaign/{campaign}`

[Update campaign](docs/data-campaign-post.md) : `POST /data/campaign/{campaign}`

[Delete campaign](docs/data-campaign-delete.md) : `DELETE /data/campaign/{campaign}`

### Prediction APIs

[Collaborative filtering](docs/collaborative-filter-get.md) : `GET /prediction/collaborativeFilter`

[Triadic closure](docs/triadic-closure-get.md) : `GET /prediction/triadicClosure`

[Bad actors](docs/bad-actors-get.md) : `GET /prediction/badActors`

[Related users](docs/related-users-get.md) : `GET /prediction/realtedUsers`

## Cleanup

To delete the Cohort Modeler stack that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name `stack-name`
```

## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

