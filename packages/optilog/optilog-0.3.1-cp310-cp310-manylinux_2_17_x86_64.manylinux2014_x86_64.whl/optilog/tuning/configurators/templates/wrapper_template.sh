#!/usr/bin/env bash

ulimit -c 0  # Do not generate core files

CWD=$(realpath $(dirname ${0}))         # Path to the wrapper directory
WRAPPER_PY="${CWD}/wrapper.py" # Path to wrapper_template.py
RUNSOLVER="__@RUNSOLVER#@PATH#__"       # Path to runsolver utility
CONFIGURATOR_NAME="__@CONFIGURATOR#@NAME#__"

PYTHON_EXEC="__@PYTHON#@PATH#__"

######################## Extract SMAC specific
if [[ $CONFIGURATOR_NAME == "smac" ]]; then
    SEED=$5
elif [[ $CONFIGURATOR_NAME == "gga" ]]; then
    SEED=$3
fi

if [[ ! -x "${RUNSOLVER}" ]] || [[ ! -f "${RUNSOLVER}" ]]; then
    echo "${RUNSOLVER} does not exist or is not an executable" >&2
    echo "Result of this algorithm run: ABORT, 0, 0, 0, ${SEED}"
    exit -1
fi

exec $PYTHON_EXEC "${WRAPPER_PY}" ${@}