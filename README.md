# BM Generator 3000

Test generator for battery cyclers.

Web version: https://openbat.isea.rwth-aachen.de/bmgen/

![Screenshot](images/screenshot.png)

## Examples

This is a [simple example](examples/simple_program.py) that shows the basic structure of a program:

```python
# import required functions and channel variables
from bmgen.function import *
from bmgen.channel import *

# set data recording interval
# registration format is only applied to BM programs
register(time=seconds(1), format=["my_custom_reg"])

# set safety limits
limit(V > 4.2, error(1))
limit(V < 2.5, error(1))
limit(I > 5, error(1))
limit(I < -5, error(1))

# specify test steps
charge(current=2.0, voltage=4.2, limits=[I < 0.2])
pause(hours=1)
discharge(current=1.5, limits=[V < 3.0])
```

To see the test programs that are generated, expand the sections below.


<p>
<details>
<summary>Battery Manager</summary>

Command for this example: <code>bmgen --target bm --format table examples/simple_program.py</code>

<table>
<tr><th>Step</th><th>Label</th><th>Operator</th><th>Value</th><th>Limit</th><th>Action</th><th>Registration</th></tr>
<tr><td>1</td><td></td><td>SET</td><td></td><td></td><td></td><td>my_custom_reg<br>1 s</td></tr>
<tr><td>2</td><td></td><td>SET</td><td></td><td>> 4.2 V<br>< 2.5 V<br>> 5 A<br>< -5 A</td><td>ERR 1<br>ERR 1<br>ERR 1<br>ERR 1</td><td></td></tr>
<tr><td>3</td><td></td><td>CHA</td><td>2.0 A<br>4.2 V</td><td>< 0.2 A</td><td></td><td></td></tr>
<tr><td>4</td><td></td><td>PAU</td><td></td><td>90 min</td><td></td><td></td></tr>
<tr><td>5</td><td></td><td>DCH</td><td>1.5 A</td><td>< 3.0 V</td><td></td><td></td></tr>
<tr><td>6</td><td></td><td>STO</td><td></td><td></td><td></td><td></td></tr>
</table>

</details>
</p>

<p>
<details>
<summary>Neware</summary>

Command for this example: <code>bmgen --target neware --format table examples/simple_program.py</code>

<table>
<tr><th>Step Index</th><th>Step Name</th><th>Step Time (hh:mm:ss.ms)</th><th>Voltage (V)</th><th>Current (A)</th><th>Cutoff voltage (V)</th><th>Cutoff current (A)</th><th>Capacity (Ah)</th><th>Others</th></tr>
<tr style="color: #81bc06"><td>1</td><td>CCCV Chg</td><td></td><td>4.2</td><td>2.0</td><td></td><td>0.2</td><td></td><td></td></tr>
<tr style="color: #eec908"><td>2</td><td>Rest</td><td>1:30:00.000</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr style="color: #f35325"><td>3</td><td>CC DChg</td><td></td><td></td><td>1.5</td><td>3.0</td><td></td><td></td><td></td></tr>
<tr style="color: #000000"><td>4</td><td>End</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
</table>

</details>
</p>

<p>
<details>
<summary>Basytec</summary>

Command for this example: <code>bmgen --target basytec --format table examples/simple_program.py</code>

<table>
<tr><th></th><th>Level</th><th>Label</th><th>Command</th><th>Parameter</th><th>Termination</th><th>Action</th><th>Registration</th><th>Comment</th></tr>
<tr><td>1</td><td></td><td></td><td>Start</td><td></td><td>U>4.2V<br>U<2.5V<br>I>5A<br>I<-5A</td><td><br><br><br></td><td></td><td></td></tr><tr><td>2</td><td></td><td></td><td>Charge</td><td>I=2.0A<br>U=4.2V</td><td>I<0.2A</td><td></td><td>t=1s</td><td></td></tr><tr><td>3</td><td></td><td></td><td>Pause</td><td></td><td>t>90min</td><td></td><td>t=1s</td><td></td></tr><tr><td>4</td><td></td><td></td><td>Discharge</td><td>I=1.5A</td><td>U<3.0V</td><td></td><td>t=1s</td><td></td></tr><tr><td>5</td><td></td><td>STOP</td><td>Stop</td><td></td><td></td><td></td><td></td><td></td></tr></table>

</details>
</p>

 ## Installation

 A working installation of Python >= 3.9 and pip is required.

 The bmgen package can be downloaded from the Gitlab server:

    pip install --index-url https://token:glpat-pNBLCU7BiNexQJA6GVNh@git.isea.rwth-aachen.de/api/v4/projects/2105/packages/pypi/simple bmgen

## Usage

The easiest way to get started is using the [web version](https://openbat.isea.rwth-aachen.de/bmgen/) in the browser.

The program can also be used as a command line tool.
The only required argument is the filename of the Python program to be translated.
A dash ( - ) can be used to read from standard input.

The following options are supported:

### -t, --target

Set the target language. Available values are bm, neware, and basytec. The default value is bm.

### -f, --format

Set the target format. The supported formats depend on the target:

BM:
- text (default): Plain text file that can be pasted into the Battery Manager
- table: HTML table resembling the Battery Manager interface for test programs

Neware:
- xml (default): XML file that can be opened in the Neware client
- table: HTML table resembling the Neware interface for test programs

Basytec:
- text (default): Plain text PLN file that can be opened in the Basytec program
- table: HTML table resembling the Basytec interface for test programs

### -o, --out

Name of the output file. If this option is not provided, the output is written to the terminal.

## Feature completeness

|                                                   | Battery Manager            | Neware | BasyTec |
| ------------------------------------------------- | -------------------------- | ------ | ------- |
| charge/discharge/pause                            | ✔️                         | ✔️    | ✔️      |
| limits (global and for individual steps)          | ✔️                         | ✔️    | ✔️      |
| registrations (global)                            | ✔️                         | ✔️    | ✔️      |
| registrations (for individual steps)              | ➖                         | ➖    | ➖      |
| variables in the generated program                | ✔️                         | ❌    | ➖      |
| battery parameters                                | ✔️                         | ❌    | ✔️      |
| if / else statements                              | ✔️                         | ➖    | ➖      |
| loops with fixed cycle count                      | ✔️                         | ➖    | ➖      |
| loops with arbitrary conditions                   | ➖                         | ❌    | ➖      |
| references to duration/Ah count of previous steps | ✔️                         | ✔️    | ✔️      |
| calculations in the generated program             | ➖ (+= and -= implemented) | ❌    | ➖      |
| array constants                                   | ✔️                         | ➖    | ➖      |
| mutable arrays                                    | ✔️                         | ❌    | ❌      |

✔️ implemented
➖ planned
❌ not supported by the target