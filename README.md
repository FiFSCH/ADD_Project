# League of Legends Match Data ADD Project
Czupyt, Schulz, Sulimka
</br>
__Dataset:__ [League of Legends Dataset](https://www.kaggle.com/datasets/karlorusovan/league-of-legends-soloq-matches-at-10-minutes-2024/data)

## Instructions

### Build the Docker container

**Change to project directory**:
   ```powershell
   cd ...
   ```

**Create the containers**:
   ```powershell
   docker-compose up -d
   ```

**(Alternative) Create containers + hard reset (good if docker ignored changes to code)**:
   ```powershell
   docker-compose build --no-cache
   ```
   ```powershell
   docker-compose up -d
   ```

### Remove docker container

**Simple remove**:
   ```powershell
   docker-compose down
   ```
(or just press the delete button in the interface)

**Nuke**:
   ```powershell
   docker-compose down -v
   ```

### Connect to PostgreSQL Container

1.**Start the containers**:
   ```powershell
   docker-compose up -d
   ```

2.**Connect to container CLI + Connect to postgres + Connect to lol_data DB**:
```powershell
docker exec -it add_project-database-1 psql -U postgres -d lol_data
```

3.**You can execute SQL commands from here, such as**:
Check list of relations in current database
```sql
\dt - checks list of relations in current database
```

Get row count from given table (raw_data, processed_data)
```sql
SELECT COUNT(*) FROM [table];
```
