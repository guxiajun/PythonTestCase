#!/bin/bash
FILENAME="$1"
SCRIPT=$(basename $0)
function usage(){
echo -e "\nUSAGE: $SCRIPT file \n"
exit 1
}

if [ $# -lt 1 ] ; then
usage
fi

retpath=$(dirname $FILENAME)

array=($(awk '/Result:/ {print NR}' $FILENAME))
len=${#array[@]}

awk -v arr2="${array[*]}" 'BEGIN{split(arr2,arr3," "); print arr3[5]}''{
len=length(arr3)
lastline = 0;
for (i=1;i<=NF;i++){
if ($i ~ /Terminal/) {
print $0
for(j=1;j<=8;j++)
{getline; print $0}
}
for(k=1;k<=len;k++)
{
if((NR >(arr3[k]-4)) && (NR < (arr3[k]+2)) && NR != lastline)
{
lastline=NR;
print $0
}
}
}
}' $FILENAME >$retpath/result.log
