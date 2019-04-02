Basic web server app.

## Usage

```bash
    # Server
    flask run --host 0.0.0.0 --port 8000

    # Query data.
    curl localhost:8000/v1/staging/myapp --request POST -H "Content-Type: application/json" --data '{"foo": "bar"}' # noqa
```
