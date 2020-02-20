Feature: Load ETL transform data file and check that it end up in MySQL

  Scenario: Testing etl-load locally
    Given I load the transform file "test.sql" into a MySQL database running on "localhost" with a user of "user" and a password of "password" into the "zipster" database
    When I search for zipcodes within "2.0" miles of "07440"
    Then the results should be
      | zipcode | zipcode_type | city           | state | location_type | latitude | longitude | location                | decomissioned | distance          |
      | 07444   | STANDARD     | POMPTON PLAINS | NJ    | PRIMARY       | 40.96    | -74.3     | NA-US-NJ-POMPTON PLAINS | 0             | 1.477185115083272 |
      | 07035   | STANDARD     | LINCOLN PARK   | NJ    | PRIMARY       | 40.92    | -74.3     | NA-US-NJ-LINCOLN PARK   | 0             | 1.477240978042409 |
      | 07477   | UNIQUE       | WAYNE          | NJ    | PRIMARY       | 40.92    | -74.27    | NA-US-NJ-WAYNE          | 1             | 1.732068600965657 |
    When I search for zipcodes within "6.0" miles of "06612"
    Then the results should be
      | zipcode | zipcode_type | city           | state | location_type | latitude | longitude | location                | decomissioned | distance           |
      | 06883   | STANDARD     | WESTON         | CT    | PRIMARY       | 41.22    | -73.37    | NA-US-CT-WESTON         | 0             | 3.4105464758201736 |
      | 06875   | PO BOX       | REDDING CENTER | CT    | PRIMARY       | 41.3     | -73.38    | NA-US-CT-REDDING CENTER | 0             | 5.513520502095821  |
      | 06876   | PO BOX       | REDDING RIDGE  | CT    | PRIMARY       | 41.3     | -73.38    | NA-US-CT-REDDING RIDGE  | 0             | 5.513520502095821  |
      | 06896   | STANDARD     | REDDING        | CT    | PRIMARY       | 41.3     | -73.38    | NA-US-CT-REDDING        | 0             | 5.513520502095821  |
      | 06611   | STANDARD     | TRUMBULL       | CT    | PRIMARY       | 41.25    | -73.2     | NA-US-CT-TRUMBULL       | 0             | 5.756241520902255  |
    When I search for zipcodes within "3.0" miles of "91030"
    Then the results should be
      | zipcode | zipcode_type | city           | state | location_type | latitude | longitude | location                | decomissioned | distance           |
      | 91031	| PO BOX	   | SOUTH PASADENA	| CA	| PRIMARY	    | 34.11	   | -118.15   | NA-US-CA-SOUTH PASADENA | 0	         | 0                  |
      | 91189	| UNIQUE	   | PASADENA	    | CA  	| PRIMARY	    | 34.12	   | -118.16   | NA-US-CA-PASADENA	     | 0	         | 0.8969874654659848 |
      | 91115	| PO BOX	   | PASADENA	    | CA	| PRIMARY	    | 34.13	   | -118.15   | NA-US-CA-PASADENA	     | 0	         | 1.3818950740214173 |
      | 91184	| UNIQUE	   | PASADENA	    | CA	| PRIMARY	    | 34.13	   | -118.16   | NA-US-CA-PASADENA	     | 0	         | 1.4956454742065857 |
      | 91106	| STANDARD	   | PASADENA	    | CA	| PRIMARY	    | 34.13	   | -118.13   | NA-US-CA-PASADENA	     | 0	         | 1.7941347630838786 |
      | 91801	| STANDARD	   | ALHAMBRA	    | CA	| PRIMARY	    | 34.09	   | -118.13   | NA-US-CA-ALHAMBRA	     | 0	         | 1.7943073321849174 |
      | 91123	| UNIQUE	   | PASADENA	    | CA	| PRIMARY	    | 34.14	   | -118.15   | NA-US-CA-PASADENA	     | 0	         | 2.0727108262645757 |
      | 91124	| UNIQUE	   | PASADENA	    | CA	| PRIMARY	    | 34.14	   | -118.15   | NA-US-CA-PASADENA	     | 0	         | 2.0727108262645757 |
      | 91129	| UNIQUE	   | PASADENA	    | CA	| PRIMARY	    | 34.14	   | -118.15   | NA-US-CA-PASADENA	     | 0	         | 2.0727108262645757 |
      | 91102	| PO BOX	   | PASADENA	    | CA	| PRIMARY	    | 34.14	   | -118.14   | NA-US-CA-PASADENA	     | 0	         | 2.1502122791944007 |
      | 91105	| STANDARD	   | PASADENA	    | CA	| PRIMARY	    | 34.14	   | -118.16   | NA-US-CA-PASADENA	     | 0	         | 2.1502122791944007 |
      | 91182	| UNIQUE	   | PASADENA	    | CA	| PRIMARY	    | 34.14	   | -118.14   | NA-US-CA-PASADENA	     | 0	         | 2.1502122791944007 |
      | 91188	| UNIQUE	   | PASADENA	    | CA	| PRIMARY	    | 34.14	   | -118.14   | NA-US-CA-PASADENA	     | 0	         | 2.1502122791944007 |
      | 91125	| UNIQUE	   | PASADENA	    | CA	| PRIMARY	    | 34.13	   | -118.12   | NA-US-CA-PASADENA	     | 0	         | 2.2031860178016607 |
      | 91126	| UNIQUE	   | PASADENA	    | CA	| PRIMARY	    | 34.13	   | -118.12   | NA-US-CA-PASADENA	     | 0	         | 2.2031860178016607 |
      | 91802	| PO BOX	   | ALHAMBRA	    | CA	| PRIMARY	    | 34.09	   | -118.12   | NA-US-CA-ALHAMBRA	     | 0	         | 2.2035020405287025 |
      | 91804	| STANDARD	   | ALHAMBRA	    | CA	| PRIMARY	    | 34.09	   | -118.12   | NA-US-CA-ALHAMBRA	     | 0	         | 2.2035020405287025 |
      | 91841	| UNIQUE	   | ALHAMBRA	    | CA	| PRIMARY	    | 34.09	   | -118.12   | NA-US-CA-ALHAMBRA	     | 1	         | 2.2035020405287025 |
      | 91896	| PO BOX	   | ALHAMBRA	    | CA	| PRIMARY	    | 34.09	   | -118.12   | NA-US-CA-ALHAMBRA	     | 0	         | 2.2035020405287025 |
      | 90042	| STANDARD	   | LOS ANGELES	| CA	| PRIMARY	    | 34.11	   | -118.19   | NA-US-CA-LOS ANGELES	 | 0	         | 2.2883144920681744 |
      | 90032	| STANDARD	   | LOS ANGELES	| CA	| PRIMARY	    | 34.08	   | -118.17   | NA-US-CA-LOS ANGELES	 | 0	         | 2.367528373965177  |
      | 91101	| STANDARD	   | PASADENA	    | CA	| PRIMARY	    | 34.14	   | -118.13   | NA-US-CA-PASADENA	     | 0	         | 2.3675432142437    |
      | 91116	| PO BOX	   | PASADENA	    | CA	| PRIMARY	    | 34.14	   | -118.13   | NA-US-CA-PASADENA	     | 0	         | 2.3675432142437    |
      | 91899	| PO BOX	   | ALHAMBRA	    | CA	| PRIMARY	    | 34.08	   | -118.13   | NA-US-CA-ALHAMBRA	     | 0	         | 2.367739363527123  |
      | 91108	| STANDARD	   | SAN MARINO	    | CA	| PRIMARY	    | 34.12	   | -118.11   | NA-US-CA-SAN MARINO	 | 0	         | 2.3901863243250427 |
      | 91110	| UNIQUE	   | PASADENA	    | CA	| PRIMARY	    | 34.15	   | -118.15   | NA-US-CA-PASADENA	     | 0	         | 2.7637901480428346 |
      | 91131	| UNIQUE	   | PASADENA	    | CA	| PRIMARY	    | 34.15	   | -118.15   | NA-US-CA-PASADENA	     | 1	         | 2.7637901480428346 |
      | 91191	| UNIQUE	   | PASADENA	    | CA	| PRIMARY	    | 34.15	   | -118.15   | NA-US-CA-PASADENA	     | 1	         | 2.7637901480428346 |
      | 91803	| STANDARD	   | ALHAMBRA	    | CA	| PRIMARY	    | 34.07	   | -118.14   | NA-US-CA-ALHAMBRA	     | 0	         | 2.8224261818103455 |
      | 90050	| PO BOX	   | LOS ANGELES	| CA	| PRIMARY	    | 34.12	   | -118.2    | NA-US-CA-LOS ANGELES	 | 0	         | 2.9421481434643515 |
      | 91778	| PO BOX	   | SAN GABRIEL	| CA	| PRIMARY	    | 34.1	   | -118.1    | NA-US-CA-SAN GABRIEL	 | 0	         | 2.9429629554372325 |


