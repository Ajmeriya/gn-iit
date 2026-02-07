"""
Hardcoded Question Bank
50 MCQ, 50 Subjective (SQL), 20 DSA questions
Each DSA question has 5 test cases (basic, edge, max boundary, etc.)
Questions are categorized by skills/technologies for resume-based selection
"""

# MCQ Questions (50 questions covering various technologies)
MCQ_QUESTIONS = [
    # Python Basics (10 questions)
    {
        "question": "What is the output of: print(2 ** 3 ** 2)?",
        "options": ["64", "512", "729", "Error"],
        "correct_answer": "512",
        "difficulty": "Medium",
        "tags": ["python", "operators"],
        "estimated_time": 1
    },
    {
        "question": "Which method is used to add an element to the end of a list in Python?",
        "options": ["append()", "add()", "insert()", "push()"],
        "correct_answer": "append()",
        "difficulty": "Low",
        "tags": ["python", "data-structures"],
        "estimated_time": 1
    },
    {
        "question": "What is the time complexity of accessing an element in a Python dictionary?",
        "options": ["O(1)", "O(n)", "O(log n)", "O(n log n)"],
        "correct_answer": "O(1)",
        "difficulty": "Medium",
        "tags": ["python", "data-structures", "complexity"],
        "estimated_time": 2
    },
    {
        "question": "What does the 'yield' keyword do in Python?",
        "options": ["Returns a value and stops execution", "Creates a generator function", "Raises an exception", "Imports a module"],
        "correct_answer": "Creates a generator function",
        "difficulty": "Medium",
        "tags": ["python", "generators"],
        "estimated_time": 2
    },
    {
        "question": "What is the difference between '==' and 'is' in Python?",
        "options": ["No difference", "'==' compares values, 'is' compares identity", "'is' compares values, '==' compares identity", "Both compare identity"],
        "correct_answer": "'==' compares values, 'is' compares identity",
        "difficulty": "Medium",
        "tags": ["python", "operators"],
        "estimated_time": 2
    },
    {
        "question": "What is a decorator in Python?",
        "options": ["A function that modifies another function", "A class that wraps another class", "A module import statement", "A variable type"],
        "correct_answer": "A function that modifies another function",
        "difficulty": "High",
        "tags": ["python", "decorators"],
        "estimated_time": 3
    },
    {
        "question": "What is the output of: [x for x in range(5) if x % 2 == 0]",
        "options": ["[0, 2, 4]", "[1, 3]", "[0, 1, 2, 3, 4]", "[2, 4]"],
        "correct_answer": "[0, 2, 4]",
        "difficulty": "Low",
        "tags": ["python", "list-comprehension"],
        "estimated_time": 1
    },
    {
        "question": "What is the purpose of __init__ method in Python?",
        "options": ["To initialize class variables", "To destroy objects", "To import modules", "To handle exceptions"],
        "correct_answer": "To initialize class variables",
        "difficulty": "Low",
        "tags": ["python", "oop"],
        "estimated_time": 1
    },
    {
        "question": "What is the Global Interpreter Lock (GIL) in Python?",
        "options": ["A lock that allows only one thread to execute Python bytecode at a time", "A global variable", "A module", "A data structure"],
        "correct_answer": "A lock that allows only one thread to execute Python bytecode at a time",
        "difficulty": "High",
        "tags": ["python", "multithreading"],
        "estimated_time": 3
    },
    {
        "question": "What is the difference between list and tuple in Python?",
        "options": ["Lists are mutable, tuples are immutable", "Tuples are mutable, lists are immutable", "No difference", "Lists can only store integers"],
        "correct_answer": "Lists are mutable, tuples are immutable",
        "difficulty": "Low",
        "tags": ["python", "data-structures"],
        "estimated_time": 1
    },
    
    # Java Basics (10 questions)
    {
        "question": "What is the default value of a boolean variable in Java?",
        "options": ["true", "false", "null", "0"],
        "correct_answer": "false",
        "difficulty": "Low",
        "tags": ["java", "basics"],
        "estimated_time": 1
    },
    {
        "question": "What is method overloading in Java?",
        "options": ["Having multiple methods with same name but different parameters", "Inheriting methods from parent class", "Overriding parent class methods", "Removing methods"],
        "correct_answer": "Having multiple methods with same name but different parameters",
        "difficulty": "Medium",
        "tags": ["java", "oop"],
        "estimated_time": 2
    },
    {
        "question": "What is the difference between == and .equals() in Java?",
        "options": ["== compares references, .equals() compares values", ".equals() compares references, == compares values", "No difference", "Both compare references"],
        "correct_answer": "== compares references, .equals() compares values",
        "difficulty": "Medium",
        "tags": ["java", "operators"],
        "estimated_time": 2
    },
    {
        "question": "What is a static method in Java?",
        "options": ["A method that belongs to the class, not instance", "A method that cannot be called", "A method that changes state", "A private method"],
        "correct_answer": "A method that belongs to the class, not instance",
        "difficulty": "Medium",
        "tags": ["java", "oop"],
        "estimated_time": 2
    },
    {
        "question": "What is the purpose of 'final' keyword in Java?",
        "options": ["To prevent inheritance, overriding, or modification", "To make variables public", "To create constants only", "To enable garbage collection"],
        "correct_answer": "To prevent inheritance, overriding, or modification",
        "difficulty": "Medium",
        "tags": ["java", "keywords"],
        "estimated_time": 2
    },
    {
        "question": "What is the difference between ArrayList and LinkedList in Java?",
        "options": ["ArrayList uses array, LinkedList uses nodes", "LinkedList uses array, ArrayList uses nodes", "No difference", "Both use arrays"],
        "correct_answer": "ArrayList uses array, LinkedList uses nodes",
        "difficulty": "Medium",
        "tags": ["java", "data-structures"],
        "estimated_time": 2
    },
    {
        "question": "What is exception handling in Java?",
        "options": ["Mechanism to handle runtime errors", "A data structure", "A design pattern", "A loop construct"],
        "correct_answer": "Mechanism to handle runtime errors",
        "difficulty": "Low",
        "tags": ["java", "exceptions"],
        "estimated_time": 1
    },
    {
        "question": "What is the time complexity of HashMap.get() in Java?",
        "options": ["O(1)", "O(n)", "O(log n)", "O(n log n)"],
        "correct_answer": "O(1)",
        "difficulty": "Medium",
        "tags": ["java", "data-structures", "complexity"],
        "estimated_time": 2
    },
    {
        "question": "What is the difference between checked and unchecked exceptions in Java?",
        "options": ["Checked exceptions must be handled, unchecked don't", "Unchecked exceptions must be handled, checked don't", "No difference", "Both are the same"],
        "correct_answer": "Checked exceptions must be handled, unchecked don't",
        "difficulty": "Medium",
        "tags": ["java", "exceptions"],
        "estimated_time": 2
    },
    {
        "question": "What is polymorphism in Java?",
        "options": ["Ability of objects to take multiple forms", "A data structure", "A loop type", "A variable type"],
        "correct_answer": "Ability of objects to take multiple forms",
        "difficulty": "Medium",
        "tags": ["java", "oop"],
        "estimated_time": 2
    },
    
    # JavaScript (10 questions)
    {
        "question": "What is the difference between var, let, and const in JavaScript?",
        "options": ["var is function-scoped, let/const are block-scoped", "All are the same", "let is function-scoped, var/const are block-scoped", "const is function-scoped"],
        "correct_answer": "var is function-scoped, let/const are block-scoped",
        "difficulty": "Medium",
        "tags": ["javascript", "variables"],
        "estimated_time": 2
    },
    {
        "question": "What is closure in JavaScript?",
        "options": ["Function with access to outer function's variables", "A data structure", "A loop", "A variable type"],
        "correct_answer": "Function with access to outer function's variables",
        "difficulty": "High",
        "tags": ["javascript", "closures"],
        "estimated_time": 3
    },
    {
        "question": "What is the difference between == and === in JavaScript?",
        "options": ["== compares values with type coercion, === compares without coercion", "=== compares values with type coercion, == compares without coercion", "No difference", "Both are the same"],
        "correct_answer": "== compares values with type coercion, === compares without coercion",
        "difficulty": "Low",
        "tags": ["javascript", "operators"],
        "estimated_time": 1
    },
    {
        "question": "What is a promise in JavaScript?",
        "options": ["Object representing eventual completion of async operation", "A data structure", "A loop", "A function"],
        "correct_answer": "Object representing eventual completion of async operation",
        "difficulty": "Medium",
        "tags": ["javascript", "async"],
        "estimated_time": 2
    },
    {
        "question": "What is the event loop in JavaScript?",
        "options": ["Mechanism that handles async operations", "A data structure", "A loop construct", "A variable"],
        "correct_answer": "Mechanism that handles async operations",
        "difficulty": "High",
        "tags": ["javascript", "async"],
        "estimated_time": 3
    },
    {
        "question": "What is the difference between null and undefined in JavaScript?",
        "options": ["null is assigned value, undefined is default", "undefined is assigned value, null is default", "No difference", "Both are the same"],
        "correct_answer": "null is assigned value, undefined is default",
        "difficulty": "Low",
        "tags": ["javascript", "basics"],
        "estimated_time": 1
    },
    {
        "question": "What is hoisting in JavaScript?",
        "options": ["Moving declarations to top of scope", "A data structure", "A function", "A loop"],
        "correct_answer": "Moving declarations to top of scope",
        "difficulty": "Medium",
        "tags": ["javascript", "basics"],
        "estimated_time": 2
    },
    {
        "question": "What is the purpose of 'this' keyword in JavaScript?",
        "options": ["Refers to the object that owns the function", "A data type", "A loop", "A variable"],
        "correct_answer": "Refers to the object that owns the function",
        "difficulty": "Medium",
        "tags": ["javascript", "basics"],
        "estimated_time": 2
    },
    {
        "question": "What is async/await in JavaScript?",
        "options": ["Syntax for handling promises", "A data structure", "A loop", "A variable type"],
        "correct_answer": "Syntax for handling promises",
        "difficulty": "Medium",
        "tags": ["javascript", "async"],
        "estimated_time": 2
    },
    {
        "question": "What is the difference between map() and forEach() in JavaScript?",
        "options": ["map() returns new array, forEach() returns undefined", "forEach() returns new array, map() returns undefined", "No difference", "Both return arrays"],
        "correct_answer": "map() returns new array, forEach() returns undefined",
        "difficulty": "Low",
        "tags": ["javascript", "arrays"],
        "estimated_time": 1
    },
    
    # Database/SQL (10 questions)
    {
        "question": "What is the difference between INNER JOIN and LEFT JOIN?",
        "options": ["INNER JOIN returns matching rows, LEFT JOIN returns all left rows", "LEFT JOIN returns matching rows, INNER JOIN returns all left rows", "No difference", "Both are the same"],
        "correct_answer": "INNER JOIN returns matching rows, LEFT JOIN returns all left rows",
        "difficulty": "Medium",
        "tags": ["sql", "joins"],
        "estimated_time": 2
    },
    {
        "question": "What is a primary key in SQL?",
        "options": ["Unique identifier for a row", "A foreign key", "An index", "A constraint"],
        "correct_answer": "Unique identifier for a row",
        "difficulty": "Low",
        "tags": ["sql", "basics"],
        "estimated_time": 1
    },
    {
        "question": "What is normalization in database design?",
        "options": ["Process of organizing data to reduce redundancy", "Adding more tables", "Removing tables", "Creating indexes"],
        "correct_answer": "Process of organizing data to reduce redundancy",
        "difficulty": "Medium",
        "tags": ["sql", "database-design"],
        "estimated_time": 2
    },
    {
        "question": "What is the difference between DELETE and TRUNCATE?",
        "options": ["DELETE can be rolled back, TRUNCATE cannot", "TRUNCATE can be rolled back, DELETE cannot", "No difference", "Both are the same"],
        "correct_answer": "DELETE can be rolled back, TRUNCATE cannot",
        "difficulty": "Medium",
        "tags": ["sql", "commands"],
        "estimated_time": 2
    },
    {
        "question": "What is an index in SQL?",
        "options": ["Data structure to improve query performance", "A table", "A view", "A constraint"],
        "correct_answer": "Data structure to improve query performance",
        "difficulty": "Low",
        "tags": ["sql", "performance"],
        "estimated_time": 1
    },
    {
        "question": "What is ACID in database transactions?",
        "options": ["Atomicity, Consistency, Isolation, Durability", "A SQL command", "A data type", "A function"],
        "correct_answer": "Atomicity, Consistency, Isolation, Durability",
        "difficulty": "High",
        "tags": ["sql", "transactions"],
        "estimated_time": 3
    },
    {
        "question": "What is a foreign key?",
        "options": ["Key that references primary key of another table", "A primary key", "An index", "A constraint only"],
        "correct_answer": "Key that references primary key of another table",
        "difficulty": "Low",
        "tags": ["sql", "basics"],
        "estimated_time": 1
    },
    {
        "question": "What is the difference between WHERE and HAVING?",
        "options": ["WHERE filters rows, HAVING filters groups", "HAVING filters rows, WHERE filters groups", "No difference", "Both are the same"],
        "correct_answer": "WHERE filters rows, HAVING filters groups",
        "difficulty": "Medium",
        "tags": ["sql", "queries"],
        "estimated_time": 2
    },
    {
        "question": "What is a view in SQL?",
        "options": ["Virtual table based on result of a query", "A physical table", "An index", "A constraint"],
        "correct_answer": "Virtual table based on result of a query",
        "difficulty": "Low",
        "tags": ["sql", "basics"],
        "estimated_time": 1
    },
    {
        "question": "What is the purpose of GROUP BY in SQL?",
        "options": ["Groups rows with same values into summary rows", "Sorts data", "Filters data", "Joins tables"],
        "correct_answer": "Groups rows with same values into summary rows",
        "difficulty": "Low",
        "tags": ["sql", "queries"],
        "estimated_time": 1
    },
    
    # Data Structures & Algorithms (10 questions)
    {
        "question": "What is the time complexity of binary search?",
        "options": ["O(log n)", "O(n)", "O(n log n)", "O(1)"],
        "correct_answer": "O(log n)",
        "difficulty": "Medium",
        "tags": ["algorithms", "search", "complexity"],
        "estimated_time": 2
    },
    {
        "question": "What is the time complexity of quicksort in average case?",
        "options": ["O(n log n)", "O(n²)", "O(n)", "O(log n)"],
        "correct_answer": "O(n log n)",
        "difficulty": "Medium",
        "tags": ["algorithms", "sorting", "complexity"],
        "estimated_time": 2
    },
    {
        "question": "What is the difference between BFS and DFS?",
        "options": ["BFS uses queue, DFS uses stack", "DFS uses queue, BFS uses stack", "No difference", "Both use queue"],
        "correct_answer": "BFS uses queue, DFS uses stack",
        "difficulty": "Medium",
        "tags": ["algorithms", "graph"],
        "estimated_time": 2
    },
    {
        "question": "What is a hash table?",
        "options": ["Data structure that maps keys to values", "A tree structure", "A linked list", "An array"],
        "correct_answer": "Data structure that maps keys to values",
        "difficulty": "Low",
        "tags": ["data-structures", "hash"],
        "estimated_time": 1
    },
    {
        "question": "What is the time complexity of inserting an element in a heap?",
        "options": ["O(log n)", "O(n)", "O(1)", "O(n log n)"],
        "correct_answer": "O(log n)",
        "difficulty": "Medium",
        "tags": ["data-structures", "heap", "complexity"],
        "estimated_time": 2
    },
    {
        "question": "What is dynamic programming?",
        "options": ["Solving problems by breaking into subproblems", "A sorting algorithm", "A data structure", "A search algorithm"],
        "correct_answer": "Solving problems by breaking into subproblems",
        "difficulty": "High",
        "tags": ["algorithms", "dynamic-programming"],
        "estimated_time": 3
    },
    {
        "question": "What is the time complexity of finding an element in a balanced BST?",
        "options": ["O(log n)", "O(n)", "O(1)", "O(n log n)"],
        "correct_answer": "O(log n)",
        "difficulty": "Medium",
        "tags": ["data-structures", "tree", "complexity"],
        "estimated_time": 2
    },
    {
        "question": "What is memoization?",
        "options": ["Storing results of expensive function calls", "A sorting technique", "A data structure", "A search method"],
        "correct_answer": "Storing results of expensive function calls",
        "difficulty": "Medium",
        "tags": ["algorithms", "optimization"],
        "estimated_time": 2
    },
    {
        "question": "What is the difference between array and linked list?",
        "options": ["Array has fixed size, linked list is dynamic", "Linked list has fixed size, array is dynamic", "No difference", "Both are the same"],
        "correct_answer": "Array has fixed size, linked list is dynamic",
        "difficulty": "Low",
        "tags": ["data-structures", "basics"],
        "estimated_time": 1
    },
    {
        "question": "What is the time complexity of merge sort?",
        "options": ["O(n log n)", "O(n²)", "O(n)", "O(log n)"],
        "correct_answer": "O(n log n)",
        "difficulty": "Medium",
        "tags": ["algorithms", "sorting", "complexity"],
        "estimated_time": 2
    }
]

