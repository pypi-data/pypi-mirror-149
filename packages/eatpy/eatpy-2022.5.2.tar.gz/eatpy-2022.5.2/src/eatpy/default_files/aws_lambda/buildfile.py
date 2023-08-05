DOCKERFILE = """\
# 가장 기본적인 Dockerfile for AWS lambda
FROM public.ecr.aws/lambda/python:{PYTHON_VERSION}
MAINTAINER {MAINTAINER} <{MAINTAINER_EMAIL}>

# set localtime
RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# app 폴더에 있는 코드를 이미지로 복사합니다.
COPY ./{APP_DIR}/ ${LAMBDA_TASK_ROOT}/

# Install python packages.
COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to your handler.
#  - could also be done as a parameter override outside of the Dockerfile
CMD [ "{APP}.{HANDLER}" ]
"""
