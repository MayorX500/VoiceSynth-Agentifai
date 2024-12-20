## Standalone Usage

This allows the user to synthesize text using the Intelex Module. This version is a standalone (Single Service) version of the implementation.

### Prerequisites

- (see [Standalone Installation Pre-requisites](../installation/standalone.md#prerequisites))

### Steps

1. Run the program:

   ```bash
   python intlex.py [TEXT] [CONFIG] --output [OUTPUT] --lang [LANG] --kwargs [KWARGS]
   ```

2. The output will be saved in the output file if provided, otherwise it will be stored in the default location.

### Arguments and Options

For a more detailed explanation of the arguments and options for the standalone version, see the [Intlex Model](../components/app_standalone.md#arguments-and-options) section.

#### TEXT _(Required)_

This argument is used to pass the text to be synthesized.

#### CONFIG _(Optional)_

This argument is used to pass the configuration file. The default configuration file is in the `config` directory.

#### OUTPUT _(Optional)_

This argument is used to pass the output file. The default output file is `output.wav`.

#### LANG _(Optional)_

This argument is used to pass the language of the text to be synthesized. The default language is `pt`.

#### KWARGS _(Optional)_

This argument is used to pass additional arguments to the synthesizer. The arguments should be passed as a dictionary in the following format:

```bash
--kwargs '{"temperature":0.01,"top_p":0.4,"top_k":60}'
```

