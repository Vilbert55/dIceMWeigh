scp *.py root@fsfp:/srv/dIceMWeigh/
scp *.sh root@fsfp:/srv/dIceMWeigh/
scp *.txt root@fsfp:/srv/dIceMWeigh/
scp *.service root@fsfp:/srv/dIceMWeigh/
scp -r templates root@fsfp:/srv/dIceMWeigh/
scp -r static root@fsfp:/srv/dIceMWeigh/
scp -r scripts root@fsfp:/srv/dIceMWeigh/

ssh root@fsfp systemctl restart dIceMWeigh
