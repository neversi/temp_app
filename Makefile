
develop:
	docker run -v $(PWD)/app:/app/app --network host --name cv_develop -e PORT='7500' fastapi:test /start-reload.sh 

build:
	docker build -t fastapi:test .

run:
	docker run --network host --name cv_back -e PORT="7500" -e WORKERS_PER_CORE="0.5" fastapi:test 

stop-rm:
	docker stop develop
	docker rm develop

re:
	docker ps -a -q | xargs docker rm

re-run:
	docker rm cv_back
	docker run --network host --name cv_back -e PORT="7500" fastapi:test 