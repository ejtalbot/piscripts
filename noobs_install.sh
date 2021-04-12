(
echo d # delete partition
echo n # new partition
echo p # select primary as partition type
echo # default partition 1
echo # default beginning
echo # default ending
echo t # change parition type
echo b # select FAT32
echo w # write to disk
) | sudo fdisk /dev/sdb1

sudo umount /dev/sdb1

sudo mkfs.vfat /dev/sdb1

sudo mkdir -p /media/$USER/9016-4EF8

sudo mount -t vfat /dev/sdb1 /media/$USER/9016-4EF8

# gat the path to the sd card
sdcardpath="/$(mount | grep -i sdb1 | grep -oE "media[^ ]+")"

sudo unzip NOOBS_v3_5_1.zip -d $sdcardpath

sudo rm -rf "${sdcardpath}/os/LibreELEC_RPi"*
