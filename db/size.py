from sqlalchemy.orm import sessionmaker
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer
from ts_util import *
from sqlalchemy.ext.declarative import declarative_base
from collections import defaultdict
import csv
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import settings
import sys

url = 'postgresql://tech:tech@127.0.0.1/techwatch'

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()

count = 0
for r in session.query(Recommendation):
	count += 1
print(count)
session.close()
engine.dispose()
