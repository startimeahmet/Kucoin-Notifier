# Kucoin-Notifier

When open orders on your Kucoin account get partially/fully filled, sends you an email including the respective market pair and the filled amount. Checks every 15 seconds.

Prerequisites: 
```
pip3 install kucoin-python
pip3 install apscheduler
```

Running:

```
python3 notifier.py
```

Changelog:
```
v0.1.1:
-Fixed 'Connection reset by peer' error.
-Repeated requests are done with apscheduler instead of in an infinite loop.

v0.1.0:
Initial Release
```



