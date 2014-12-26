DOM=$(date +%-d)
DOM=$((DOM % 7))
sudo -s mysqldump -u arlanda -parlanda ontolicious > /home/ubuntu/ontolicious-$DOM.sql
echo "done"
sudo -s mv /home/ubuntu/ontolicious-$DOM.sql /s3 
