# README

This is a *very* simple authentication service to be used in conjunction with
NGINX's *auth_request* module. It answers the question: is this user
authenticated? It has two usable endpoints:

- `/auth/` returns a `200` if the user is authenticated and a `401` if not.
- `/accounts/login` is a user login portal

## Installation

Clone the repository, with permissions such that the directory belongs to your
application user, create a Python virtual environment for the app, and install
the application's dependencies into the virtual environment:

```shell
$ git clone https://github.com/kylerjohnston/is_authenticated.git /srv/is_authenticated
$ cd /srv/is_authenticated
$ python3 -m venv venv/
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

It uses SQLite for a database. Make sure you have SQLite installed.

You need to set a couple environment variables:

- `REDIRECT_URL` defines where users will be redirected after successfully
  logging in or out;
- `SECRET_KEY` is a secret key needed for Django. Generate one on the command
  line like this: `python -c 'import secrets; print(secrets.token_urlsafe())'`

Here is an example script you could use to start the server, which also sets
those environment variables.

``` shell
#!/usr/bin/env bash

# Update these variables with your values
export REDIRECT_URL='/path/to/redirect'
export SECRET_KEY='YOUR SECRET KEY'

source /srv/is_authenticated/venv/bin/activate
cd /srv/is_authenticated/is_authenticated && \
  gunicorn is_authenticated.wsgi --bind 127.0.0.1:8000 --workers 1
```

## Create a user

After installing, you can use `./manage.py createsuperuser` to create a new admin user.

``` shell
$ source /srv/is_authenticated/venv/bin/activate
$ cd /srv/is_authenticated/is_authenticated/
$ ./manage.py createsuperuser
```

Then you can sign in at the `/admin/` endpoint to create other users, if needed.

## Using with the NGINX auth_request module

Let's say you have an app without authentication, with NGINX set up as a reverse
proxy in front of it, and you want a way to control access to it.

In your NGINX config, add something like:

``` nginx
location = /auth/ {
    internal;
    proxy_pass   http://127.0.0.1:8000;
    proxy_pass_request_body off;
    proxy_set_header Content-Length "";
}

location = /accounts/login/ {
    proxy_pass  http://127.0.0.1:8000;
}

location / {
    error_page 401 = @error401;
    auth_request    /auth/;
    proxy_pass https://your-app.example.com;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}

location @error401 {
    return 302 https://$host/accounts/login/;
}
```

For each request to your app, to a location that's not `/auth/` or
`/accounts/login/`, NGINX will send a subrequest to `is_authenticated`, running
on http://127.0.0.1:8000. If the subrequest returns a `200`, the user is
authenticated and NGINX upstreams the request to https://your-app.example.com.
If the subrequest returns a `401`, the user is not authenticated and NGINX
redirects to the login page.

## License

Copyright 2020 Kyle Johnston.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
