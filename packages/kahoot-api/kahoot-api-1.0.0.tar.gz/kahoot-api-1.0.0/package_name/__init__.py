
"""
  A python package similar to the kahoot-spam npm package (nodejs)
"""

# imports
from kahoot import client


# join handle
def joinHandle():
  pass


# spam
def spam(name, code, amount):
  amount_bk = amount
  for i in range(amount):
    # bot
    bot = client()
    bot.join(code, f"{name}{amount_bk}")
    bot.on("joined", joinHandle())
    print(f"{name}{amount_bk} joined the kahoot")

    # amount
    amount_bk -= 1