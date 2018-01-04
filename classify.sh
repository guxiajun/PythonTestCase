#!/bin/bash
FILENAME="$1"
DSTPATH="$2"
SCRIPT=$(basename $0)
function usage(){
echo -e "\nUSAGE: $SCRIPT file \n"
exit 1
}

if [ $# -lt 1 ] ; then
usage
fi

retpath=$(dirname $FILENAME)
DSTPATH=$retpath
dstpath=$DSTPATH/TestResult
mkdir $dstpath

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
arrayD=($(awk '/Result: PENDING/ {print NR}' $FILENAME))
arrayS=($(awk '/Result: PENDING/ {print NR}' $FILENAME))
lenA=${#arrayA[@]}
lenP=${#arrayP[@]}
lenF=${#arrayF[@]}
lenD=${#arrayD[@]}
lenS=${#arrayS[@]}
#=======================================
#get failed case and pending case result line number
#for((i=0;i<=$lenA-1;i++));
#do
#	for((j=0;j<=$lenP-1;j++));
#	do
#	if((${arrayA[i]}==${arrayP[j]}));then
#	{
#		bAdd=0;
#		break
#	}
#	fi
#	done
#	if(($bAdd==1));then
#	{
#		lenT=${#arrayT[@]}
#		arrayT[$lenT]=${arrayA[i]}
#	}
#	fi
#	bAdd=1;
#done

#========================================
#get failed case name
for((i=0;i<=$lenF-1;i++));
do
	temp=$[${arrayF[i]}+1]
	casef=`awk -F'/|  *' -v var=$temp 'NR==var{print $(NF-1)}' $FILENAME`
	casef0=`awk -F'/|  *' -v var=$temp 'NR==var{print $(NF-2)}' $FILENAME`
	lenfailed=${#failedcase[@]}	
	if [[ $casef =~ ^[0-9]*\.?[0-9]$ ]];then
		failedcase[$lenfailed]=$casef0"("$casef")"
		mkdir $dstpath/$casef0"("$casef"+Failed)"
		cp -rf $retpath/$casef0/$casef/* $dstpath/$casef0"("$casef"+Failed)"
	else
		failedcase[$lenfailed]=$casef
		mkdir $dstpath/$casef0"(Failed)"
		cp -rf $retpath/$casef/* $dstpath/$casef0"(Failed)"
	fi
done
echo ${failedcase[@]}
#========================================

#========================================
#get pending case name
for((i=0;i<=$lenD-1;i++));
do
	temp=$[${arrayD[i]}+1]
	cased=`awk -F'/|  *' -v var=$temp 'NR==var{print $(NF-1)}' $FILENAME`
	cased0=`awk -F'/|  *' -v var=$temp 'NR==var{print $(NF-2)}' $FILENAME`
	lenpending=${#pendcase[@]}
	if [[ $cased =~ ^[0-9]*\.?[0-9]$ ]];then
		pendcase[$lenpending]=$cased0"("$cased")"
		mkdir $dstpath/$cased0"("$cased"+Pending)"
		cp -rf $retpath/$cased0/$cased/* $dstpath/$cased0"("$cased"+Pending)"
	else
		pendcase[$lenpending]=$cased
		mkdir $dstpath/$cased0"(Pending)"
		cp -rf $retpath/$cased/* $dstpath/$cased0"(Pending)"
	fi
done
echo ${pendcase[@]}
#========================================
#clear log
echo "============summary=====================">$retpath/result.log
#===========================================
echo "============failed cases num:$lenF=========" >>$retpath/result.log
if(($lenF!=0));then
	echo "failed case:${failedcase[@]}">>$retpath/result.log
	for((i=0;i<$lenF;i++));
	do
		echo ${failedcase[i]} "case info:">>$retpath/result.log
		#=======case info
		for((p=0;p<=$caseinfolen-1;p++));
		do
			if((${arrayF[i]}<${caseinfo[p]}));then
				if((p>=1));then
					sed -n ''${caseinfo[p-1]}'p' $FILENAME>>$retpath/result.log 
				fi
				break
			fi
			if((p==$[$caseinfolen-1]));then
				sed -n ''${caseinfo[p]}'p' $FILENAME>>$retpath/result.log
				break
			fi
		done
	
		echo ${failedcase[i]} "device info:">>$retpath/result.log
		#=======device info
		for((j=0;j<=$termarraylen-1;j++));
		do
			if(((${arrayF[i]}<${termarray[j]})||((i==$lenF-1)&&(j==$termarraylen-1))));then
				if(((i==$lenF-1)&&(j==$termarraylen-1)));then
					j=$[$j+1];
				fi
				if((j>=1));then
					sed -n ''${termarray[j-1]}','$[${termarray[j-1]}+8]'p' $FILENAME >>$retpath/result.log
				fi
			for((k=j-1;k>=1;k--));
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
		echo "============analyze=====================" >>$retpath/result.log
		echo ${failedcase[i]} "why this is an error:">>$retpath/result.log
		#=======result info
		sed -n ''$[${arrayF[i]}-3]','$[${arrayF[i]}-1]'p' $FILENAME >>$retpath/result.log
		echo ${failedcase[i]} "log path:">>$retpath/result.log
		#=======log
		sed -n ''$[${arrayF[i]}+1]'p' $FILENAME >>$retpath/result.log
		echo -e "\n" >>$retpath/result.log
	done
fi



echo "============pending cases num:$lenD=========" >>$retpath/result.log
if(($lenD!=0));then
	echo "pending case:${pendcase[@]}">>$retpath/result.log
	for((i=0;i<$lenD;i++));
	do	
		echo ${pendcase[i]} "case info:">>$retpath/result.log
		#=======case info
		for((p=0;p<=$caseinfolen-1;p++));
		do
			if((${arrayD[i]}<${caseinfo[p]}));then
				if((p>=1));then
					sed -n ''${caseinfo[p-1]}'p' $FILENAME>>$retpath/result.log 
				fi
				break
			fi
			if((p==$[$caseinfolen-1]));then
				sed -n ''${caseinfo[p]}'p' $FILENAME>>$retpath/result.log
				break
			fi
			
		done
	
		echo ${pendcase[i]} "device info:">>$retpath/result.log
		#=======device info
		for((j=0;j<=$termarraylen-1;j++));
		do
			if((${arrayD[i]}<${termarray[j]}||(i==$lenD-1)&&(j==$termarraylen-1)));then
				if(((i==$lenD-1)&&(j==$termarraylen-1)));then
					j=$[$j+1];
				fi
				if((j>=1));then
					sed -n ''${termarray[j-1]}','$[${termarray[j-1]}+8]'p' $FILENAME >>$retpath/result.log
				fi
				for((k=j-1;k>=1;k--));
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
		echo ${pendcase[i]} "log path:">>$retpath/result.log
		#=======log
		sed -n ''$[${arrayD[i]}+1]'p' $FILENAME >>$retpath/result.log
		echo -e "\n" >>$retpath/result.log
	done
fi

mv -f $retpath/result.log $dstpath