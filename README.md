Docker Health Check Playground
==============================

A very simple python application to demonstrate Docker [Health Checks](https://docs.docker.com/engine/reference/builder/#healthcheck).

## Running Health Check Playground

```terminal
docker stack deploy -c hcp-stack.yml hcp
```

This will run 4 swarm tasks (4 instances of the application), listening on 
port 10000.

Now view the service logs:
```terminal
docker service logs -f hcp_hcp
````

You should see a stream of entries that start with `hcp_hcp.1` etc -- these are the
logs of Docker performing health checks.

## Viewing / Manipulating Tasks

Use your browser or `curl http://localhost:10000/` to view the app. Successive hits should round-robin
through the nodes.

### Additional Endpoints

|  URL    |  Action                              |
|---------|--------------------------------------|
| /       | Human-friendly status page           |
| /status | Machine-friendly status page         |
| /poison | Cause the instance to be 'unhealthy' |
| /die    | Cause the instance to shut down      |


Try hitting the `/poison` url either with your browser or curl. You will not
be able to hit a specific node from outside the container, but you will see 
the status change in the log from `200` to `410`. Docker will see a few `410` 
statuses and then kill and restart the container.

#### The `/die` endpoint

This container will be default run using [Gunicorn](http://gunicorn.org/) - a python web server
which starts several processes that serve requests. When you hit the `/die` endpoint, you are
killing _one_ of those processes, but the parent process continues to live, and will respawn
*a new child process but not a new container*.

To see Docker spawning a new container:
1. Uncomment `entrypoint: ["python", "hcp.py"]` in `hcp-stack.yml`
1. Change `tty: false` to `tty: true`
1. Re-deploy the stack

With these changes, the application now runs under a much simpler (and less robust) python web server
called [wsgiref](https://docs.python.org/3/library/wsgiref.html) which is included in the Python
standard library. This time when we abort the python process, the entire container dies (why? [1]).

## Additional Experiments

### Restart Policy

Try changing the `restart_policy`.`condition` and see if the behavior of the `/die` endpoint changes.
Allowed values are one of: `none`, `on-failure`, `any`. (default: `any`)
See [Restart Policy](https://docs.docker.com/compose/compose-file/#restart_policy)

### Becoming healthy

Make a new endpoint, say `/antidote` that changes the `healthy` value back to True.
How does docker deal with the change?

-----

[1] Why does the container die when the python process is aborted? 
    When running under the `wsgiref` server, the python script is running as PID 1.
