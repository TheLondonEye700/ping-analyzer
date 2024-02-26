#!/bin/bash

echo "Ping from client (_) to server (169.254.9.17)"

# sudo bash ping_server.bash 10 20 (each ping -c 10 times and run for 20 pings)

ping_count=${1:-3}

run_count="${2:-3}"

ping_server(){
    res=$($1 ping 169.254.9.17 -c $ping_count | tail -2)
    # res=$(ping $1 -c $ping_count 2>/dev/null | tail -2)
    truncated=${res#$ping_count packets transmitted, }
    truncated=${truncated#$ping_count received, 0% packet loss, }
    echo -e "$truncated\n" | tee -a $2
}

run_low_pcp () {
    echo -e "Low PCP:"
    ping_server "" "./low.txt"
}

run_high_pcp () {
    echo -e "High PCP:"
    ping_server "ip netns exec client " "./high.txt"
}

# clear file
> ./low.txt
> ./high.txt

for i in $(eval echo {1..$run_count})
do
    echo -e "$i:"

    run_low_pcp

    run_high_pcp
done

python3 compare_ping.py

# if test -f "./output.csv"; then
#     python3 process_csv.py
# fi