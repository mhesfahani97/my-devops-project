running the project locally:

git clone https://github.com/mhesfahani97/my-devops-project.git
cd my-devops-project
docker compose pull
docker compose up -d gitlab runner grafana prometheus mongo-exporter elasticsearch kibana logstash
wait to upping gitlab, it takes some minuetes (5 ~ 10)
gitlab user: root
gitlab password:
docker exec -it gitlab grep 'Password:' /etc/gitlab/initial_root_password
in a browser access to gitlab `http://localhost:80`
create a project with my-devops-project name add your public ssh key to gitlab
again in your local repository:
cd my-devops-project
git remote add gitlab git@localhost:root/my-devops-project.git
vim docker-compose.yml:
uncomment application and database services




docker compose up -d gitlab runner
http://localhost
http://localhost/admin/runners/new
tag: production-like
docker exec -it runner bash
http://gitlab
git remote add gitlab git@gitlab.com:your-username/your-project.git

root

guide sources:
[ELK-Medium](https://medium.com/@lopchannabeen138/deploying-elk-inside-docker-container-docker-compose-4a88682c7643)
