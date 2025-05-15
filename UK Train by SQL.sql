create database Uk_Train;
use Uk_Train ;
select *  from railway ;

-- calculate Duration
select 
DATEDIFF(MINUTE, [Departure Time], [Arrival Time]) AS Duration
from railway ; 

-- create taple Routes 
CREATE TABLE Routes (
    Route_ID INT IDENTITY(1,1) PRIMARY KEY ,
	Depature_station varchar(100) ,
	Arrival_Destination varchar(100) ,
	Duration time ,
	
);
select * from Routes ;

SELECT COUNT(DISTINCT [Transaction ID]) AS Amount from railway ;

-- create table transaction 
create table Transactions(
				Trasaction_ID  int primary key ,
				Ticket_ID int identity(1,1) ,
				Payment_Method varchar(100) ,
				Amount int ,
);
select * from Transactions ;

-- create table Tickets 
create table Tickets (
  Ticket_ID int primary key , 
  passenger_ID int ,
  Ticket_class varchar(100) ,
  Ticket_Type varchar(100) ,
  price int ,
  Date_of_Purchase date 
  ) ;

  select CONCAT([Departure Station],'--> ',[Arrival Destination] )as Route_Station
  from railway  ;

  select *  from railway;

  -- What is Peak Time Rides
   
SELECT 
	[Departure Time]  ,
    COUNT([Transaction ID]) AS Total_Rides
FROM railway
WHERE [Journey Status] IN ('On Time', 'Delayed')
GROUP BY [Departure Time]
ORDER BY [Departure Time] ASC;
-- Feature Engineering 

alter table railway add Duration as
DATEDIFF(MINUTE, [Departure Time], [Arrival Time]) 

ALTER TABLE railway
ADD Route_Station AS ([Departure Station] + '--> ' + [Arrival Destination]); 
select * from railway


ALTER TABLE railway 
add Month_of_Purchase as month([Date of Purchase]) ;

ALTER TABLE railway
ADD Monthname_of_Purchase AS DATENAME(month, [Date of Purchase]);

ALTER TABLE railway
ADD Purchase_hour AS Datename(hour,[Time of Purchase]);

alter table railway 
add Depature_day as day([Date of journey]) 

alter table railway 
add Depature_dayname as datename(day,[Date of journey])

ALTER TABLE railway
DROP COLUMN [Depature_dayname];

-- Data Analysis 
-- Total Tickets
select 
	count([Transaction ID])
from railway;

--"Where were the top tickets sold and by which payment_method?"
WITH RankedMethods AS (
    SELECT 
        [Departure Station],
        [Payment Method],
        COUNT(*) AS Tickets_Count,
        ROW_NUMBER() OVER (
            PARTITION BY [Departure Station]
            ORDER BY COUNT(*) DESC
        ) AS rn
    FROM railway
    GROUP BY [Departure Station], [Payment Method]
)
SELECT 
    [Departure Station],
    [Payment Method],
    Tickets_Count
FROM RankedMethods
WHERE rn = 1
ORDER BY [Departure Station];


-- reason for Delay
select
	[Reason for Delay] ,
	count(*) as 'count of Delay'
from railway
where [Refund Request]= 'Yes' and [Journey Status] = 'Delayed'
group by [Reason for Delay] 
order by 2 desc ;

-- how often are the rides
             
SELECT 
    CASE 
        WHEN DATEPART(HOUR, [Departure Time]) IN (0, 1, 2, 3) THEN '1.Early_time' 
        WHEN DATEPART(HOUR, [Departure Time]) IN (4, 5, 6, 7) THEN '2.Morning' 
        WHEN DATEPART(HOUR, [Departure Time]) IN (8, 9, 10, 11) THEN '3.Late Morning' 
        WHEN DATEPART(HOUR, [Departure Time]) IN (12, 13, 14, 15) THEN '4.Afternoon' 
        WHEN DATEPART(HOUR, [Departure Time]) IN (16, 17, 18, 19) THEN '5.Evening' 
        WHEN DATEPART(HOUR, [Departure Time]) IN (20, 21, 22, 23) THEN '6.Night'
    END AS Hour_category,
    COUNT([Transaction ID]) AS Total_Rides,
    COUNT(CASE WHEN [Journey Status] = 'On Time' THEN [Transaction ID] END) AS On_Time_Rides
FROM railway
WHERE [Journey Status] != 'Cancelled'
GROUP BY 
    CASE 
        WHEN DATEPART(HOUR, [Departure Time]) IN (0, 1, 2, 3) THEN '1.Early_time' 
        WHEN DATEPART(HOUR, [Departure Time]) IN (4, 5, 6, 7) THEN '2.Morning' 
        WHEN DATEPART(HOUR, [Departure Time]) IN (8, 9, 10, 11) THEN '3.Late Morning' 
        WHEN DATEPART(HOUR, [Departure Time]) IN (12, 13, 14, 15) THEN '4.Afternoon' 
        WHEN DATEPART(HOUR, [Departure Time]) IN (16, 17, 18, 19) THEN '5.Evening' 
        WHEN DATEPART(HOUR, [Departure Time]) IN (20, 21, 22, 23) THEN '6.Night'
    END
ORDER BY Hour_category ASC;


-- what is total REV , NET REV , Loss REV
select 
	 SUM([Price]) as Total_Rev ,
	 sum(case when [Refund Request]= 'No' Then [Price] end)as Net_REV,
	 sum(case when [Refund Request]= 'Yes' Then [Price] end)as Loss_REV

from railway 

-- what is percentage of the loss REV was due to delay ,cancelled
select 
	case 
		when  [Journey Status] = 'Cancelled' then 'Cancelled'
		when [Journey Status] = 'Delayed'    then  'Delayed'
		end  as reason_for_loss ,
		sum([Price]) as Loss_REV
from railway 
where [Refund Request]= 'Yes'
group by 
		case 
		when  [Journey Status] = 'Cancelled' then 'Cancelled'
		when [Journey Status] = 'Delayed'    then  'Delayed'
		end ;

-- whta is reason for Delay 
select 
      [Reason For Delay] ,
	  SUM([Price]) as loss_REV
from railway  
where [Refund Request]= 'Yes' and [Journey Status] in ('Cancelled' ,'Delayed')

Group by [Reason For Delay] 
order by 2 desc ;



