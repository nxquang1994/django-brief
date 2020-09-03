
start: stop
	@docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

start_log: stop
	@docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
	@docker-compose logs -f

stop:
	@docker-compose down

stop_orphans:
	@docker-compose down --remove-orphans

status:
	@docker-compose ps

test:
	@tools/runtest.sh

build:
	@docker-compose -f docker-compose.yml -f docker-compose.dev.yml build django

reset_db:
	@tools/resetdb.sh
