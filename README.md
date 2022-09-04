# ws6in1

Standalone fork of the weewx-ws6in1 driver from https://github.com/BobAtchley/weewx-ws6in1

## Installation

python3 only support in this repo

```
pip3 install pyusb
pip3 install crcmod
pip3 install datetime
```

## Additional Information

Now follows information mainly from the original repository by BobAtchley.

However, some refers to weewx, so it is maybe not relevant for this clone.

---

The weewx-ws6in1 driver supports weather stations that are believed to be
manufactured by CCL Electronics - https://cclel.com
That use a particular console that connects to PCs

These are rebadged and sold as clones by multiple outlets.  The ones known
to work with this driver are listed below:

The weewx driver for the 6 in 1 PC weather station clones:
Youshiko YC9388
Bresser PC 6 in 1 - 7002570
Garni 935PC
Ventus W835

It also supports 5 in 1 PC weather stations:
Bresser PC 5 in 1 - 7002571
Logia 5-in-1 PC - LOWSB510PB

NB: This driver is not compatible with the WiFi versions of these 6 in
1 weatherstations.  It is still possible to use weewx using a Software
Defined Radio (SDR) - search for SDR in the weewx wiki or Interceptor.


### csv_ws6in1

This is a standalone program written in python3 that also gets installed into
the weewx/bin/user area.  It has no arguments.  It needs to run with sudo
unless the local user has usb permissions:

```
$ sudo python3 ./csv_ws6in1
```

When run from the command line it downloads the data from the WS6in1 console
and creates 2 files:

```
ws6in1_<date and time>.csv
ws6in1_<date and time>.raw
```

These can be used for analysis, debugging, etc
weewx should be stopped before this is used and restarted afterwards.

### Additional Notes

The Archive_Interval in the weewx.conf section "[StdArchive]" controls how often
data is written to the database.  Default is 300 seconds.  If the console data
logger is not set to 5 minutes you may want to consider changing this to the
logger setting (but in seconds).

It is recommended you change your weather station console Data Log interval to
'5' minutes.  Please note this means after 50 days the weather station data log
will be full and it will no longer record data, so it is essential you
regularly clear the console data log (best practice would be after a successful
weewx database backup).  This can only be done at the weather station console.

HeatIndex provided by the console is calculated differently to the
HeatIndex calculated by weewx.  If the weewx calculation is preferred
then the weewx.conf file should be modified like this:

```
[StdWXCalculate]
[[Calculations]]
heatindex = software
```

Rainrate on the console uses a sliding window of an hour to perform the
calculation as opposed to WeeWX which uses a sliding window of 900
seconds (15 minutes). After WeeWX has performed its calculation, the
result is scaled to an hour.  This can make a big difference to the
calculated rainrate.  If the weewx calculation is prefered then the
weewx.conf file should be modified like this:

```
[StdWXCalculate]
[[Calculations]]
rainRate = software
```

I now set the heatindex, rainRate and windchill to 'software' so that
these are compatible with the majority of other weather stations, but
this is user choice.

Weewx is backfilling lost values even if record_generation is set to
'software' If you do not want the backfill update the weewx.conf file
with:

```
[StdArchive]
no_catchup = True
```

### Known Issues

If weewx is started after clearing the data log on the console then timeout
errors might occur when there are no entries in the log.  The only cure found
so far is to wait for the console to have one item in its data log and then
re-start weewx.  Note if weewx is already running it does not appear to cause
any problems to clear the data log buffer.

The console uses local time (passed to it from the WS6in1 driver).
This is good in that the console will display the correct time, but
bad because it uses this time to store its data in the console.  The
driver will correct for this local time difference when backfilling.
However if Summertime is being used on the device this will cause
problems when the clocks change.  There are currently 2 options
1) live with the issue - probability of the backlog being needed
(i.e. server failure) when the clocks change is very low
2) Disable summertime on the device weewx is running on

