import discord
import os
import requests
import json
from keep_alive import keep_alive

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

def return_currency(base):
  response = requests.get("https://api.exchangeratesapi.io/latest?base="+base)
  json_data = json.loads(response.text)
  rates = json_data['rates']
  tmp = ""
  for i in rates:
    tmp += str(i) + " : " + str(rates[i]) + "\n"
  return tmp

def return_all_currencies():
  response = requests.get("https://api.exchangeratesapi.io/latest?base=EUR")
  json_data = json.loads(response.text)
  rates = json_data['rates']
  tmp = ""
  for currency in rates:
    tmp += currency + "\n"
  return tmp

def return_specific(base,value):
  response = requests.get("https://api.exchangeratesapi.io/latest?base="+base)
  json_data = json.loads(response.text)
  rates = json_data['rates']
  tmp = ""
  for i in rates:
    if(i == value):
      tmp = "1 " + str(base) + " = " + str(rates[i]) + str(value)
  return tmp

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content.lower()
  if msg.startswith('$return'):
    base_value = msg.split("$return ",1)[1]
    if base_value == "all":
      await message.channel.send(return_all_currencies())
    else:
      if "?" in base_value:
        values = base_value.split('?')
        base = values[1].strip().upper()
        value= values[0].strip().upper()
        await message.channel.send(return_specific(base,value))
      else:
        await message.channel.send(return_currency(base_value.upper()))
    
keep_alive()  
  
client.run(os.getenv('TOKEN'))