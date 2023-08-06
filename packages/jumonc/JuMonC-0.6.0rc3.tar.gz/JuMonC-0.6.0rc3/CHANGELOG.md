# Changelog JuMonC


## [0.6.0] - 2022-04-06
### Changed
- Code changed to fullfill changed CI
- using dynamic strings instead of varchar in cache DB
- removed unneeded IDs in DB, instead use composite keys

### Added
- It is now possible to use https connections with JumonC for encryoted connections. See: [Readme Encryption](https://gitlab.jsc.fz-juelich.de/coec/jumonc#authorization)
- PyPi extras
- Cache access from REST-API
- CMD arguments to format REST-API cache output
- CMD argument to set path for DB
- DB version und version check

## [0.5.0] - 2022-04-29
### Added
- cache to retrieve old results based on a sql database

## [0.4.2] - 2022-04-19
### Changed
- Fixed error in user plugin

## [0.4.1] - 2022-04-19
### Changed
- Fixed error in disk plugin when missing (the optional dependency) psutil
