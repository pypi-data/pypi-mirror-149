# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [2022.5.0]

### Added
- Default for make/model/serial

## [2022.4.0]

### Fixed
- channel shapes and channel/mapping units corrected

## [2021.10.0]

### Changed
- Convert `integration_time` field to updated [YEP-111](https://yeps.yaq.fyi/111) property

### Added
- Add messages for units and limits on integration time

## [2021.3.2]

### Changed
- Updated is-sensor trait

## [2021.3.1]

### Changed
- rerendered avpr (forgotten in previous release)

## [2021.3.0]

### Added
- document support for USB4000 spectrometer

### Fixed
- added forgotten config options to is-daemon: enable, log_level, and log_to_file

## [2021.2.0]

### Added
- new field: integration_time_micros [YEP-111](https://yeps.yaq.fyi/111)

### Changed
- refactored to comply with has-mapping trait [YEP-311](https://yeps.yaq.fyi/311)

## [2020.12.0]

### Added
- conda-forge as installation source

### Changed
- regenerated avpr based on recent traits update

## [2020.07.0]

### Changed
- Update to avro-backed yaqd-core [YEP-107](https://yeps.yaq.fyi/107)
- Update to flit for packaging

## [2020.05.0]

### Added
- initial release

[Unreleased]: https://gitlab.com/yaq/yaqd-seabreeze/-/compare/v2024.5.0...main
[2022.5.0]: https://gitlab.com/yaq/yaqd-seabreeze/-/compare/v2022.4.0...v2022.5.0
[2022.4.0]: https://gitlab.com/yaq/yaqd-seabreeze/-/compare/v2021.10.0...v2022.4.0
[2021.10.0]: https://gitlab.com/yaq/yaqd-seabreeze/-/compare/v2021.3.2...v2021.10.0
[2021.3.2]: https://gitlab.com/yaq/yaqd-seabreeze/-/compare/v2021.3.1...v2021.3.2
[2021.3.1]: https://gitlab.com/yaq/yaqd-seabreeze/-/compare/v2021.3.0...v2021.3.1
[2021.3.0]: https://gitlab.com/yaq/yaqd-seabreeze/-/compare/v2021.2.0...v2021.3.0
[2021.2.0]: https://gitlab.com/yaq/yaqd-seabreeze/-/compare/v2020.12.0...v2021.2.0
[2020.12.0]: https://gitlab.com/yaq/yaqd-seabreeze/-/compare/v2020.07.0...v2020.12.0
[2020.07.0]: https://gitlab.com/yaq/yaqd-seabreeze/-/compare/v2020.05.0...v2020.07.0
[2020.05.0]: https://gitlab.com/yaq/yaqd-seabreeze/-/tags/v2020.05.0
