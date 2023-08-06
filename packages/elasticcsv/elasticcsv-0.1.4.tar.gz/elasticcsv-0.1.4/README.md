# Elastic CSV Loader

## Install

```shell
pip install --upgrade elasticcsv
```

## Run

### Elastic Connection Config
Connection configuration is based in a YAML text file (`connection.yaml`) that must be present in
command directory.

Sample `connection.yaml`


```yaml
elastic_connection:
  proxies:
    http: "http://user:pass@proxy.url:8080"
    https: "http://user:pass@proxy.url:8080"
  user: myuser
  password: mypassword
  node: my.elastic.node
  port: 9200
```

### Run command

```shell
csv2es load-csv --csv ./pathtomyfile/file.csv --index myindex --sep ";"
```