base="/srv/dIceMWeigh/log"
systemctl stop dIceMWeigh
cd $base
date=`date +%Y-%m-%d`
tar -cpjf dIceMWeigh_logs_$date.tbz *.log
for i in *.log;do
  echo "rotate" >$i
done
systemctl start dIceMWeigh