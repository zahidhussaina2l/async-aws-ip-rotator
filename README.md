# async-ip-rotator
An async-first Python library that utilizes AWS API Gateway's large IP pool as a proxy to generate pseudo-infinite IPs for web scraping and automated requests. This is an async implementation inspired by [requests-ip-rotator](https://github.com/Ge0rg3/requests-ip-rotator), rebuilt with httpx for modern async support.

This library allows you to bypass IP-based rate-limits for sites and services using async/await syntax.

X-Forwarded-For headers are automatically randomized and applied unless given. This is because otherwise, AWS will send the client's true IP address in this header.

AWS' ApiGateway sends its requests from any available IP - and since the AWS infrastructure is so large, it is almost guaranteed to be different each time. By using ApiGateway as a proxy, we can take advantage of this to send requests from different IPs each time. Please note that these requests can be easily identified and blocked, since they are sent with unique AWS headers (i.e. "X-Amzn-Trace-Id").

## Installation

This package is on pypi so you can install via any of the following:
* `pip install async-aws-ip-rotator`
* `python -m pip install async-aws-ip-rotator`

## Quick Start

```python
import asyncio
import httpx
from async_aws_ip_rotator import ApiGateway

async def main():
    # Create and use gateway with async context manager
    async with ApiGateway("https://site.com") as gateway:
        # Create async client with gateway
        async with httpx.AsyncClient(transport=gateway) as client:
            # Send request (IP will be randomized)
            response = await client.get("https://site.com/index.php", params={"theme": "light"})
            print(response.status_code)

asyncio.run(main())
```

Note: The gateway will automatically clean up its resources when the context manager exits.

## Costs

API Gateway is free for the first million requests per region, which means that for most use cases this should be completely free.
At the time of writing, AWS charges ~$3 per million requests after the free tier has been exceeded.
If your requests involve data stream, AWS would charge data transfer fee at $0.09 per GB.

## Documentation

### AWS Authentication

It is recommended to setup authentication via environment variables. With [awscli](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html), you can run `aws configure` to do this, or alternatively, you can simply set the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` variables yourself.

You can find your access key ID and secret by following the [official AWS tutorial](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html).

### Creating ApiGateway object

The ApiGateway class can be created with the following optional parameters:

| Name | Description | Required | Default |
|------|-------------|----------|----------|
| site | The site (without path) requests will be sent to | True | |
| regions | An array of AWS regions to setup gateways in | False | DEFAULT_REGIONS |
| access_key_id | AWS Access Key ID (will override env variables) | False | *Relies on env variables* |
| access_key_secret | AWS Access Key Secret (will override env variables) | False | *Relies on env variables* |
| verbose | Include status and error messages | False | True |

```python
from async_ip_rotator import ApiGateway, EXTRA_REGIONS, ALL_REGIONS

# Gateway to outbound HTTP IP and port for only two regions
gateway_1 = ApiGateway("http://1.1.1.1:8080", regions=["eu-west-1", "eu-west-2"])

# Gateway to HTTPS google for the extra regions pack, with specified access key pair
gateway_2 = ApiGateway(
    "https://www.google.com", 
    regions=EXTRA_REGIONS, 
    access_key_id="ID", 
    access_key_secret="SECRET"
)
```

### Starting API gateway

The ApiGateway can be used as an async context manager, which will handle initialization and cleanup automatically:

```python
# Using context manager (recommended)
async with ApiGateway("https://site.com") as gateway:
    # Gateway is ready to use here
    async with httpx.AsyncClient(transport=gateway) as client:
        response = await client.get("https://site.com/path")

# For manual control, you can still use start/shutdown methods
gateway = ApiGateway("https://site.com")
await gateway.start(force=True)  # force=True creates new endpoints even if some exist
# ... use gateway ...
await gateway.shutdown()
```

### Sending Requests

Requests are sent using the httpx AsyncClient with the ApiGateway as transport:

```python
async with httpx.AsyncClient(transport=gateway) as client:
    # Send request with random IP
    response = await client.get("https://site.com/path")
    
    # Send with custom X-Forwarded-For header
    response = await client.get(
        "https://site.com/path",
        headers={"X-Forwarded-For": "127.0.0.1"}
    )
```

### Closing ApiGateway Resources

It's important to shutdown the ApiGateway resources once you have finished with them, to prevent dangling public endpoints that can cause excess charges to your account.

```python
# Shutdown all gateways
await gateway.shutdown()

# Shutdown specific endpoints only
await gateway.shutdown(endpoints=["endpoint1", "endpoint2"])
```

**Please note that any gateways started with `require_manual_deletion=True` will not be deleted via the `shutdown` method, and must be deleted manually through either the AWS CLI or Website.**

## Credit

This project is a fork of [requests-ip-rotator](https://github.com/Ge0rg3/requests-ip-rotator) by Ge0rg3, reimplemented with async support using httpx.

The core gateway creation and organisation code was adapted from RhinoSecurityLabs' [IPRotate Burp Extension](https://github.com/RhinoSecurityLabs/IPRotate_Burp_Extension/).

The X-My-X-Forwarded-For header forwarding concept was originally conceptualised by [ustayready](https://twitter.com/ustayready) in his [fireprox](https://github.com/ustayready/fireprox) proxy.