# WebSocket

WebSocket server. Based on [Lawrence D'Oliveiro](https://github.com/ldo) prime factor calculator.

[Uvicorn](https://www.uvicorn.org/) is an Asynchronous Server Gateway Interface [ASGI](https://asgi.readthedocs.io/en/latest/) web server implementation for Python.

Until recently Python has lacked a minimal low-level server/application interface for async frameworks. The ASGI specification fills this gap, and means we're now able to start building a common set of tooling usable across all async frameworks.

Uvicorn currently supports HTTP/1.1 and WebSockets.

Depending on your distro, the following dependencies may need installing as follows...
```
sudo apt install uvicorn python3-uvicorn python3-uvloop python3-httptools
```

## Rocket Launch

This repository includes the files `page_2.html` and `server_2.py`. Copy these files to a local directory. Use a console terminal to launch the server with the command...
```
uvicorn --port 9370 server_2:rocket
```

In a browser tab open the file page_02.html. 

The browser will now interact with the server to simulate launching a rocket.

There are radio buttons to select: rocket weight, thrust, initial fuel and burn rate. Upon pushing *Launch* a comma delimited text string is sent to the server with the values of the radio buttons.

The server calculates Weight, Remaining fuel, acceleration and altitude and along with a countdown sends this back to the browser as another comma delimited text string. The webpage javascript and HTML display this information on the rocket.

## Rocket Launch with music

The files `page_3.html` and `server_3.py` in conjunction with two music files `music_6secs.ogg` and `music_11secs.ogg` provide a rocket launch with music. The lauch information is passing *text* between the server and the client, while the music is passes as *bytes*



