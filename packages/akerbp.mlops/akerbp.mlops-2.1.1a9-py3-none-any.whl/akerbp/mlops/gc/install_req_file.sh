# install_req_file.sh
#
# Input: Takes a requirement file as argument

# Try to install (max 5 retries)
n=0
until [ "$n" -ge 4 ]
do
    pip install -r $1 && break
    n=$((n+1))
    sleep 5
done