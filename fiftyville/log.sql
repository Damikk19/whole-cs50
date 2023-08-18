-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT * FROM crime_scene_reports WHERE street = "Humphrey Street"; -- looking for crimes that took place on Humphrey Street id 295 is what we are looking for

SELECT * from bakery_security_logs WHERE day = 28 AND month = 7; -- license plates may be a great helper (bakery logs security and people)

SELECT * from people WHERE license_plate in (SELECT license_plate FROM bakery_security_logs WHERE day = 28 AND month = 7); -- people that was seen the day the theft took place

SELECT * from interviews WHERE day = 28 AND month = 7; -- honestly I dont know if its a good way of looking for but theres no interviews in the next few days so that may make sense

-- phone call that took less than a minute is a red flag and id 161 is a red flag too:: theft took place at 10:15am
SELECT * from phone_calls WHERE day = 28 AND month = 7 AND  duration <= 60;
-- look for someone who left at 10:15 - 10:25 and someone who was taalking for less than a minute at the time
select * from bakery_security_logs WHERE day = 28 AND month = 7 AND hour >= 10;
-- someone who was whisperng for half an hours

SELECT name from people WHERE phone_number IN (SELECT caller from phone_calls WHERE day = 28 AND month = 7 AND  duration <= 60);

SELECT * from atm_transactions WHERE day = 28 AND month = 7; -- search based on the interview where someone saw thief at the atm
SELECT * from atm_transactions WHERE day = 28 AND month = 7 AND transaction_type = "withdraw";
SELECT * from atm_transactions WHERE day = 28 AND month = 7 AND transaction_type = "withdraw" AND atm_location = "Leggett Street"; -- link bank account with the person somehow (maybe by license plate or something)


select name from people WHERE license_plate IN (select license_plate from bakery_security_logs WHERE day = 28 AND month = 7 AND hour >= 10);
select name from people WHERE license_plate IN(SELECT * from atm_transactions WHERE day = 28 AND month = 7 AND transaction_type = "withdraw" AND atm_location = "Leggett Street");


-- link account number with license plate from bakery logs
SELECT name
FROM people JOIN bank_accounts ON people.id = bank_accounts.person_id JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE day = 28 AND month = 7 AND transaction_type = "withdraw" AND atm_location = "Leggett Street" -- people that were seen withdrawing money on the x street
INTERSECT
select name from people WHERE license_plate IN (select license_plate from bakery_security_logs WHERE day = 28 AND month = 7 AND hour >= 8) -- people that were seen in the bakery that day
INTERSECT
select name from people WHERE license_plate IN (select license_plate from bakery_security_logs WHERE day = 28 AND month = 7 AND hour >= 10 AND minute <= 30 AND activity = "exit") -- people that left bakery before 10:30
INTERSECT
SELECT name from people WHERE phone_number IN (SELECT caller from phone_calls WHERE day = 28 AND month = 7 AND  duration <= 60) -- people that were calling for less than 60 sec
INTERSECT
SELECT name
FROM people JOIN passengers ON people.passport_number = passengers.passport_number JOIN flights ON passengers.flight_id = flights.id
WHERE people.passport_number IN (SELECT passport_number FROM passengers)
INTERSECT
SELECT name
FROM people JOIN passengers ON people.passport_number = passengers.passport_number JOIN flights ON passengers.flight_id = flights.id
WHERE flights.id = 36;



SELECT * from phone_calls WHERE day = 28 AND month = 7 AND  duration <= 60 AND caller = "(367) 555-5533"  -- looking for a person bruce called to
SELECT name FROM people WHERE phone_number = "(375) 555-8161"