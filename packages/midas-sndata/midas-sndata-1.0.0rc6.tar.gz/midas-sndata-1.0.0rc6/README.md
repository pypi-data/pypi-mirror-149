# MIDAS Smart Nord Data Simulator

## Description
This package contains a MIDAS module providing a simulator for the Smart Nord data set.

Although this package is intended to be used with MIDAS, it does not depend from anything MIDAS-related except for the `midas-util` package. You can use in any mosaik simulation scenario.

## Installation
This package will usually installed automatically together with `midas-mosaik`. It is available on pypi, so you can install it manually with

```bash
pip install midas-sndata
```

## Usage
The complete documentation is available at https://midas-mosaik.gitlab.io/midas.

### Inside of MIDAS
To use the powergrid inside of MIDAS, just add `powergrid` to your modules

```yaml
my_scenario:
  modules:
    - sndata
    - ...
```

and configure it with:

```yaml
  sndata_params:
    my_grid_scope:
      step_size: 900
      grid_name: my_grid_scope
      start_date: 2020-01-01 00:00:00+0100
      load_scaling: 1.0
      household_mapping: {}
      land_mapping: {}
      cos_phi: 0.9
      filename: SmartNordProfiles.hdf5
      data_path: path/to/hdf-specified-by-filename
      interpolate: False
      randomize_data: False
      noise_factor: 0.2
      randomize_cos_phi: False
      seed: ~
      seed_max: 1_000_000
```

One of the mappings is required to create load models. All other attributes show their default values and can optionally be left out.

## License
This software is released under the GNU Lesser General Public License (LGPL). See the license file for more information about the details.