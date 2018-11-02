#!/bin/bash

HOST="http://localhost:10000"
COUNT=10
SLEEP=1

usage() {
    cat <<EOF
Usage: $0 [options] [HOST]

  -c COUNT  Make COUNT requests [${COUNT}]
  -s SLEEP  Delay SLEEP seconds between requests [${SLEEP}]
EOF
}

while getopts "c:s:h" flag
do 
    case ${flag} in
        c) COUNT="${OPTARG}";;
        s) SLEEP="${OPTARG}";;
        h|*) usage; exit;;
    esac
done
shift $((${OPTIND} -1))

if [[ "$#" > 0 ]]; then
    HOST=$1
fi

for ((i=0; i <= COUNT ; i++)); do
    curl ${HOST}/die
    sleep ${SLEEP}
done