main : 
	echo "use run-<store_type>store to run container and stop-all-container to stop all"

run-all-store : run-index-store run-vector-store run-document-store run-chat-store
	make run-index-store
	make run-vector-store
	make run-chat-store
	make run-document-store

stop-all-container : run-all-store
	sudo docker container stop $$(sudo docker container ps -q -a)

run-index-store : ./database/index_db/index-db-docker-compose.yaml
	sudo docker compose -f ./database/index_db/index-db-docker-compose.yaml up -d

run-vector-store : ./database/vector_db/vector-db-docker-compose.yaml
	sudo docker compose -f ./database/vector_db/vector-db-docker-compose.yaml up -d

run-document-store : ./database/document_db/document-db-docker-compose.yaml
	sudo docker compose -f ./database/document_db/document-db-docker-compose.yaml up -d

run-chat-store : ./database/chat_db/chat-db-docker-compose.yaml 
	sudo docker compose -f ./database/chat_db/chat-db-docker-compose.yaml up -d


