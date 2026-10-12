602. Friend Requests II: Who Has the Most Friends
Solved
Medium
Topics
premium lock icon
Companies
Hint
SQL Schema
Pandas Schema
Table: RequestAccepted

+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| requester_id   | int     |
| accepter_id    | int     |
| accept_date    | date    |
+----------------+---------+
(requester_id, accepter_id) is the primary key (combination of columns with unique values) for this table.
This table contains the ID of the user who sent the request, the ID of the user who received the request, and the date when the request was accepted.
 

Write a solution to find the people who have the most friends and the most friends number.

The test cases are generated so that only one person has the most friends.

The result format is in the following example.

 

Example 1:

Input: 
RequestAccepted table:
+--------------+-------------+-------------+
| requester_id | accepter_id | accept_date |
+--------------+-------------+-------------+
| 1            | 2           | 2016/06/03  |
| 1            | 3           | 2016/06/08  |
| 2            | 3           | 2016/06/08  |
| 3            | 4           | 2016/06/09  |
+--------------+-------------+-------------+
Output: 
+----+-----+
| id | num |
+----+-----+
| 3  | 3   |
+----+-----+
Explanation: 
The person with id 3 is a friend of people 1, 2, and 4, so he has three friends in total, which is the most number than any others.

CODE:
with all_friends as ( select requester_id from RequestAccepted UNION ALL select accepter_id from RequestAccepted ) 
, friends as ( select requester_id , count(*) as num  from all_friends group by requester_id)
select top 1 requester_id as id  , num from friends order by num desc;


PATTERN:

An entity can appear in either of two columns, and we need its total..

So when the data is in multiple columns and 
you need to find out the total of id's or etc from all those columns 
then we can use this process , where we will union all the those columns 
and do a count of it then we will get the asnwer . 

SUPPOSE

RequestAccepted

requester   accepter
---------   --------
1           2
1           3
2           3


id
--
1
1
2
2
3
3


id    num
--    ---
1      2
2      2
3      2