#!/bin/sh

## Usage:
##   . ./export-env.sh ; $COMMAND
##   . ./export-env.sh ; echo ${MINIENTREGA_FECHALIMITE}

unamestr=$(uname)

parse_env() {
  while IFS= read -r line || [ -n "$line" ]; do
    if echo "$line" | grep -F = &>/dev/null; then
      varname=$(echo "$line" | cut -d '=' -f 1)
      varvalue=$(echo "$line" | cut -d '=' -f 2-)
      export "$varname=$varvalue"
    fi
  done < .devcontainer/.env
}

if [ "$unamestr" = 'Linux' ]; then
  parse_env
elif [ "$unamestr" = 'FreeBSD' ] || [ "$unamestr" = 'Darwin' ]; then
  parse_env
fi
