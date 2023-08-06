# Linkhub Exporter

A Prometheus exporter for Alcatel Linkhub boxes.

Tested with an Alcatel HH41 4G LTE hotspot WiFi router.

## Usage

Install Poetry for you system (need `>=1.2.0b1` currently if using
the dynamic versioning, and have to add the relevant plugin with
`poetry plugin add poetry-dynamic-versioning-plugin`). Then install the
package with:

```shell
poetry install
```

You'll need a Request Key to run exporter, which is derived from the
login password of router box admin interface. See below how to
obtain it.

Once you have a key, you can set it in multiple ways:

* In `.secrets.toml`, see the template shipped at `secrets.toml.template`
  for the format (note the `.` for the non-template filename), OR
* Set an environment variable `DYNACONF_REQUEST_KEY` with the value, e.g.
  `export DYNACONF_REQUEST_KEY=...` in your shell where `...` is replaced with
  the actual value.

Then start up the exporter:

```shell
poetry run exporter
```

### Running in Docker

Build the image with the included Dockerfile from the cloned repository,
let's say:

```shell
docker build -t linkhub_exporter
```

and then run the resulting image as:

```shell
docker run -ti --rm -e "DYNACONF_REQUEST_KEY=...." -p 9877:9877 linkhub_exporter
```

which exposes the Prometheus metrics on `http://localhost:9877`. Don't forget
to set the `DYNACONF_REQUEST_KEY` value, or add it in an `.env` file and
run things as:

```shell
docker run -ti --rm --env-file .env -p 9877:9877 linkhub_exporter
```

### Getting the request key

Currently the easiest way to get it is to:

* Open a browser  and navigate to your router admin interface
* Open the debug console, and ensure that network requests are logged there
* Log in to the admin interface
* Check requests going to `webapi`, look for the requests headers, and the
  value of the `_TclRequestVerificationKey` is what you should use for the
  request key setting of this exporter.

## License

Copyright 2022 Gergely Imreh <gergely@imreh.net>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.