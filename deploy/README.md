# Tips

### Using local docker images for minikube

```shell
minikube image load app-frontend
minikube image load app-backend
minikube image load app-psql
```

### Figure out service host:port with minikube

```shell
minikube service sa-frontend-lb
```
