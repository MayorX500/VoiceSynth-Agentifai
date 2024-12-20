## Normalization

The Normalization Service is a microservice responsible for pre-processing text inputs to ensure a standardized and consistent format before they are sent to the TTS synthesis process. It uses a modular design, allowing flexibility in managing text transformations such as punctuation adjustments, number-to-word conversions, date formatting, and abbreviation expansions.

This service supports multiple languages and can be configured via a `rules.toml` file, making it easy to adapt to new use cases or languages.

### Functionality

**Key Features**:

- **Text Normalization**:  
  Converts raw text into a predictable, synthesis-ready format. Handles various textual elements including punctuation, numbers, and abbreviations.
- **Multi-Language Support**:  
  Adapts normalization rules based on the language (e.g., `pt` for Portuguese, `en` for English).

- **gRPC Communication**:  
  Offers a `Normalize` method to process text requests from the TTS server and returns a `NormalizeResponse` with the transformed text.

- **Modularity**:  
  Rules are implemented as independent modules, which can be enabled or disabled through the configuration file.

### Architecture

**Core Logic**:

- The `Normalizer` class is the entry point for applying normalization rules.
- Rules are dynamically loaded based on the configuration file.

**Rule Modules**:

- Each rule is a separate class inheriting from a `NormalizationRule` base class.

**gRPC Service**:

- **File**: `normalizer.py`
- Defines the `NormalizerService` and handles requests via gRPC.

### Implementation

**File**: `normalizer.py`

The `NormalizerService` initializes the `Normalizer` class with a rule configuration and exposes the `Normalize` method:

```python
class NormalizerService(normalizer_pb2_grpc.NormalizerServiceServicer):
    def __init__(self, args):
        if args.rules is None:
            args.rules = NORMALIZER_RULES
        self.normalizer = Normalizer(args.rules)

    def Normalize(self, request, context):
        normalized_text = self.normalizer.normalize_text(request.text.strip())
        return normalizer_pb2.NormalizeResponse(normalized_text=normalized_text)
```

The service listens on a configurable port (`NORMALIZER_PORT`) and communicates with other components using gRPC.

### Rules

#### Punctuation Handling

- **File**: `punctuation_handling.py`
- **Functionality**: Removes or replaces specified punctuation marks and reduces multiple consecutive spaces to a single space.

**Example**:

```json
Input: "Olá, mundo!"
Output: "Olá  mundo"
```

**Configuration** (`rules.toml`):

```toml
[rules.punctuation_handling]
enabled = true
remove = ["!", "?"]
replace_with_space = [",", ";"]
```

#### Number Conversion

- **File**: `number_conversion.py`
- **Functionality**: Converts numbers into words and handles percentages, ordinals, fractions, and ranges.

**Example**:

```json
Input: "25%" (language: pt)
Output: "vinte e cinco por cento"
```

**Configuration** (`rules.toml`):

```toml
[rules.number_conversion]
enabled = true
detect_percentage = true
detect_years = true
detect_ordinal = true
handle_fractions = true
handle_ranges = true
handle_currency = true
supported_currency = ["USD", "EUR"] # Example
currency_map = "path/to/currency_map.json"
type = "long" # Example
```

#### Date Conversion

- **File**: `date_conversion.py`
- **Functionality**: Converts date formats into words and supports partial dates (e.g., "January 2020").

**Example**:

```json
Input: "2022-12-25"
Output: "vinte e cinco de dezembro de dois mil e vinte e dois"
```

**Configuration** (`rules.toml`):

```toml
[rules.date_conversion]
enabled = true
allowed_separator = ["-", "/"]
formats = ["yyyy-MM-dd", "MM/dd/yyyy"]
```

#### Custom Replacements

- **File**: `custom_replacements.py`
- **Functionality**: Replaces patterns defined in a `custom_replacements.json` file.

**Example**:

```json
Input: "IA é fascinante"
Output: "Inteligência Artificial é fascinante"
```

**Configuration** (`rules.toml`):

```toml
[rules.custom_replacements]
case_sensitive = false
use_regex_flags = true
```

#### Abbreviations

- **File**: `abbreviations.py`
- **Functionality**: Expands abbreviations using a `abbreviations.json` mapping file.

**Example**:

```json
Input: "Dr. Silva"
Output: "Doutor Silva"
```

**Configuration** (`rules.toml`):

```toml
[rules.abbreviations]
enabled = true
abbreviation_file = "abbreviations.json"
```

### Configuration

**File**: `rules.toml`

This file allows enabling/disabling specific rules and defining their parameters. For example:

```toml
[rule_order]
rules = ["punctuation_handling", "number_conversion", "date_conversion", "abbreviations"]

[punctuation_handling]
enabled = true
remove = ["!", "?"]
replace_with_space = [",", ";"]

[number_conversion]
enabled = true
handle_currency = true
detect_percentage = true
detect_ordinal = true

[date_conversion]
enabled = true
formats = ["yyyy-MM-dd", "MM/dd/yyyy"]

[abbreviations]
enabled = true
abbreviation_file = "abbreviations.json"
```

### Workflow

**Input**:

```python
"Dr. Silva deve $25,50 desde 01/01/2022."
```

**Steps**:

1. **Abbreviation Expansion**:

   ```python
   "Doutor Silva deve $25,50 desde 01/01/2022."
   ```

2. **Number Conversion**:

   ```python
   "Doutor Silva deve vinte e cinco dólares e cinquenta cêntimos desde 01/01/2022."
   ```

3. **Date Conversion**:
   ```python
   "Doutor Silva deve vinte e cinco dólares e cinquenta cêntimos desde o primeiro de janeiro de dois mil e vinte e dois."
   ```

**Output**:

```python
"Doutor Silva deve vinte e cinco dólares e cinquenta cêntimos desde o primeiro de janeiro de dois mil e vinte e dois."`
```

