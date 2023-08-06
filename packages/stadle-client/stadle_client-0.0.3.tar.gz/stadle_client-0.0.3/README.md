# STADLE v0.0.2

<img src="logo/stadle_logo.png" width="600"/>

Our STADLE platform is a paradigm-shifting technology for collaborative and continuous learning combining privacy-preserving frameworks.
STADLE platform stands for Scalable, Traceable, Adaptive, Distributed Learning platform for versatile ML applications.

## Table of Contents

- [STADLE v0.0.1](#stadle-v002)
  - [Table of Contents](#table-of-contents)
  - [General Terminologies](#general-terminologies)
  - [Contributing](#contributing)
    - [Bug Reports](#bug-reports)
    - [Tech Support](#tech-support)
  - [License](#license)

## General Terminologies

There are 3 main components in STADLE.

- Persistence-server

  - A core functionality which helps in keeping track of various database entries.
  - Packaged as a command inside `stadle` library.
  - `stadle persistence-server [args]`

- Aggregator

  - A core functionality which helps aggregation process.
  - Packaged as a command inside `stadle` library.
    - `stadle aggregator [args]`

- Client [this package]
  - In charge of communicating with `stadle` core functions.
  - A core functionality which helps executing the machine learning code from client side.
  - Packaged inside `stadle` library as a class.
    - `from stadle import BasicClient`
    - `class BasicClient` is used to let `stadle` know that the following code is going to be ML oriented.

## Contributing

Reach out with your issues or proposals to improve STADLE.

### Bug Reports

Please check/submit issues [here](https://github.com/tie-set/stadle_client/issues).

### Tech Support

Please reach out to our technical support team via [support@tie-set.com](support@tie-set.com).

## License

Any use and distribution of this code must be under the NDA with [TieSet Inc.](https://tie-set.com/)
