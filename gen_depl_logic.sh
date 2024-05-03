app_name=$1
arg1=$2
# cp ./templates/Dockerfile ./$app_name/
cat ./templates/Dockerfile | sed s/ARG1/$arg1/ >> ./$app_name/Dockerfile
eval $(minikube docker-env)
docker build ./$app_name/ -t $app_name-img
