# MAPING PORT 5431:5432 
docker run --name dbt_app -e POSTGRES_PASSWORD=postgres -p 5431:5432 -d postgres
# show information about the image
docker ps -a
