docker compose up -d gitlab runner
http://localhost
http://localhost/admin/runners/new
tag: production-like
docker exec -it runner bash
http://gitlab

root
docker exec -it gitlab grep 'Password:' /etc/gitlab/initial_root_password

guide sources:
[ELK-Medium](https://medium.com/@lopchannabeen138/deploying-elk-inside-docker-container-docker-compose-4a88682c7643)
