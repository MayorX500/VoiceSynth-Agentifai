# PI
Projeto Informática '24 - Síntese de Voz em Tempo Real - Agentifai

## Main Program
`python intlex.py [TEXT] [CONFIG] --output [OUTPUT] --lang [LANG] --kwargs [KWARGS]`

### Arguments
- `TEXT`: Text to be synthesized
- `CONFIG`: Configuration file
- `OUTPUT`: Output file (optional)
- `LANG`: Language [pt, en] (optional)
- `KWARGS`: Additional arguments (optional)

### Docker
- `docker compose build`

### Run
- `docker compose {proxy, frontend, server, normalizer, api}`

### Run Client
- `docker compose run client`

### Stop
- `docker compose down`


## Client
### TODO: Add voice option in client,
### TODO: Add option to listen to generated audios

## Proxy
### TODO: Fix prints in proxy
### TODO: Add Logfile

## Server
### TODO: Add Logfile

## Normalizer
### TODO: Add Logfile

## API
### FIX: Not connecting (API or Frontend)
