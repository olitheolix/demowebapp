Basic web server app.

## Usage

```bash
    # Server
    flask run --host 0.0.0.0 --port 8080

    # Query data.
    curl localhost:8000/v1/staging/myapp --request POST -H "Content-Type: application/json" --data '{"foo": "bar"}' # noqa
```

## Deploy on K8s

    kubectl apply -f deployment.yaml

