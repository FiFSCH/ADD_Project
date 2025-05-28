# ADD Project - League of Legends Data :school:

The goal of this project is to create a system that uses RabbitMQ to send data across different components that are responsible for the following things:

1. __Producer__
    * Supplying data from the dataset to the Processor.
    * Supplying data from the dataset to the Uploader.
2. __Processor__
    * Data transformation.
3. __Uploader__
    * Uploding data sent by the Producer to the Database.
    * Uploding data sent by the Processor to the Database.
4. __Database__
    * Stores data provided by the Producer.
    * Stores data provided by the Processor.
5. __Presenter__
    * Presenting data supplied by the Processor. 

The architecture of the system can be obsserved on the following diagram:
![System architecture](https://github.com/user-attachments/assets/49bf23d9-62c6-4d5d-b7f0-1cda381c6b91)

## Dataset :scroll:

The dataset contains __24 226__ rows divided into __29__ columns.

>This dataset contains data about the first 15 minutes of gameplay for over 24 thousand solo queue matches taken from european servers (EUNE and EUW). Average ELO of the matches is between mid emerald to high diamond. The main purpose of the dataset is to help train models for predicting the winner based on how the first 15 minutes of the match played out.

__Link:__ [League of Legends Dataset](https://www.kaggle.com/datasets/karlorusovan/league-of-legends-soloq-matches-at-10-minutes-2024/data)

## Prerequisites :white_check_mark:
* __Docker__ 

## Installation :arrow_down:
1. Clone the repository
2. Within project's directory, create the containers:
   ```powershell
   docker-compose up -d
   ```
Successfull installation should result in the following containers being present in the Docker Desktop GUI:
![Installation success](https://github.com/user-attachments/assets/bb387ef6-ec1a-474a-a906-09873c078a39)

## Usage  :computer:

:bangbang: The insturctions assumes that no port changes were made on the end user's side. If needed please adjust accordingly. :bangbang:

From now on you can explore the logs of each container to see how the software behaves. 
<br/> Apart from that, other available ways of interacting with the system are:

1. __Frontend GUI (Presenter)__
>http://localhost:5173

![Presenter GUI](https://github.com/user-attachments/assets/fb44f72f-c05f-40a7-8cde-78ddda5c2b29)

2. __RabbitMQ GUI__
  
>http://localhost:15672/#/

_login:_ guest <br/>
_password:_ guest

3. __Connect to PostgreSQL DB__
```powershell
docker exec -it add_project-database-1 psql -U postgres -d lol_data
```

## Troubleshooting :rotating_light:
Sometimes it happens that during startup __Producer__ fails with the following error:
![Producer error](https://github.com/user-attachments/assets/f633153e-1e2d-458e-9a0c-fde2225f9c67)
In such case please simply run again only this component within Docker. One-time restart should resolve this issue.

![Producer restart](https://github.com/user-attachments/assets/ec3cbb3f-cad8-4d27-a9ea-297087bfe8a3)

## Authors :man_technologist: :man_artist: :mage_man:
* Maciej Czupyt, s22405
* Maciej Sulimka, s23635  
* Filip Schulz, s22455


