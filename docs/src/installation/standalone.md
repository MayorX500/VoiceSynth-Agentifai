## Standalone Program

The Intelex Module can be used as a standalone program (Single Service).

### Prerequisites

- [Python 3.12](https://www.python.org/downloads/)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Pip](https://pip.pypa.io/en/stable/installation/)
- [FFmpeg](https://ffmpeg.org/download.html)
- [wget](https://www.gnu.org/software/wget/)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ddu72/PI
   ```

2. Change to the project directory:

   ```bash
   cd PI
   ```

3. Download the pre-trained models:

   ```bash
   sh download_models.sh
   ```

   **!Note**: This will download the pre-trained models to the `model` directory. This may take a while depending on your internet connection. (Aprox. 7GB)

4. Install the requirements:

   ```bash
   pip install -r environments/server_requirements.txt
   ```

The standalone program is now ready to be used. See [How to Use](../usage/standalone.md) for more information.
