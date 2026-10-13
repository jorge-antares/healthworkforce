run:
	docker build -t healthforce-app .
	docker run -p 5000:5000 healthforce-app