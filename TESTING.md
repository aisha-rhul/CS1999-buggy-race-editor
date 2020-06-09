**TESTING**
===================

The following tests were carried out and the results were as stated below.
1. Unit Testing
2. Black-box Testing
3. User Testing


**Unit testing**
--------------
During the development process, testing was conducted on all functions that retured a numeric value.

**Test 1 - Function validate_integer()**
The  purpose of the function is to return a Boolean value after taking two integer parameters and determining if the first parameter is greater than or equal to the second parameter. Test data was used to check all possible instances and this was compared against an expected value using the self.eassrtEqual() function in the unit-test library in Python. 

>Test data: (5, 3), (4, 4), (3, 4), (-3, 4), (3, -4), (0, -4), (0, 0)<br>
>Expected Results: All tests should return True except (3,4) and (-3, 4)<br>
>Results: All tests passed

**Test 2 - Function get_buggy_record()**
The purpose of this function is to return a record from the Buggy table given the buggy id as a parameter. The record for the default buggy was stored in a variable and was compared to the returned result of the function when the default buggy’s id was passed to it. 

>Test data: buggy_id = 1 (existing record), buggy_id = 11 (non existent record)<br>
>Expected Results: Existing record found, Non-existent record not found<br>
>Results: All tests passed

**Test 3 - Function  get_last_buggy**
The purpose of the function is to return the buggy id of the last record in the Buggy table. The buggy id of the last record was compared to the returned result of the function using self.assertEqual().

>Test data: function call to get_last_buggy()<br>
>Expected Results: buggy_id of the last record in the database table Buggy<br>
>Results: Test passed

**Test 4 - Function get_records()**
The purpose of the function is to return all the records from the Buggy table. The expected result was stored in a variable and was compared to the returned result of the function using self.assertEqual().

>Test data: function call to get_records()<br>
>Expected Results: All records in the database table Buggy returned<br>
>Results: All tests passed

**Test 5 - Function delete_buggy()**
The purpose of this function is to delete a buggy from the Buggy table and the Ownership table given the buggy id as a parameter. Once the buggy had been successfully deleted from both tables, the message “Buggy deleted” should be received. This was compared to the string “Buggy deleted” using the self.assertEqual function().

>Test data: function call to delete_buggy(1)<br>
>Expected Results: buggy id = 1 records in tables Buggy and User tables<br>
>Results: Test passed, records were successfully deleted


Testing for validation
--------------------------

 - Number of wheels has to be an even integer greater than 4. This was
   tested by submitting integers less than 4 and odd integers greater
   than 4.
   
 - Primary power unit has to be an integer greater than 0. This was   
   tested by submitting integers less than 0.
   
 - Auxiliary power unit has to be an integer greater than 0 if auxiliary
   power type is chosen. This was tested by submitting 0 for the   
   auxiliary power units when the auxiliary power type was chosen.

 - Auxiliary power unit has to be 0 if no auxiliary power type is   
   chosen. This was tested by submitting integers other than 0 when no  
   auxiliary power type was chosen.

 - Primary/auxiliary power unit can only be 1 if primary/auxiliary power
   type is consumable. This was tested by submitting integers other than
   1 when the primary/auxiliary power type chosen was consumable.

 - Hamster booster has to be an integer greater than or equal to 0 if   
   primary/auxiliary power type is Hamster. This was tested by   
   submitting integers other than 0 when both primary/auxiliary power   
   type chosen was not Hamster.

 - Hamster booster has to be 0 if primary/auxiliary power type is not   
   Hamster. This was tested by submitting integers other than 0 when the
   primary/auxiliary power type chosen was not Hamster.

 - Number of tyres must be greater than or equal to the number of wheels
   chosen. This was tested by submitting integers less than the number  
   of wheels chosen.

 - Number of attacks has to be an integer greater than 0 if attack is   
   chosen. This was tested by submitting integers less than 1 when an   
   attack was chosen.

 - Number of attacks has to be 0 if no attack is chosen. This was tested
   by submitting integers other than 0 when no attack was chosen.

Each test case described above was conducted to see if the program displayed the appropriate error message(s) and denied the submission of the record to be written to the database in the event of invalid buggy records. For each validation check, permissible values were also tested to see if the program did submit the record to be written to the database.

Results: All tests passed


Testing tools 
-------------
Web testing can also be carried out using other tools listed below. However, due to lack of time, these options were not investigated.

+ Selenium
+ Katalon Studio
+ UFT One


Black-box Testing
---------------------
I tried to use the approach of Black-box testing to test each function in the python code to see if it worked correctly. This was carried out after the function was written together with its dependencies. Test cases were created to examine the function behavior. This proved very useful as many bugs were found during testing and they were eradicated.

User Testing
---------------------
Once the application was fully functional, I tested it generally to see if it worked as intended.  I navigated to each page to see it it loads without errors. Also tested the input by entering various buggy options to generate a new buggy and compares the results with expected. I also tested each of the buttons to see if they had the desired effect. These tests were all successful. 

I used the built-in debugger within my web browser by pressing **F12** to find issues which were difficult to trace. This is a useful tool as it can help monitor network transfers, console messages, inspect HTML code, edit styles, etc. This is very helpful as it can help check if the necessary files have loaded for a certain web page. Furthermore, it was useful for styling the pages, as browsers like Firefox has a built-in style editor which can be used in real time.

Conclusion
---------------------
Basic tests shown above have reported no issues. However, extensive user testing is required to identify potential bugs.


