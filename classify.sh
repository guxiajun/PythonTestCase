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
bAdd=1;
#get caseinfo
caseinfo=($(awk '/Test case is:/ {print NR}' $FILENAME))
caseinfolen=${#caseinfo[@]}
#get Terminal line number
termarray=($(awk '/Terminal/ {print NR}' $FILENAME))
termarraylen=${#termarray[@]}
#echo ${termarray[@]}
#get all Result line number
arrayA=($(awk '/Result:/ {print NR}' $FILENAME))
#get pass case Result line number
arrayp=($(awk '/Result: PASS/ {print NR}' $FILENAME))
arrayF=($(awk '/Result: FAILED/ {print NR}' $FILENAME))
lenA=${#arrayA[@]}
lenP=${#arrayP[@]}
lenF=${#arrayF[@]}
#=======================================
#get failed case and pending case result line number
for((i=0;i<=$lenA-1;i++));
do
for((j=0;j<=$lenP-1;j++));
do
if((${arrayA[i]}==${arrayP[j]}));then
{
bAdd=0;
break
}
fi
done
if(($bAdd==1));then
{
lenT=${#arrayT[@]}
arrayT[$lenT]=${arrayA[i]}
}
fi
bAdd=1;
done

#========================================
#get failed case name
for((i=0;i<=$lenF-1;i++));
do
for((j=0;j<=$caseinfolen-1;j++));
do
if((${caseinfo[j]}>${arrayF[i]}||$caseinfolen==1));then
temp0=$[${caseinfo[j-1]}+1]
caseindex=`awk -F'/|  *' -v var=$temp0 'NR==var{print $NF}' $FILENAME`
break
fi
done

temp=$[${arrayF[i]}+1]
casef=`awk -F'/|  *' -v var=$temp 'NR==var{print $(NF-1)}' $FILENAME`
lenfailed=${#failedcase[@]}
if(($casef==$caseindex));then
failedcase[$lenfailed]=$casef
else
failedcase[$lenfailed]=$caseindex"("$casef")"
fi
done

#========================================
#clear log
echo /dev/null >$retpath/result.log



#===========================================
echo "============summary=====================" >>$retpath/result.log
echo "============failed cases num:$lenF=========" >>$retpath/result.log
echo "failed case:${failedcase[@]}">>$retpath/result.log
echo "============analyze=====================" >>$retpath/result.log
for((i=0;i<$lenF;i++));
do

echo ${failedcase[i]} "case info:">>$retpath/result.log
#=======case info
for((p=0;p<=$caseinfolen-1;p++));
do
if((${arrayF[i]}<${caseinfo[p]}));then
if((p>1));then
sed -n ''${caseinfo[p-1]}'p' $FILENAME>>$retpath/result.log 
fi
break
fi
done

echo ${failedcase[i]} "device info:">>$retpath/result.log
#=======device info
for((j=0;j<=$termarraylen-1;j++));
do
if((${arrayF[i]}<${termarray[j]}));then
if((j>1));then
sed -n ''${termarray[j-1]}','$[${termarray[j-1]}+8]'p' $FILENAME >>$retpath/result.log
fi
for((k=j-1;k>=0;k--));
do
if((${termarray[k]}==${termarray[k-1]}+9));then
sed -n ''${termarray[k-1]}','$[${termarray[k-1]}+8]'p' $FILENAME >>$retpath/result.log
else
break;
fi
done
break;
fi
done
echo ${failedcase[i]} "why this is an error:">>$retpath/result.log
#=======result info
sed -n ''$[${arrayF[i]}-3]','$[${arrayF[i]}-1]'p' $FILENAME >>$retpath/result.log
echo -e "\n" >>$retpath/result.log
done
