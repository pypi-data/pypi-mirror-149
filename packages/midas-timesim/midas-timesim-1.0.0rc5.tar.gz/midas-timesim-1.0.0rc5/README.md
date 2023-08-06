# MIDAS Time Simulator

## Description
This package contains a MIDAS *timesim* module, which contains a simulator that tracks time and is able to manipulate it within the simulation.

The intended use-case for the time simulator is to be used inside of MIDAS.
However, it only depends on the `midas-util` package and be used in any mosaik simulation scenario.

## Installation
This package will usually installed automatically together with `midas-mosaik`. It is available on pypi, so you can install it manually with

```bash
pip install midas-timesim
```

## Usage
The complete documentation is available at https://midas-mosaik.gitlab.io/midas.

### Inside of MIDAS
To use the store inside of MIDAS, simply add `timesim` to your modules:

```yaml
    my_scenario:
      modules:
        - timesim
        # - ...
```

This is sufficient for the timesim to run. 
However, additional configuration is possible with:

```yaml
    my_scenario:
      # ...
      timesim_params:
        start_date: 2020-01-01 01:00:00+0100
```

All of the core simulators that have support time inputs will then automatically connect to the *timesim* simulator. 
The scope *timesim* will be created automatically but no other scopes are supported.

### Any Mosaik Scenario

If you don't use MIDAS, you can add the `timesim` manually to your mosaik scenario file. First, the entry in the `sim_config`:

```python
    sim_config = {
        "TimeSimulator": {"python": "midas.modules.timesim:TimeSimulator"},
        # ...
    }
```

Next, you need to start the simulator (assuming a `step_size` of 900):

```python    
    timesim_sim = world.start("TimeSimulator", step_size=900)
```

Finally, the model needs to be started:

```python
    timesim = timesim_sim.Timegenerator()
```

Afterwards, you can define `world.connect(timesim, other_entity, attrs)` as you like.

## License
This software is released under the GNU Lesser General Public License (LGPL). See the license file for more information about the details.