# Subjective/SQL Questions (50 questions)
SUBJECTIVE_QUESTIONS = [
    {
        "question": "Write a SQL query to find the second highest salary from the Employees table.",
        "difficulty": "Medium",
        "tags": ["sql", "aggregation"],
        "estimated_time": 5
    },
    {
        "question": "Write a SQL query to find all employees who have the same salary.",
        "difficulty": "Medium",
        "tags": ["sql", "self-join"],
        "estimated_time": 5
    },
    {
        "question": "Write a SQL query to find the department with the highest number of employees.",
        "difficulty": "Low",
        "tags": ["sql", "group-by"],
        "estimated_time": 3
    },
    {
        "question": "Write a SQL query to delete duplicate rows from a table.",
        "difficulty": "Medium",
        "tags": ["sql", "delete"],
        "estimated_time": 5
    },
    {
        "question": "Write a SQL query to find employees who joined in the last 30 days.",
        "difficulty": "Low",
        "tags": ["sql", "date-functions"],
        "estimated_time": 3
    },
    {
        "question": "Write a SQL query to find the top 3 highest paid employees from each department.",
        "difficulty": "High",
        "tags": ["sql", "window-functions"],
        "estimated_time": 7
    },
    {
        "question": "Write a SQL query to find employees who do not have a manager.",
        "difficulty": "Low",
        "tags": ["sql", "null"],
        "estimated_time": 2
    },
    {
        "question": "Write a SQL query to calculate the running total of sales.",
        "difficulty": "Medium",
        "tags": ["sql", "window-functions"],
        "estimated_time": 5
    },
    {
        "question": "Write a SQL query to find customers who have placed orders in all categories.",
        "difficulty": "High",
        "tags": ["sql", "subquery"],
        "estimated_time": 7
    },
    {
        "question": "Write a SQL query to find the average salary by department, excluding departments with less than 5 employees.",
        "difficulty": "Medium",
        "tags": ["sql", "group-by", "having"],
        "estimated_time": 5
    },
    {
        "question": "Write a SQL query to find employees whose salary is greater than their manager's salary.",
        "difficulty": "Medium",
        "tags": ["sql", "self-join"],
        "estimated_time": 5
    },
    {
        "question": "Write a SQL query to find the nth highest salary using a subquery.",
        "difficulty": "High",
        "tags": ["sql", "subquery"],
        "estimated_time": 7
    },
    {
        "question": "Write a SQL query to find all products that have never been ordered.",
        "difficulty": "Medium",
        "tags": ["sql", "left-join"],
        "estimated_time": 5
    },
    {
        "question": "Write a SQL query to find the month with the highest sales.",
        "difficulty": "Low",
        "tags": ["sql", "group-by", "aggregation"],
        "estimated_time": 3
    },
    {
        "question": "Write a SQL query to find employees who have changed departments at least once.",
        "difficulty": "High",
        "tags": ["sql", "self-join", "aggregation"],
        "estimated_time": 7
    },
    {
        "question": "Write a SQL query to find the percentage of employees in each department.",
        "difficulty": "Medium",
        "tags": ["sql", "aggregation", "calculation"],
        "estimated_time": 5
    },
    {
        "question": "Write a SQL query to find customers who have made purchases in consecutive months.",
        "difficulty": "High",
        "tags": ["sql", "window-functions", "date"],
        "estimated_time": 7
    },
    {
        "question": "Write a SQL query to find the employee with the longest tenure in each department.",
        "difficulty": "Medium",
        "tags": ["sql", "window-functions"],
        "estimated_time": 5
    },
    {
        "question": "Write a SQL query to find all orders placed on weekends.",
        "difficulty": "Low",
        "tags": ["sql", "date-functions"],
        "estimated_time": 3
    },
    {
        "question": "Write a SQL query to find products that are out of stock (quantity = 0).",
        "difficulty": "Low",
        "tags": ["sql", "filtering"],
        "estimated_time": 2
    },
    {
        "question": "Write a SQL query to find the total revenue by customer, ordered by revenue descending.",
        "difficulty": "Low",
        "tags": ["sql", "group-by", "aggregation"],
        "estimated_time": 3
    },
    {
        "question": "Write a SQL query to find employees who earn more than the average salary of their department.",
        "difficulty": "Medium",
        "tags": ["sql", "subquery", "aggregation"],
        "estimated_time": 5
    },
    {
        "question": "Write a SQL query to find the top 5 customers by total purchase amount.",
        "difficulty": "Low",
        "tags": ["sql", "group-by", "limit"],
        "estimated_time": 3
    },
    {
        "question": "Write a SQL query to find all employees who report to the same manager.",
        "difficulty": "Medium",
        "tags": ["sql", "self-join"],
        "estimated_time": 5
    },
    {
        "question": "Write a SQL query to find departments that have at least one employee earning more than 100000.",
        "difficulty": "Low",
        "tags": ["sql", "exists", "subquery"],
        "estimated_time": 3
    },
    {
        "question": "Write a SQL query to find the difference between the highest and lowest salary in each department.",
        "difficulty": "Low",
        "tags": ["sql", "group-by", "aggregation"],
        "estimated_time": 3
    },
    {
        "question": "Write a SQL query to find employees who have the same first name.",
        "difficulty": "Low",
        "tags": ["sql", "self-join"],
        "estimated_time": 3
    },
    {
        "question": "Write a SQL query to find all orders placed in the last quarter.",
        "difficulty": "Medium",
        "tags": ["sql", "date-functions"],
        "estimated_time": 5
    },
    {
        "question": "Write a SQL query to find customers who have placed exactly 3 orders.",
        "difficulty": "Medium",
        "tags": ["sql", "group-by", "having"],
        "estimated_time": 5
    },
    {
        "question": "Write a SQL query to find the employee who joined most recently in each department.",
        "difficulty": "Medium",
        "tags": ["sql", "window-functions"],
        "estimated_time": 5
    },
    {
        "question": "Write a SQL query to find all products that have been ordered more than 100 times.",
        "difficulty": "Low",
        "tags": ["sql", "group-by", "having"],
        "estimated_time": 3
    },
    {
        "question": "Write a SQL query to find the cumulative sum of sales by month.",
        "difficulty": "Medium",
        "tags": ["sql", "window-functions"],
        "estimated_time": 5
    },
    {
        "question": "Write a SQL query to find employees whose name starts with 'A' and ends with 'n'.",
        "difficulty": "Low",
        "tags": ["sql", "pattern-matching"],
        "estimated_time": 2
    },
    {
        "question": "Write a SQL query to find the average order value by customer.",
        "difficulty": "Low",
        "tags": ["sql", "group-by", "aggregation"],
        "estimated_time": 3
    },
    {
        "question": "Write a SQL query to find all employees who have been with the company for more than 5 years.",
        "difficulty": "Low",
        "tags": ["sql", "date-functions"],
        "estimated_time": 3
    },
    {
        "question": "Write a SQL query to find departments with no employees.",
        "difficulty": "Low",
        "tags": ["sql", "left-join"],
        "estimated_time": 3
    },
    {
        "question": "Write a SQL query to find the rank of employees by salary within each department.",
        "difficulty": "Medium",
        "tags": ["sql", "window-functions"],
        "estimated_time": 5
    },
    {
        "question": "Write a SQL query to find customers who have purchased products from all available categories.",
        "difficulty": "High",
        "tags": ["sql", "subquery", "aggregation"],
        "estimated_time": 7
    },
    {
        "question": "Write a SQL query to find the median salary in each department.",
        "difficulty": "High",
        "tags": ["sql", "window-functions", "statistics"],
        "estimated_time": 7
    },
    {
        "question": "Write a SQL query to find employees who have never taken a leave.",
        "difficulty": "Medium",
        "tags": ["sql", "left-join"],
        "estimated_time": 5
    },
    {
        "question": "Write a SQL query to find the total number of orders placed each day for the last 7 days.",
        "difficulty": "Medium",
        "tags": ["sql", "date-functions", "group-by"],
        "estimated_time": 5
    },
    {
        "question": "Write a SQL query to find products with the highest and lowest prices.",
        "difficulty": "Low",
        "tags": ["sql", "aggregation"],
        "estimated_time": 3
    },
    {
        "question": "Write a SQL query to find employees who have worked in multiple departments.",
        "difficulty": "High",
        "tags": ["sql", "self-join", "aggregation"],
        "estimated_time": 7
    },
    {
        "question": "Write a SQL query to find the percentage change in sales from previous month.",
        "difficulty": "High",
        "tags": ["sql", "window-functions", "calculation"],
        "estimated_time": 7
    },
    {
        "question": "Write a SQL query to find all customers who have placed orders worth more than $1000.",
        "difficulty": "Low",
        "tags": ["sql", "group-by", "having"],
        "estimated_time": 3
    },
    {
        "question": "Write a SQL query to find the employee with the maximum salary in each department, along with their department name.",
        "difficulty": "Medium",
        "tags": ["sql", "window-functions", "join"],
        "estimated_time": 5
    },
    {
        "question": "Write a SQL query to find all orders that were placed on the same day as another order by the same customer.",
        "difficulty": "Medium",
        "tags": ["sql", "self-join"],
        "estimated_time": 5
    },
    {
        "question": "Write a SQL query to find the top 10% of employees by salary.",
        "difficulty": "High",
        "tags": ["sql", "window-functions", "percentile"],
        "estimated_time": 7
    },
    {
        "question": "Write a SQL query to find customers who have made purchases in at least 3 different months.",
        "difficulty": "Medium",
        "tags": ["sql", "group-by", "having", "date"],
        "estimated_time": 5
    },
    {
        "question": "Write a SQL query to find the average time between orders for each customer.",
        "difficulty": "High",
        "tags": ["sql", "window-functions", "date"],
        "estimated_time": 7
    },
    {
        "question": "Write a SQL query to find all employees who have the same manager and are in the same department.",
        "difficulty": "Medium",
        "tags": ["sql", "self-join"],
        "estimated_time": 5
    }
]

