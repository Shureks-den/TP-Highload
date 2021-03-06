# TP-Highload

### Запуск контейнера и тестов ###
Запуск докер-контейнера
`docker build . -t highload`
`docker run -p 80:80 -t highload`

Запуск тестов
`python3 httptest.py`

Результат функционального тестирования:
![func](./img/testsuccess.png)

Нагрузочное тестирование в сравнении с nginx:

#### Nginx
![nginx1](./img/nginx1.png)
![nginx2](./img/nginx2.png)

#### Python
![python1](./img/python1.png)
![python2](./img/python2.png)

Web server test suite
=====================

## Requirements ##

* Respond to `GET` with status code in `{200,404,403}`
* Respond to `HEAD` with status code in `{200,404,403}`
* Respond to all other request methods with status code `405`
* Directory index file name `index.html`
* Respond to requests for `/<file>.html` with the contents of `DOCUMENT_ROOT/<file>.html`
* Requests for `/<directory>/` should be interpreted as requests for `DOCUMENT_ROOT/<directory>/index.html`
* Respond with the following header fields for all requests:
  * `Server`
  * `Date`
  * `Connection`
* Respond with the following additional header fields for all `200` responses to `GET` and `HEAD` requests:
  * `Content-Length`
  * `Content-Type`
* Respond with correct `Content-Type` for `.html, .css, js, jpg, .jpeg, .png, .gif, .swf`
* Respond to percent-encoding URLs
* Correctly serve a 2GB+ files
* No security vulnerabilities

## Testing environment ##

* Put `Dockerfile` to web server repository root
* Prepare docker container to run tests:
  * Read config file `/etc/httpd.conf`
  * Expose port 80

Config file spec:
```
cpu_limit 4       # maximum CPU count to use (for non-blocking servers)
thread_limit 256  # maximum simultaneous connections (for blocking servers)
document_root /var/www/html
```# TP-Highload-course-project
