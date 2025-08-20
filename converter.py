# function that takes in a JSON file and converts it to a Key Value mapping pair. It is able to dynamically generate/add signature blocks
# three main steps  
# the JSON file is a list of objects with the following structure:
"""
{
  "document_name": "Foster_SK_Lilac Easement Agreement (WA)",
  "grantor_type": "Individual",
  "grantor_name_1": "Stephen Douglas Foster",
  "grantor_name_2": "Karen Rene Foster",
  "trust_entity_name": "NA",
  "grantor_name": "Stephen Douglas Foster and Karen Rene Foster",
  "owner_type": "a married couple",
  "number_of_grantor_signatures": 2,
  "grantor_address_1": "1706 RIVER TRL SUGAR LAND",
  "grantor_address_2": "SUGAR LAND TX 77479",
  "state": "Washington",
  "county": "Spokane",
  "total_acres": 35.2,
  "apn_list": ["16174.908", "16174.9077", "16174.9078"],
  "parcels": [
    {
      "apn": "16174.908",
      "acres": 15.2,
      "legal_description": "17-26-41(SE1/4): THE NORTH 492.68 FT OF THE SOUTH 1645.84 FT OF THE SE1/4; EXCEPT THE WEST 1329.35 FT THEREOF. (PARCEL D ROS AFN 7390810)",
      "isPortion": false
    },
    {
      "apn": "16174.9077",
      "acres": 10,
      "legal_description": "17-26-41(SE1/4): THE WEST 887.00 FT OF THE NORTH 492.68 FT OF THE SOUTH 1645.84 FT OF THE SE1/4; EXCEPT COUNTY ROADS. (PARCEL A ROS AFN 7390810)",
      "isPortion": false
    },
    {
      "apn": "16174.9078",
      "acres": 10,
      "legal_description": "17-26-41(SE1/4): THE WEST 887.00 FT OF THE SOUTH 1153.16 FT OF THE SE1/4; EXCEPT THE S1/2 OF THE S1/2 OF SAID SE1/4; AND EXCEPT COUNTY ROADS. (PARCEL B ROS AFN 7390810)",
      "isPortion": false
    }
  ],
  "number_of_parcels": 3
}
"""


# after that the signature block with and without the notraries are created

# after that exhibit A is generated and apennded to the JSON

# the final format is a JSON file with the following structure:



#step one read the JSON file and assign the value on the left to the key and the value on the right to the value

# return the JSON key value mapping pair

 

