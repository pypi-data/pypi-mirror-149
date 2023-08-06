print(""" 
      Q1)
        a)  update Employee
            set salary = 50000
            where Employee_no = 2;
        b)  select name from Employee
            where salary > 50000;
        c)  alter table Department add Employee_no INT;
            alter table Department
            add foreign key (Employee_no) references Employee(Employee_no);
        d)  ALTER TABLE Employee
            ALTER address SET DEFAULT 'Mumbai';
        e)  select avg(salary) from Employee;
        
        
        Q2)
            a)  select Employee_name from Employee
                where Employee_name like "%s%";
            b)  select Employee_name, job from Employee
                where Dept_no in (10,20);
            c)  select Employee_name, job from Employee
                order by Employee_name asc;
            d)  SELECT Dept_no, COUNT(*) as no_of_emp
                FROM Employee
                GROUP BY Dept_no;
            e)  SELECT Dept_no, AVG(salary), COUNT(*)
                FROM Employee
                GROUP BY Dept_no
                HAVING COUNT(*) > 5;
                
                
        Q3)
            a)  alter table Supply
                add pincode INT
                add City varchar(20);
            b)  create view supplier as
                select Id_no, Name
                from Supply;
            c)  alter table product
                add primary key (P_no);
            d)  create index index1
                on supply (S_code);
            e)  alter table emp
                modify pincod

        Q4)
            a)  select Player.Roll_no, Player.Name, Match.Match_Date
                from Player, Match
                where Player.Roll_no = Matcht.Roll_no;
            b)  select Player.Roll_no, Match.Match_no from Player, Match
                where Player.Roll_no = Match.Roll_no and Match.Match_no = 2;
            c)  create view info as
                select Player.Roll_no, Player.Name, Match.Match_no, Match.Match_Date
                from Player, Match
                where Player.Roll_no = Match.Roll_no;
            d)  select min(Roll_no) from Player;
            e)  select * from Match
                where Match_date in
                ( select max(Match_date)
                From Match );
        Q5)
            a)  SELECT *
                FROM employees
                WHERE salary IN
                (SELECT max(salary)
                FROM employees
                GROUP BY job_name)
                ORDER BY salary DESC;
            b)  select length('ENGINEER') as len;
            c)  select Employee.Employee_name, Department.Dept_location,
                Department.Dept_Name from Employee
                inner join Department on Employee.Dept_no = Department.Dept_no and
                salary>1500;
            d)  SELECT Dept_no, SUM(salary)
                FROM employees
                GROUP BY Dept_no;
       Q6)
            a)  select Instructor.I_id, Instructor.I_name from Instructor
                inner join Student on Student.S_id = Instructor.I_id;
            b)  select * from Instructor
                where Instructor.I_id not in
                (select Student.S_id from Student);
            c)  ALTER TABLE Instructor ADD age INT;
            d)  select S_name from Student
                where S_name like "%ra%"; 
                
                
    Q7)
                (persons table)
                create table persons
                
                (id int,
                firstname varchar(30),
                lastname varchar(30),
                age int );
                
                insert into persons values
                (1, "mahesh", "sharma", 30),
                (2, "suresh", "varma", 30),
                (3, "ramesh", "vishwakarma", 30);
                
                (orders table)
                CREATE TABLE Orders (
                OrderID int NOT NULL,
                OrderNumber int NOT NULL,
                PersonID int
                );
                
                insert into orders values
                (1, 4456, 3),
                (2, 5676, 1),
                (3, 7687, 2);
                
                (not null constraint)
                alter table persons
                modify age int not null;
                
                (add unique key constraint)
                alter table persons
                add constraint uc_con unique (id);
                
                (drop unique key constraint)
                alter table persons
                drop constraint uc_con;
                
                (add primary key constraint)
                alter table persons
                add constraint pk_con primary key (id);
                
                (drop primary key constraint)
                alter table persons
                drop primary key;
                
                (add foreign key constraint)
                alter table orders
                add constraint fk_con foreign key(PersonID) references persons(id);
                
                (drop foreign key constraint)
                alter table orders
                drop foreign key fk_con;
                
                (add check constraint)
                alter table persons
                add constraint chk_age check (age>=30);
                
                (drop check constraint)
                alter table persons
                drop constraint chk_age;
                
                (add default constraint)
                alter table persons
                alter age set default 20;
                
                (drop default constraint)
                alter table persons
                alter age drop default;
                
                
                
                
        Q8) create table student (id integer, name varchar(10), marks integer);
                insert into student (id, name, marks)
                values
                (1, "Rahul", 10),
                (2, "Karan", 20),
                (3, "Neha", 30),
                (4, "Kunal", 40);
                
                select count(*) from student;
                select sum(marks) from student;
                select avg(marks) from student;
                select max(marks) from student;
                select min(marks) from student;        
                
                
        Q9)
                (to add new column)
                ALTER TABLE student ADD L_name varchar(20);
                
                (to drop column)
                ALTER TABLE student DROP column L_name;
                
                (to set the default value to a column)
                ALTER TABLE student
                ALTER address SET DEFAULT 'Mumbai';
                
                (to drop the default value of a column)
                alter table student
                modify Address char(30);
                
                (to change column name)
                alter table student
                change L_name Last_name varchar(20);
                
                (add constraint)
                alter table student
                add constraint con_first unique(id);
                
                (drop constraint)
                alter table student
                drop constraint con_first;
                
                (to rename column)
                alter table student
                rename column L_name to Last_name;



        Q10)
                (AND operator)
                select * from student
                where name like '%a%' and marks>10;
                
                (OR operator)
                select * from student
                where name like '%a%' or marks>10;
                
                (NOT)
                select * from student
                where not marks>20;
                
                (find name ending with "r")
                select * from student
                where name like '%r';
                
                (find name starting with "n")
                select * from student
                where name like 'n%';
                
                (find name containing "a")
                select * from student
                where name like '%a%';
                
                
                
                
                # over
                Next DBMS.txt
                Q1)
  a)update Employee set salary = 50000 where Employee_no = 2;

  b)select name from Employee where salary > 50000;

  c)alter table Department add Employee_no INT;
    alter table Department add foreign key (Employee_no) references Employee(Employee_no);

  d)ALTER TABLE Employee ALTER address SET DEFAULT 'Mumbai';

  e)select avg(salary) from Employee;

Q2)
  a)select Employee_name from Employee where Employee_name like "%s%";

  b)select Employee_name, job from Employee where Dept_no in (10,20);

  c)select Employee_name, job from Employee order by Employee_name asc;

  d)SELECT Dept_no, COUNT(*) as no_of_emp FROM Employee GROUP BY Dept_no;
	
  e)SELECT Dept_no, AVG(salary), COUNT(*) FROM Employee GROUP BY Dept_no HAVING COUNT(*) > 5;

Q3)
  a)alter table Supply add pincode INT add City varchar(20);
	
  b)create view supplier as select Id_no, Name from Supply;

  c)alter table product add primary key (P_no);

  d)create index index1 on supply (S_code);

  e)alter table emp modify pincode integer(5);

Q4)
  a)select Player.Roll_no, Player.Name, Match.Match_Date from Player, Match where Player.Roll_no = Matcht.Roll_no;

  b)select Player.Roll_no, Match.Match_no from Player, Match where Player.Roll_no = Match.Roll_no and Match.Match_no = 2;

  c)create view info as select Player.Roll_no, Player.Name, Match.Match_no, Match.Match_Date from Player, 
    Matchwhere Player.Roll_no = Match.Roll_no; 

  d)select min(Roll_no) from Player;

  e)select * from Match where Match_date in (select max(Match_date) From Match);

Q5) 
  a)SELECT * FROM employees WHERE salary IN (SELECT max(salary) FROM employees GROUP BY job_name) ORDER BY salary DESC;

  b)select length('ENGINEER') as len;

  c)select Employee_name, Dept_location and Dept_Name from Employee, Department where salary>1500;

  d)SELECT department_id, SUM(salary) FROM employees GROUP BY department_id;

Q6)
  a)select S_id, S_name from Student intersect select I_id, I_name from Instructor;

  b)select I_id, I_name from Instructor except select S_id, S_name from Student;

  c)ALTER TABLE Instructor ADD age INT;

  d)select S_name from Student where S_name like "%ra%";

Q7)	


Q8)create table student (id integer, name varchar(10), marks integer);
 
   insert into student (id, name, marks) values (1, "Rahul", 10), (2, "Karan", 20), (3, "Neha", 30), (4, "Kunal", 40);

   select count(*) from student;

   select sum(marks) from student;

   select avg(marks) from student;

   select max(marks) from student;

   select min(marks) from student;

Q9)	
  (to add new column)
  ALTER TABLE student ADD L_name varchar(20); 

  (to drop column)
  ALTER TABLE student DROP column L_name; 

  (to set the default value to a column)
  ALTER TABLE student ALTER address SET DEFAULT 'Mumbai'; 

  (to drop the default value of a column)
  alter table student modify Address char(30);  

  (to change column name)
  alter table student change L_name Last_name varchar(20); 

  (add constraint)
  alter table student add constraint con_first unique(id); 

  (drop constraint)	
  alter table student drop constraint con_first;

  (to rename column)	
  alter table student rename column L_name to Last_name 

Q10)	
   (AND operator)
   select * from student where name like '%a%' and marks>10;

   (OR operator)
   select * from student where name like '%a%' or marks>10;

   (NOT)
   select * from student where not marks>20;

   (find name ending with "r")
   select * from student where name like '%r';

   (find name starting with "n")
   select * from student where name like 'n%';

   (find name containing "a")
   select * from student

      
      """)