app_name=$1
cp ./templates/Dockerfile ./$app_name/
eval $(minikube docker-env)
docker build ./$app_name/ -t $app_name-img