# DSA Questions (20 questions with 5 test cases each)
DSA_QUESTIONS = [
    {
        "problem": "Given an array of integers, find the maximum element.",
        "difficulty": "Low",
        "tags": ["arrays", "basic"],
        "estimated_time": 5,
        "testCases": [
            {
                "input": {"arr": [1, 2, 3, 4, 5]},
                "expectedOutput": 5,
                "description": "Basic case with ascending order"
            },
            {
                "input": {"arr": [5, 4, 3, 2, 1]},
                "expectedOutput": 5,
                "description": "Basic case with descending order"
            },
            {
                "input": {"arr": [1]},
                "expectedOutput": 1,
                "description": "Edge case with single element"
            },
            {
                "input": {"arr": [-10, -5, -1, -20]},
                "expectedOutput": -1,
                "description": "Edge case with negative numbers"
            },
            {
                "input": {"arr": [i for i in range(10000)]},
                "expectedOutput": 9999,
                "description": "Max boundary case with large array"
            }
        ]
    },
    {
        "problem": "Given a string, reverse it without using built-in reverse functions.",
        "difficulty": "Low",
        "tags": ["strings", "basic"],
        "estimated_time": 5,
        "testCases": [
            {
                "input": {"s": "hello"},
                "expectedOutput": "olleh",
                "description": "Basic case with normal string"
            },
            {
                "input": {"s": "a"},
                "expectedOutput": "a",
                "description": "Edge case with single character"
            },
            {
                "input": {"s": ""},
                "expectedOutput": "",
                "description": "Edge case with empty string"
            },
            {
                "input": {"s": "racecar"},
                "expectedOutput": "racecar",
                "description": "Edge case with palindrome"
            },
            {
                "input": {"s": "a" * 10000},
                "expectedOutput": "a" * 10000,
                "description": "Max boundary case with large string"
            }
        ]
    },
    {
        "problem": "Check if a number is prime.",
        "difficulty": "Medium",
        "tags": ["math", "algorithms"],
        "estimated_time": 10,
        "testCases": [
            {
                "input": {"n": 7},
                "expectedOutput": True,
                "description": "Basic case with prime number"
            },
            {
                "input": {"n": 4},
                "expectedOutput": False,
                "description": "Basic case with composite number"
            },
            {
                "input": {"n": 2},
                "expectedOutput": True,
                "description": "Edge case with smallest prime"
            },
            {
                "input": {"n": 1},
                "expectedOutput": False,
                "description": "Edge case with 1 (not prime)"
            },
            {
                "input": {"n": 997},
                "expectedOutput": True,
                "description": "Max boundary case with large prime"
            }
        ]
    }
]