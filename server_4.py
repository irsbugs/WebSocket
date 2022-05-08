# +
# WebSocket server. Based on Lawrence D'Oliveiro prime factor calculator.
#
# Launch a Rocket - server_4.py
# Radio buttons to select: rocket weight, thrust, initial fuel and burn rate.
# Button to start countdown and pass the radio buttons data as concatinated string
# Server calculates Weight, Remaining fuel, acceleration and altitude
# Server reads .ogg music files and sends as a "bytes" message
# Server reads two rocket image files and sends as "bytes" message
#
# TODO: await asyncio.sleep(1.0) for countdown vs. real time clock
# TODO: Second "Terminate" button on web-page.
# TODO: Add more functions for rocket inertia and velocity, etc.
#
# ASGI spec: <https://asgi.readthedocs.io/en/latest/index.html>
#
# Depending on your distro, the following dependencies may need installing.
# sudo apt install uvicorn python3-uvicorn python3-uvloop python3-httptools
#
# Ian Stewart 2022-05-07
# -
MAX_LAUNCH = 10  #
LAUNCH_COUNTDOWN = -5
ONE_SECOND_SLEEP = 1.0
import asyncio
import time


async def app(scope, receive, send):
    print("connection scope = %s" % repr(scope))
    assert scope["type"] == "websocket"
    while True:
        event = await receive()
        print("got event %s" % repr(event))
        if event["type"] == "websocket.connect":
            await send({"type": "websocket.accept"})
        elif event["type"] == "websocket.receive":
            data = event.get("bytes")
            if data == None:
                data = event["text"]
            # end if
            print("received data %s" % repr(data))
            await send({"type": "websocket.send", "text": "back atcha"})
        elif event["type"] == "websocket.disconnect":
            print("disconnect code %d" % event["code"])
            break
        else:
            print("unexpected websocket event type %s" % repr(event["type"]))
        # end if
    # end while
# end app


def current_fuel_weight(second, burn_rate, initial_fuel_weight):
    """
    Calculate for the current second the remaining fuel weight.
    If out of fuel return zero.
    """
    if second < 1:
        second = 0
    total_burnt = burn_rate * second
    cfw = initial_fuel_weight - total_burnt
    if cfw < 0:
        cfw = 0
    return cfw


def total_rocket_weight(initial_weight, cfw):
    """
    The total rocket weight reduces as fuel is consumed.
    """
    return initial_weight + cfw


def acceleration(second, trw, thrust):
    """
    Start at zero second when thrust first applied.
    Gravity drag is 9.8 Newtons
    Resultant force = thrust – weight (in newtons)
    Acceleration = resultant force ÷ mass (in m/s²).
    TODO: When out of fuel acceleration decreases. Based on inertia of mass.
    """
    if second < 1:
        return 0
    else:
        resultant_force = thrust - (trw * 9.8)
        acceleration = resultant_force / trw
        return acceleration


def altitude(previous_altitude, a):
    """
    Let current altitude be the previous altitude plus the amount travelled
    from acceleration in one second.
    """
    altitude = previous_altitude + a
    return altitude


async def rocket(scope, receive, send):
    print("connection scope = %s" % repr(scope))
    assert scope["type"] == "websocket"  # avoid accepting lifespan events
    while True:
        event = await receive()
        print("got event %s" % repr(event))

        """  
        #print(dir(event))
        #[..., 'clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 
        #'popitem', 'setdefault', 'update', 'values']        
        print("event.values():", event.values())
        print("event.items():", event.items())
        print("event.keys():", event.keys())
        #print(event.get()) # TypeError: get expected at least 1 argument, got 0
        print("event.get('text'):", event.get("text"))
        """

        if event["type"] == "websocket.connect":
            await send({"type": "websocket.accept"})

        elif event["type"] == "websocket.receive":
            data = event.get("text")
            data_list = data.split(",")
            # print(data_list)
            # ['Launch Rocket', '1000', '10000', '1000', '100']

            # Should be able to determine which button is click based on VALUE
            if data_list[0] == "Launch Rocket":  # OR: "Terminate?"
                counter = LAUNCH_COUNTDOWN
                previous_altitude = 0
                
               
                # Read the rocket_1_off.png file and send as bytes to client. No flame
                with open("rocket_off.png", "rb") as fin:
                    rocket = fin.read()
                    # print(len(music))
                await send({"type": "websocket.send", "bytes": rocket})
                
                # Read the rocket_on.png file and send as bytes to client. Flame
                with open("rocket_on.png", "rb") as fin:
                    rocket = fin.read()
                    # print(len(music))
                await send({"type": "websocket.send", "bytes": rocket})                
                
                time.sleep(1)  # Delay a second to sync the music to the countdown
                

                # Read the music .ogg file and send as bytes to client.
                with open("music_6secs.ogg", "rb") as fin:
                    music = fin.read()
                    # print(len(music))
                await send({"type": "websocket.send", "bytes": music})
                time.sleep(1)  # Delay a second to sync the music to the countdown

                while True:

                    if counter > MAX_LAUNCH:
                        break

                    # Based on Radio button data recieved, perform the maths to
                    # generate the data to send back to the web-page
                    cfw = current_fuel_weight(
                        counter, int(data_list[4]), int(data_list[3])
                    )
                    trw = total_rocket_weight(int(data_list[1]), cfw)
                    a = acceleration(counter, trw, int(data_list[2]))
                    h = altitude(previous_altitude, a)

                    previous_altitude = h
                    # print("previous_altitude:", previous_altitude)
                    if h < 0:
                        h = 0

                    if counter == 0:
                        # Read the music .ogg file and send as bytes to client.
                        with open("music_11secs.ogg", "rb") as fin:
                            music = fin.read()
                            # print(len(music)) # 229062
                        await send({"type": "websocket.send", "bytes": music})

                    if counter < 1:
                        print("Pre-launch Coundown: {}".format(counter))
                    else:
                        # Launched
                        print(
                            "{}: Current fuel weight: {}, Total weight: {}, Acceleration: {:.2f}, Altitude: {:.2f}".format(
                                counter, cfw, trw, a, h
                            )
                        )
                    # end if

                    # Send the data to the web-page
                    # The send type can be "text" or "bytes". Send a string of text.
                    await send(
                        {
                            "type": "websocket.send",
                            "text": "{},{},{},{:.2f},{:.2f}".format(
                                counter, cfw, trw, a, h
                            ),
                        }
                    )

                    await asyncio.sleep(ONE_SECOND_SLEEP)

                    counter += 1

                # end while
                # await send({"type" : "websocket.send", "bytes" : test_bytes})
                await send({"type": "websocket.close", "code": 1000})
            else:
                await send({"type": "websocket.close", "code": 1003})
                # codes come from RFC6455 <https://www.rfc-editor.org/rfc/rfc6455>
            # end if
        elif event["type"] == "websocket.disconnect":
            print("disconnect code %d" % event["code"])
            break
        else:
            print("unexpected websocket event type %s" % repr(event["type"]))
        # end if
    # end while
# end factor
