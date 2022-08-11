FROM ubuntu:18.04

RUN apt-get clean && \
    apt-get update --fix-missing && \
    apt-get -y upgrade

ADD ./ext /tmp

RUN apt-get install -y git curl python3-pip && \
    curl -sL https://deb.nodesource.com/setup_12.x | bash && \
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
    apt-get update && \
    apt-get install -y libssl1.0-dev nodejs yarn && \
    mkdir /opt/oracle && \
    tar -xvzf /tmp/*.tar.gz -C /opt/oracle && \
    dpkg -i /tmp/*.deb && \
    sh -c "echo /opt/oracle/instantclient_18_3 > /etc/ld.so.conf.d/oracle-instantclient.conf" && \
    ldconfig

RUN yarn global add @vue/cli@4.2.3

ADD ./requirements.txt /tmp

RUN apt-get install -y libmysqlclient-dev libpq-dev && \
    pip3 install --upgrade pip && \
    pip3 install -r /tmp/requirements.txt
