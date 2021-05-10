
# Remote call monitoring for missed calls

A little tool to query a FritzBox for missed calls. It then sends out a Threema message to
a predefined list of people to inform them about the calls. The FritzBox can either be in
the local network or accessed through ```myfritz.net```.

## Configuration file

Modify this template with your own FritzBox and Threema login credentials,
then save it as ```monitor.ini``` in the app root:

```
[configuration]
identity = *XYZ1234
secret = TopSecretCode

[recipients]
mark = KAENOHYEE
caren = F9OOROOGH
duffy = A3IENG9YI
bob = 6EIjU8SO4

[home]
address = 192.168.178.1
user = someUsername
password = fritzboxPassword

[office]
address = deadCoffeeMeat.myfritz.net
port = 12345/tr064
user = someUsername
password = fritzboxPassword
```

## Installation as a Docker container

Todo.


## Realtime call monitoring (not implemented for now)

A more realtime approach to call monitoring for a local FritzBox is using the
builtin CallMonitor service. Its advantage is that the information is being 
pushed to us instead of having to pull the FritzBox regularly.

To use the feature it has to be activated. This can be done with any registered phone
by using the following codes:

* enable: ```#96*5*```
* disable: ```#96*4*```

The stream of calls can then be monitoring on port 1012:

```
> telnet 192.168.0.1 1012
Trying 192.168.0.1...
Connected to fritz.box.
Escape character is '^]'.
09.05.21 21:21:25;RING;0;012345678901;01234567;SIP2;
09.05.21 21:21:27;DISCONNECT;0;0;
09.05.21 21:21:35;RING;0;012345678901;01234567;SIP2;
09.05.21 21:21:36;CONNECT;0;13;012345678901;
09.05.21 21:21:41;DISCONNECT;0;2;
```

## Todos and other resources

https://medium.com/@andreas.schallwig/how-to-make-your-raspberry-pi-file-system-read-only-raspbian-stretch-80c0f7be7353
