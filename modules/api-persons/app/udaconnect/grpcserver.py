import time
from concurrent import futures
import grpc
import person_pb2
import person_pb2_grpc



class PersonServicer(person_pb2_grpc.PersonServiceServicer):
    def Get(self, request, context):

        # newperson = PersonService.retrieve_all()

        first_person = person_pb2.PersonMessage(
            id=2222,
            first_name = 'Ahmed',
            last_name = 'Ali',
            company_name= 'Aramco',
            
        )

        
        second_person = person_pb2.PersonMessage(
            id=1111,
            first_name = 'Mona',
            last_name = 'Hosam',
            company_name= 'Aramco',
            
        )

        result = person_pb2.PersonMessageList()
        result.persons.extend([first_person, second_person])

        # print(newperson)

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