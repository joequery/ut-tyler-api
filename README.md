UT Tyler Student API
====================

This API serves as a way to retrieve information about a University of Texas at
Tyler student. The API accesses [MyUTTyler][0] and [UT Tyler's Blackboard][1]

[0]: http://my.uttyler.edu
[1]: http://blackboard.uttyler.edu

Requirements
------------

* Python 2.7
* pip/virtualenv

Installation
------------

    $ git clone git://github.com/joequery/ut-tyler-api.git
    $ cd ut-tyler-api
    $ virtualenv env
    $ . env/bin/activate
    $ pip install -r requirements.txt
    (env)$ python ut-api.py

API version
-----------
The most recent API version is 1.0

Is this API hosted anywhere for me to use in my projects?
---------------------------------------------------------
Not yet, but I plan on hosting a version on my server very soon. 

Endpoints
---------

### Making API calls

The URL should be structured `http://localhost:5000/API_VERSION/endpoint`. So, for
example, `http://localhost:5000/1.0/grades`.

All requests should be of type **POST**.

### Retrieving student grades

* Endpoint: `/grades`
* Expected data parameters:
    + `username`: The UT Tyler patriot user name
    + `password`: The UT Tyler patriot password
* Responses:
    + Student authentication failure
        - Status code: 401
        - JSON: `{"error": "authenticationFailure"}`
    + Generic Server Error
        - Status code: 500
        - JSON: `{"error": "serverError"}`
    + Successful grade retrieval
        - Status code: 200
        - JSON: 

                {'grades': 
                [
                    [
                        'ABSTRACT ALGEBRA I',
                        [
                            {
                                'date': 'Mar 8, 2013 9:05 AM',
                                'grade': '97.00 /100',
                                'timestamp': 1362755100,
                                'title': 'Test 1'
                            },
                            {
                                'date': 'Mar 1, 2013 9:24 AM',
                                'grade': '25.00 /25',
                                'timestamp': 1362151440,
                                'title': 'Homework 8'
                            },
                        ]
                    ],
                    [
                        'COMPUTER SECURITY MGMT',
                        [
                            {
                                'date': 'Mar 6, 2013 9:46 AM',
                                'grade': '79.00 /110',
                                'timestamp': 1362584760,
                                'title': 'Midterm Exam'
                            },
                            {
                                'date': 'Feb 25, 2013 10:42 AM',
                                'grade': '78.00 /100',
                                'timestamp': 1361810520,
                                'title': 'First Project Individual Score'
                            }
                        ]
                    ]
                ]
                }

### Retrieving blackboard announcements

* Endpoint: `/announcements`
* Expected data parameters:
    + `username`: The UT Tyler patriot user name
    + `password`: The UT Tyler patriot password
* Responses:
    + Student authentication failure
        - Status code: 401
        - JSON: `{"error": "authenticationFailure"}`
    + Generic Server Error
        - Status code: 500
        - JSON: `{"error": "serverError"}`
    + Successful announcement retrieval
        - Status code: 200
        - JSON: 

                {"announcements": 
                    [
                        {
                            "date": "Friday, March 8, 2013", 
                            "timestamp": 1362722400, 
                            "title": "Midterm Exam should be viewable now", 
                            "details": "You should be able to view your Midterm Exam now...", 
                            "course": "COSC 4361.001"
                        },
                        {
                            "date": "Wednesday, March 6, 2013", 
                            "timestamp": 1362549600, 
                            "title": "Office Hours", 
                            "details": "Office hours on Thursday are cancelled.", 
                            "course": "MATH 3336.001"
                        }
                    ]
                }

### Retrieving MyUTTyler info (schedule, TODO list, account summary)

* Endpoint: `/myuttyler`
* Expected data parameters:
    + `username`: The UT Tyler patriot user name
    + `password`: The UT Tyler patriot password
* Responses:
    + Student authentication failure
        - Status code: 401
        - JSON: `{"error": "authenticationFailure"}`
    + Generic Server Error
        - Status code: 500
        - JSON: `{"error": "serverError"}`
    + Successful myuttyler information retrieval
        - Status code: 200
        - JSON: 

                {'myuttyler': 
                    {'schedule': 
                        [
                            [
                                'Monday',
                                [
                                    {
                                        'courseNum': 4361,
                                        'location': 'Ratliff Building North 03038',
                                        'startTime': {
                                                         'hour': 9,
                                                         'min': 50,
                                                         'str': '9:50AM'
                                                     },
                                        'subject': 'COSC',
                                        'time': '9:00AM-9:50AM'
                                    },
                                    {
                                        'courseNum': 3336,
                                        'location': 'Ratliff Building North 04025',
                                        'startTime': {
                                                          'hour': 10,
                                                          'min': 50,
                                                          'str': '10:50AM'
                                                     },
                                        'subject': 'MATH',
                                        'time': '10:00AM-10:50AM'
                                    },
                                    {
                                        'courseNum': 4336,
                                        'location': 'Ratliff Building North 03039',
                                        'startTime': {
                                                         'hour': 12,
                                                         'min': 50,
                                                         'str': '12:50PM'
                                                     },
                                        'subject': 'COSC',
                                        'time': '12:00PM-12:50PM'
                                    }
                                ]
                            ],
                            ... Tuesday, Wednesday, Thursday
                            [
                                'Friday',
                                [
                                    {
                                        'courseNum': 3336,
                                        'location': 'Ratliff Building North 04025',
                                        'startTime': {
                                                         'hour': 10,
                                                         'min': 50,
                                                         'str': '10:50AM'
                                                     },
                                        'subject': 'MATH',
                                        'time': '10:00AM-10:50AM'
                                    },
                                ]
                            ],
                            [
                                'TBA',
                                [
                                    {
                                        'courseNum': 4229,
                                        'date': 'TBA',
                                        'startTime': {
                                                         'hour': 0,
                                                         'min': 0,
                                                         'str': '12:00AM'
                                                     },
                                        'subject': 'MUAP',
                                        'time': 'TBA'
                                    }
                                ]
                            ]
                        ],
                    'summary': False,
                    'todo': [
                                "TODO Item1",
                                "TODO Item2"
                            ]
                    }
                }
