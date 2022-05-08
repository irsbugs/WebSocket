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

In a browser tab open the file `page_2.html`. 

The browser will now interact with the server to simulate launching a rocket.

There are radio buttons to select: rocket weight, thrust, initial fuel and burn rate. Upon pushing *Launch* a comma delimited text string is sent to the server with the values of the radio buttons.

The server calculates Weight, Remaining fuel, acceleration and altitude and along with a countdown sends this back to the browser as another comma delimited text string. The webpage javascript and HTML display this information on the rocket.

## Rocket Launch with music

The files `page_3.html` and `server_3.py` in conjunction with two music files `music_6secs.ogg` and `music_11secs.ogg` provide a rocket launch with music. The launch information is passing *text* between the server and the client, while the music is passes as *bytes*.

Use a console terminal to launch the server with the command...
```
uvicorn --port 9370 server_3:rocket
```

## Rocket Launch with music and animated rocket images

The files `page_4.html` and `server_4.py` in conjunction with two music files `music_6secs.ogg` and `music_11secs.ogg` and two image files `rocket_on.png` and `rocket_off.png` provide a rocket launch with music and animated images. The launch information is passing *text* between the server and the client, while the music and images are passes as *bytes*.

Use a console terminal to launch the server with the command...
```
uvicorn --port 9370 server_4:rocket

## Notes

Both the Javascript Audio() function and the HTML <audio scr= > only accept a "URL". This also applies to <img> and <video>. Refer to:

https://developer.mozilla.org/en-US/docs/Web/API/HTMLAudioElement/Audio
https://www.w3schools.com/tags/att_source_src.asp

A URL is comprised of ASCII characters.

The initial URL specification RFC1738 https://datatracker.ietf.org/doc/html/rfc1738 only listed 10 "official" schemes for a URL, including "http", "ftp" and "file". 

So while Audio can be played using with local URL's that point to a file, like: Audio("music.ogg") or <AUDIO src="music.ogg"> it seems that the source can't be a variable that's a binary blob of music.


URL's have been expanded to have about 100 schemes... 
https://en.wikipedia.org/wiki/List_of_URI_schemes 

...and includes "data" which is RFC2397...
https://datatracker.ietf.org/doc/html/rfc2397

The data scheme allows inclusion of small data items as "immediate" data, as if it had been included externally.

The "data" scheme could include a binary blob, but this isn't the case. Thus the binary blob must be converted to ASCII via Base64 so it can become part of the URL.

So I don't know of any way to pass a variable that is a binary blob to javascript/html audio or image. I assume it also applies to Images and Video. However as the client can access the web-server, then maybe its simplier to leave the audio/image/video files on the server and use a URL pointing to the server to get the file. If that's the case then I can't think of reasons to send a binary blob from the server to the client.
