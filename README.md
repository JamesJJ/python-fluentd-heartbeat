# Fluentd Heartbeat


[![CodeFactor](https://www.codefactor.io/repository/github/JamesJJ/python-fluentd-heartbeat/badge)](https://www.codefactor.io/repository/github/JamesJJ/python-fluentd-heartbeat)


#### Send a message to Fluentd periodically

# How to use this container

### Supported environment variables

Name            | Default      | Description
---:            | :---         | :---
`LOG_LEVEL`     | `INFO`       | Normally a just short message is shown when this container starts. Setting to `DEBUG` to see continuous verbose debug information.
`FLUENTD_HOST`  | `localhost`  | The hostname of your Fluentd
`FLUENTD_PORT`  | `24224`      | The port your Fluentd is listening on
`FLUENTD_TAG`   | `heartbeat`  | Fluentd message tag
`JSON_MODE`     | `string`     |  `string` or `object` or `none`. See below.
`MESSAGE_KEY`   | null         | If set, encapulate `MESSAGE` inside this key name
`MESSAGE`       | `{ }`        | The message to send. See below.
`SLEEP_DURATION`| 600          | Send messages every `SLEEP_DURATION` seconds (a small time randomization is applied)

### Message formatting

The message to be sent is based on the `MESSAGE` environment variable. `MESSAGE` is parsed as a [Python Format String](https://docs.python.org/3.6/library/string.html#format-string-syntax). `{unixs}` and `{unixms}` placeholders are available for the current time as an integer unix timestamp, in seconds or milliseconds respectively. Use `{{` and `}}` in `MESSAGE` to represent literal `{` and `}`.

#### Message examples

JSON_MODE | MESSAGE_KEY | MESSAGE | Result | Explanation
:---      | :---        | :--- | --- | ---
`none`    |             | `Hello {unix}` | `"Hello 1524492634"` |
`none`    |  `data`     | `Hello {unix}` | `data: "Hello 1524492634"` |
`string`  |             | `Hello {unix}` | ERROR | Message is not valid JSON
`string`  |             | `{{ "Hello:"{unix}" }}` | `{ \"Hello\": \"1524492634\" }` | JSON is validated and then dumped as a _string_ in to the message
`string`  |  `data`     | `{{ "Hello:"{unix}" }}` | `{ data: "{ \"Hello\": \"1524492634\" }"` | JSON is validated and then dumped as a _string_ in to `MESSAGE_KEY`
`object`  |             | `Hello {unix}` | ERROR | Message is not valid JSON
`object`  |             | `{{ "Hello:"{unix}" }}` | `{ "Hello": "1524492634" }` | JSON is validated and then each key becomes a key in the message
`object`  |  `data`     | `{{ "Hello:"{unix}" }}` | `{ data: { "Hello": "1524492634" }}` | JSON is validated and then each key becomes a child key inside `MESSAGE_KEY`


## Try it

```
$ docker-compose up --build --force-recreate
```
