#!/bin/sh
set -eu
# Re-execute inside private user, mount, PID and network namespaces.
if [ "${1:-}" != '--inside' ]; then
    exec unshare --user --map-root-user --mount --pid --net --fork sh "$0" --inside "$@"
fi
shift
delivery=$1
probe=$2
root=$(mktemp -d /tmp/delivery001-isolated-XXXXXX)
mount --make-rprivate /
mount -t tmpfs -o size=512m tmpfs "$root"
mkdir -p "$root/usr/bin" "$root/usr/lib" "$root/usr/lib64" "$root/work" "$root/etc"
ln -s usr/lib "$root/lib"
ln -s usr/lib64 "$root/lib64"
ln -s usr/bin "$root/bin"
cp -r /usr/lib/python3.12 "$root/usr/lib/"
cp -L /usr/bin/python3.12 "$root/usr/bin/python3"
cp -L /usr/bin/env "$root/usr/bin/env"
cp -L /usr/bin/dash "$root/usr/bin/sh"
find /usr/lib/python3.12 -name '*.so' -type f -exec ldd '{}' \; > "$root/ldd.txt" 2>/dev/null || true
ldd /usr/bin/python3.12 /usr/bin/env /usr/bin/dash >> "$root/ldd.txt"
awk '/=> \// {print $3} /^[[:space:]]*\/[^ ]+ \(/ {print $1}' "$root/ldd.txt" | sort -u | while IFS= read -r library; do
    cp -L --parents "$library" "$root"
done
cp -r "$delivery/." "$root/work/"
cp "$probe" "$root/work/smoke.py"
printf '127.0.0.1 localhost\n' > "$root/etc/hosts"
ip link set lo up
echo 'All mounts below isolated root:'
findmnt -R -o TARGET,SOURCE,FSTYPE,OPTIONS "$root"
echo 'Running in chroot with clean environment:'
chroot "$root" /usr/bin/env -i PATH=/usr/bin:/bin HOME=/work /usr/bin/sh -c 'cd /work && exec python3 smoke.py'
