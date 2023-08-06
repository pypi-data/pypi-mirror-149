# use DOCKER_BUILDKIT=1 docker build
# This is needed to use --mount, target and type
# Buildkit is available on linus only
FROM python:3.10
COPY pyproject.toml setup.cfg .git_archival.txt smap README.md ./
COPY bin/bedtools ./bin/
COPY smap/* ./smap/
RUN --mount=source=.git,target=.git,type=bind \
    pip3 install --use-feature=in-tree-build .
ENTRYPOINT ["smap"]