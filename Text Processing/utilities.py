import json

def disect_response(response):
    print(f"-----response.text-----\n{response.text}")
    print(f"-----response-----\n{response}")
    return
    print(f"Type :{type(response)}")
    print(f"dir(type):\n {dir(response)}")

    print("---response starts---")
    jstr = json.dumps(response.to_dict(), sort_keys=True, indent=4)
    print(jstr)
    
    print("---response end---")

