
.PHONY: local rebuild run

local:
	LOCATION=lenauweg venv/bin/python3 -m flask run --host=0.0.0.0

rebuild:
	-sudo docker stop callmonitor
	-sudo docker rm callmonitor
	sudo docker build -t schluete/callmonitor -f Dockerfile .

run:
	sudo docker run \
		-d --name callmonitor \
		--restart unless-stopped \
		--env TZ="Europe/Berlin" \
		--env LOCATION=lenauweg \
		--network=host \
		-v /home/schluete/iot-docker-setup/logs:/log \
		-v /home/schluete/iot-docker-setup/callmonitor:/database \
		schluete/callmonitor
