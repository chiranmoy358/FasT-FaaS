app_name=$1
depl_id=$2
arg1=$3
yml_path=./$app_name/$depl_id.yml
job_name=$app_name-$depl_id

cat ./templates/job.yml | sed s/APPNAME/$app_name/ | sed s/DEPLID/$depl_id/ | sed s/ARG1/$arg1/ >> $yml_path

kubectl apply -f $yml_path 1> /dev/null

kubectl wait --for=condition=complete --timeout=1m -f $yml_path 1> /dev/null

start_time=$(kubectl get job $job_name -o=jsonpath='{.status.startTime}')
completion_time=$(kubectl get job $job_name -o=jsonpath='{.status.completionTime}')

start_timestamp=$(date -d "$start_time" +%s)
completion_timestamp=$(date -d "$completion_time" +%s)

execution_time=$((completion_timestamp - start_timestamp))

pod_name=$(kubectl get pods -l job-name=$job_name -o=jsonpath='{.items[0].metadata.name}')
output=$(kubectl logs $pod_name)

echo $output
echo ${execution_time} >> ./$app_name/exec_times.txt

kubectl delete job $job_name 1> /dev/null

rm $yml_path
