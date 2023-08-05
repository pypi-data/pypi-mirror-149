DOCKERFILE_CONDA = """\
# 가장 기본적인 Dockerfile for AWS lambda
FROM public.ecr.aws/lambda/python:{PYTHON_VERSION}
MAINTAINER {MAINTAINER} <{MAINTAINER_EMAIL}>

# set localtime
RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# install linux libraries
RUN yum -y update && yum install -y wget git && yum clean all

# get miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh
RUN sh Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda

# copy envrironment and requirements
COPY environment.yml ${LAMBDA_TASK_ROOT}/environment.yml
COPY requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt
RUN sed -i -r '/m2w64|vs2015|msys2|win|vc/d' ${LAMBDA_TASK_ROOT}/environment.yml
RUN /opt/miniconda/bin/conda env create --file ${LAMBDA_TASK_ROOT}/environment.yml --prefix /opt/conda-env

# install lambda RIC
RUN /opt/conda-env/bin/pip install awslambdaric

# conda python becomes default python
RUN mv /var/lang/bin/python3.8 /var/lang/bin/python3.8-clean && ln -sf /opt/conda-env/bin/python /var/lang/bin/python3.8
ENV PYTHONPATH "/var/lang/lib/python3.8/site-packages:${LAMBDA_TASK_ROOT}"

# copy function code ~ VAR "LAMBDA_TASK_ROOT" is reserved. Do not change!
COPY ./{APP_DIR}/ ${LAMBDA_TASK_ROOT}/

# set entrypoint and cmd
ENTRYPOINT [ "/lambda-entrypoint.sh" ]
CMD [ "{APP}.{HANDLER}" ]
"""
