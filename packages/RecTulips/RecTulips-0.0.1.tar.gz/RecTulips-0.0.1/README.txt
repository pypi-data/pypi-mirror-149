Hello World !!
A Demo of Recomendation system Using SVD

How to work with ?
Super easy !! 
First import our Library . 
import Tulips

#Then start set your ratings like this

#Rate(user_id,item_id,rating,time)
Rate(1,3,5.0,'21-04-2022')


#Then the magic word to recommend 10 items to your client 

#TOP10(user_id)
TOP10(1)

Demo : 

import RecTulips as RS

RS.Rate(1,2,5,’10-04-2022 19:50:52’)
RS.Rate(1,5,4,’30-03-2022 10:34:10’)
RS.Rate(3,4,1,’11-03-2022 19:50:52’)
RS.Rate(5,3,2,’12-04-2022 17:05:02’)
RS.Rate(5,5,5,’22-04-2022 18:53:40’)
RS.Rate(4,1,4,’25-04-2022 20:51:00’)
RS.Rate(7,9,4,’20-04-2022 20:20:13’)
RS.Rate(7,8,3,’25-03-2022 10:50:17’)
RS.Rate(2,7,5,’15-04-2022 22:25:01’)
RS.Rate(6,6,2,’21-04-2022 20:00:00’)
RS.Rate(8,10,3,’20-04-2022 20:12:00’)

Result = RS.TOP10(2) # Will return the id of the 10 item recommended to user (2) 
print(Result) # [1, 9, 5, 10, 8, 4, 2, 6, 3] 

