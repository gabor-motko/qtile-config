# NvidiaSensors2
A Qtile widget to display arbitrary sensor information about Nvidia GPU(s). Based on, but not backwards compatible with `libqtile.widget.NvidiaSensors`.

Requires `nvidia-smi` (from `nvidia-utils`).

## Sensor data
The key difference between `NvidiaSensors2` and `NvidiaSensors` is that this one allows you to specify arbitrary fields to be queried by `nvidia-smi` using the `sensors` keyword argument when instantiating the widget. The queried field names can then be referenced in the `format` kwarg **with dots `.` replaced with underscores `_`.**

Run `nvidia-smi --help-gpu-query` to get a full list of supported field names. Some fields of interest are listed below. Note that not all fields will be available on all models.

Queried fields can be referenced by the `format` argument to print them to the text box. All printed fields must be queried, but not all queried fields have to be printed - this is of specific significance for the temperature alert.

Example:
```python
sensors = ["utilization.gpu", "temperature.gpu", "fan.speed"],
format = "GPU {utilization_gpu}% {temperature_gpu}°C ({fan_speed}%)"
```

## Temperature alert
The widget can be set up to use different formatting if any GPU's core temperature exceeds a threshold. This requires that the `temperature.gpu` field be queried. In case of an alert, `format` and `format_all` are replaced by `format_alert` and `format_all_alert`, as long as they are not `None`.

Example (using Pango markup):
```python
threshold = 70,
sensors = ["utilization.gpu", "temperature.gpu"],
format = "GPU {utilization_gpu}%",
format_alert = "<span color='#ffa000'>HOT HOT HOT! {utilization_gpu}% {temperature_gpu}°C</span>"
```

## Constructor arguments
Only new and altered arguments are listed. Refer to [NvidiaSensors](https://docs.qtile.org/en/latest/manual/ref/widgets.html#nvidiasensors) for the rest.
|key|default|description|
|---|---|---|
|sensors|`["utilization.gpu", "temperature.gpu"]`|A list of fields to be queried by `nvidia-smi`.
|format|`"{utilization_gpu}% {temperature_gpu}°C"`|Format string applied to values from individual GPUs. It can only refer to fields that are also defined in the `sensors` list.
|format_all|`"{}"`|Format string applied to the splatted list of individual results processed by `format`. Only displays the first GPU by default - it must be changed to include multiple GPUs.
|format_alert|`None`|If not `None`, this format string overrides the `format` argument in case of a temperature alert.
|format_all_alert|`None`|If not `None`, overrides `format_all` in case of a temperature alert.
|threshold|`70`|If any one GPU core's temperature exceeds this value, `format_alert` and `format_all_alert` override their respective non-alerting format strings.
|foreground_alert||**This argument has been removed.**

## Some interesting fields
|name|note|
|----|----|
|fan.speed|Fan speed in percent, as set by the firmware. May not match real fan speed.
|pstate|Performance state from P0 to P12.
|memory.used|Current allocated VRAM.
|memory.free|Current unallocated VRAM.
|utilization.gpu|Percent of time during which the GPU is busy.
|utilization.memory|Percent of time during which the memory is being read or written.
|encoder.stats.sessionCount|Number of running encoder sessions.
|encoder.stats.averageFps|Average framerate (1/second) over all sessions.
|encoder.stats.averageLatency|Average latency (microseconds) over all sessions.
|temperature.gpu|GPU core temperature (degrees Celsius).
|temperature.memory|HBM memory temperature (degrees Celsius).
|power.draw|Last measured power draw (watts).
|clocks.gr|Graphics clock frequency.
|clocks.sm|Streaming multiprocessor clock frequency.
|clocks.mem|Memory clock frequency.
|clocks.video|Video encoder/decoder clock frequency.
