# opentelemetry-container-distro

An OpenTelemetry distro which automatically discovers container attributes.

This distro expands the standard `opentelemetry-distro` to automatically bring in
additional resource detectors for container environments.

* [opentelemetry-resourcedetector-docker](https://pypi.org/project/opentelemetry-resourcedetector-docker/)
* [opentelemetry-resourcedetector-kubernetes](https://pypi.org/project/opentelemetry-resourcedetector-kubernetes/)
* [opentelemetry-resourcedetector-process](https://pypi.org/project/opentelemetry-resourcedetector-process/)

Otherwise, this distro preserves the behavior and configuration of
`opentelemetry-distro`.
