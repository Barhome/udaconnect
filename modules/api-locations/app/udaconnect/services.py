import logging
import json
from flask import g
from datetime import datetime, timedelta
from typing import Dict, List
from app import db
from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text
from kafka import KafkaConsumer 

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")

TOPIC_NAME = 'items' 

class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def create(location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")
        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        # send new location to kafka
        kafka_data = new_location
        kafka_producer = g.kafka_producer
        kafka_producer.send('items', kafka_data)
        consumer = KafkaConsumer(bootstrap_servers='kafka-headless:9092',auto_offset_reset='earliest',value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        consumer.subscribe(['items'])
        for message in consumer:
            print (message)
            db.session.add(message)
            db.session.commit()
        return new_location
    

    @staticmethod
    def retrieve_all() -> List[Location]:
        return db.session.query(Location).all()

