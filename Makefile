runtunnel:
	cloudflared tunnel --url http://localhost:8081

runtestdb:
	docker run -d --name testdb -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=test_db -p 5435:5432 postgres:15