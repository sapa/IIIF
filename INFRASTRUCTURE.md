# IIIF infrastructure

This document contains a concise description of the current (10.07.2023) IIIF infrastructure at SAPA.

The IIIF runs on a single server media.performing-arts.ch and uses S3 buckets for image and manifests storage.

The configuration of the server is entirely managed using [ansible](https://www.ansible.com).

[Cantaloupe](https://cantaloupe-project.github.io) is used as IIIF server and is run using [docker](https://www.docker.com) using a custom image.

[NGINX](https://www.nginx.com) is used as web server and reverse proxy to Cantaloupe.

All the images are stored on a [S3](https://en.wikipedia.org/wiki/Amazon_S3) bucket hosted by [SWITCH](https://www.switch.ch) which is configured as a data source for Cantaloupe.
Additionally, IIIF manifests and collection are also stored on the same S3 bucket. However, as the bucket is currently not public, the files are not directly served from S3, but synced daily to a local directory to be served by NGINX.