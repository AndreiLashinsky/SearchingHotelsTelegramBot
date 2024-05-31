# Searching Hotels Telegram Bot

## Project Overview
This telegram bot based on python module “telebot” uses endpoints of https://rapidapi.com/apidojo/api/hotels4/ to find Hotels that will suit your needs according to filter applied to search.


## Installation Instructions
- Clone this repository to your IDE 
- Make sure that requirements.txt made his duty
- Import your file .env with bot token and site API<br>
Site API can be found here - https://rapidapi.com/apidojo/api/hotels4/<br>
To obtain bot token visit @BotFather - https://telegram.me/BotFather/<br>
- Open IDE with project and run main

## Usage Guide
While program is running you will find your bot by following link that @BotFather gave to you.<br>
Let’s start!  Enter first command “/start”. Bot will show you options that you have to configure according to your
 needs to complete a request to the site API.<br> 
<b>Choose city</b>: at this step you need to enter place/city where you want to go. After sending message with your place
 bot will ask you to confirm your choice by choosing one of places that he will offer to you.<br>
<b>Choose dates</b>: here you need to enter dates of your travel according to pattern that bot will ask you.
“DD-MM-YYYY DD-MM-YYYY” – date of arrival and date of departure respectively.<br>
<b>Modify people quantity</b>: here you have to enter all the persons, including children. While modifying children just enter their ages.<br>
<b>Choose price</b>: just enter minimum and maximum (using space) price you want to pay.<br>
<b>Search</b>: this command will work only if all the filters below are filled with user. Except children, there
can be nothing. After command used bot will show you all the hotels that matches to your filter. By clicking
to any of them bot will send to you a photo of this place and will offer to get a short summary of this place.  

## Configuration
.json files that comes from site as response containing a lot of information like address, site link, overviews
that could be added to bot answers at users request. 


## Contributing Guidelines
This project  was done for educational proposes and can serve like an example of bot and example of working with .json files.


## License
GNU
