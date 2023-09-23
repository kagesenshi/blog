FROM fedora:37

RUN dnf install rubygem-bundler ruby-devel openssl-devel make gcc gcc-c++ -y && \
    dnf clean all && \
    mkdir /opt/jekyll /data

ADD Gemfile /opt/jekyll
WORKDIR /opt/jekyll

RUN bundle install

WORKDIR /data
ENTRYPOINT ["bundle", "exec", "jekyll"]
