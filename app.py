"""PoC of a deployment API."""

import logging
import os

import k8s

from flask import Flask, request, jsonify

# Global Flask app handle.
app = Flask(__name__)

# Convenience: global logger instance to avoid repetitive code.
logit = logging.getLogger("square")


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/v1/staging/demo', methods=['GET', 'PATCH'])
def deployer():
    """Update the deployment programmatically"""
    if request.method == 'PATCH':
        # Inspect the payload and extract the image name and environment variables.
        payload = request.get_json()
        image = payload["image"]
        env_vars = [{"name": k, "value": v} for k, v in payload["env"].items()]

        # Contact K8s to patch the deployment.
        data, err = patch_deployment(image, env_vars)

        # Return K8s response.
        return jsonify({"data": data, "err": err})
    else:
        # Return JSON payload with all env vars that start with "showme_" plus
        # the hostname.
        envs = {
            k: v for k, v in os.environ.items()
            if k.lower().startswith('showme')
        }
        envs["hostname"] = os.environ.get("HOSTNAME", "Unknown")
        return jsonify(envs)


def setup_logging(log_level: int) -> None:
    """Configure logging at `log_level`."""
    # Pick the correct log level.
    if log_level == 0:
        level = "ERROR"
    elif log_level == 1:
        level = "WARNING"
    elif log_level == 2:
        level = "INFO"
    else:
        level = "DEBUG"

    # Create logger.
    logger = logging.getLogger("square")
    logger.setLevel(level)

    # Configure stdout handler.
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Attach stdout handlers to the `square` logger.
    logger.addHandler(ch)
    logit.info(f"Set log level to {level}")


def patch_deployment(docker_image: str, env_vars: list):
    # Create a `requests` client with proper security certificates to access
    # K8s API.
    kubeconfig = os.path.expanduser("~/.kube/config")
    try:
        config = k8s.load_auto_config(kubeconfig, None, disable_warnings=True)
        assert config

        client = k8s.session(config)
        assert client

        # Update the config with the correct K8s API version.
        config, err = k8s.version(config, client)
        assert not err and config
    except AssertionError:
        return 1

    # Log the K8s API address and version.
    logit.info(f"Kubernetes server at {config.url}")
    logit.info(f"Kubernetes version is {config.version}")

    url = f"{config.url}/apis/extensions/v1beta1/namespaces/deployer/deployments/demo"
    containers = {
        "name": "demo",
        "image": docker_image,
        "env": env_vars,
    }
    payload = {"spec": {"template": {"spec": {"containers": [containers]}}}}
    logit.info(f"Patching <demo> container to {docker_image}")
    return k8s.patch(client, url, payload)


def main():
    # Initialise logging.
    setup_logging(2)

    # Start Flask.
    app.run(debug=True, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
