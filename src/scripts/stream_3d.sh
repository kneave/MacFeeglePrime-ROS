/opt/vc/bin/raspivid -cs 1 -o - -3d sbs -3dswap -t 0 -hf -w 1280 -h 360 -fps 25|cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8090}' :demux=h264
