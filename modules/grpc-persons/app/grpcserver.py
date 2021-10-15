import time
from concurrent import futures
import grpc
import person_pb2
import person_pb2_grpc


personlist = [
 {"first_name": "Taco", "id": 5, "company_name": "Alpha Omega Upholstery", "last_name": "Fargo"},
 {"first_name": "Frank", "id": 6, "company_name": "USDA", "last_name": "Shader"}, 
 {"first_name": "Pam", "id": 1, "company_name": "Hampton, Hampton and McQuill", "last_name": "Trexler"}, 
 {"first_name": "Paul", "id": 8, "company_name": "Paul Badman & Associates", "last_name": "Badman"}, 
 {"first_name": "Otto", "id": 9, "company_name": "The Chicken Sisters Restaurant", "last_name": "Spring"}
 ]

class PersonServicer(person_pb2_grpc.PersonServiceServicer):
    def Get(self, request, context):
        print ('grpcserver recieved a request')
        allpersons =[]
        for  persondict in personlist:
           allpersons.append(person_pb2.PersonMessage(
                id = persondict['id'],
                first_name = persondict['first_name'],
                last_name = persondict['last_name'],
                company_name = persondict['company_name']
            ))


        result = person_pb2.PersonMessageList()
        result.persons.extend(allpersons)

        print('grpcserver succeded in delivering the request')
        return result



# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
person_pb2_grpc.add_PersonServiceServicer_to_server(PersonServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)