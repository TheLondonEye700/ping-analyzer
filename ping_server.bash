#!/bin/bash

echo "DEPRECICATED: Ping from client (169.254.9.15) to server (169.254.9.17)"


ping_count=${1:-3}

run_count="${2:-3}"

ping_server(){
    res=$(ip netns exec client ping 169.254.9.17 -c $ping_count -Q $1 | tail -2)
    # res=$(ping $1 -c $ping_count 2>/dev/null | tail -2)
    truncated=${res#$ping_count packets transmitted, }
    truncated=${truncated#$ping_count received, 0% packet loss, }
    echo -e "$truncated" | tee -a $2
}

run_low_pcp () {
    echo -e "Low PCP:"
    ping_server "80" "./low.txt"
}

run_high_pcp () {
    echo -e "\nHigh PCP:"
    ping_server "224" "./high.txt"
}
